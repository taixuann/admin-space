const D = __DATA__;
const root = document.querySelector(".npu");
const stage = root.querySelector(".npu-stage");
const front = stage.querySelector(".npu-front");
const rig = front.querySelector(".npu-rig");
const live = root.querySelector("[data-live]");
const readout = root.querySelector("[data-readout]");
const pulseButton = root.querySelector("[data-pulse]");
const pulseLabel = root.querySelector("[data-pulse-label]");
const screenText = stage.querySelector("[data-screen-text]");
const needles = [0, 1, 2, 3].map((i) => stage.querySelector(`[data-needle="${i}"]`));
const partButtons = [...root.querySelectorAll(".npu-part")];
const still = matchMedia("(prefers-reduced-motion: reduce)");

const nodes = [...rig.querySelectorAll(".it")].map((el) => ({
  el,
  piece: el.dataset.piece,
  ride: el.dataset.ride || el.dataset.piece,
  key: Number(el.dataset.k),
  m: el.dataset.m.split(",").map(Number),
  index: Number(el.dataset.i),
  shown: "",
}));
for (const node of nodes) node.lift = node.m[0] * D.V[0] + node.m[1] * D.V[1] + node.m[2] * D.V[2];
let order = nodes.map((_, index) => index);

const IDS = Object.keys(D.pieces);
const STAGGER = D.stagger;
const SPRING = D.spring;
const piece = Object.fromEntries(IDS.map((id) => [id, { x: 0, v: 0, target: 0, pending: null }]));
const clamp = (value, low, high) => Math.min(high, Math.max(low, value));

let clock = 0;
let apart = false;
let selected = null;
let inside = false;
let leaveTimer = 0;
let touring = !still.matches;
let tourClock = -0.4;
let idleTimer = 0;
let visible = false;
let frame = 0;
let last = 0;

const pulse = {
  on: false,
  armed: false,
  tour: false,
  t: -1,
  stopAt: 5.8,
  stopping: -1,
  level: 0,
  rate: 0,
  phase: "",
};

function say(text) {
  if (readout.textContent !== text) readout.textContent = text;
}

function announce(phase) {
  if (pulse.phase === phase) return;
  pulse.phase = phase;
  if (live) live.textContent = phase;
}

function describe() {
  const text = selected
    ? D.pieces[selected].say
    : pulse.on
      ? "Executing analog VMM pulse"
      : apart
        ? "Exploded · 8 full-stack assemblies"
        : "Assembled · standby · 18 µS HRS";
  if (stage.getAttribute("aria-valuetext") !== text) stage.setAttribute("aria-valuetext", text);
}

function setApart(on) {
  if (apart === on) return;
  apart = on;
  const goal = on ? 1 : 0;
  let index = 0;
  for (const id of on ? STAGGER : [...STAGGER].reverse()) {
    if (!piece[id]) continue;
    if (piece[id].target === goal) piece[id].pending = null;
    else piece[id].pending = { value: goal, at: clock + (still.matches ? 0 : index++ * SPRING.stagger) };
  }
  describe();
  run();
}

function select(id) {
  if (id === "stand") id = null;
  if (selected === id) return;
  selected = id;
  for (const node of nodes) {
    if (id !== null && node.piece === id) node.el.setAttribute("data-on", "");
    else node.el.removeAttribute("data-on");
  }
  if (id) stage.setAttribute("data-focus", "");
  else stage.removeAttribute("data-focus");
  partButtons.forEach((button) =>
    button.dataset.part === id ? button.setAttribute("data-on", "") : button.removeAttribute("data-on"),
  );
  stage.setAttribute("aria-valuenow", String(id ? D.order.indexOf(id) + 1 : 0));
  describe();
}

function steerSpring(state, dt, calm) {
  if (state.pending && clock >= state.pending.at) {
    state.target = state.pending.value;
    state.pending = null;
  }
  if (calm) {
    state.x = state.target;
    state.v = 0;
    return false;
  }
  for (let index = 0; index < SPRING.substeps; index++) {
    const h = dt / SPRING.substeps;
    state.v += ((state.target - state.x) * SPRING.stiffness - state.v * SPRING.damping) * h;
    state.x += state.v * h;
  }
  if (Math.abs(state.target - state.x) < 2e-4 && Math.abs(state.v) < 2e-4) {
    state.x = state.target;
    state.v = 0;
    return state.pending !== null;
  }
  return true;
}

function needlePath(colIndex, share) {
  const cx = D.meters[colIndex][0];
  const cy = D.meters[colIndex][1];
  const cz = D.meterTop;
  const r = D.meterR - 2.4;
  const targetRatio = D.colCurrents[colIndex] / 22.0;
  const ratio = 0.12 + share * targetRatio;
  const angle = (ratio - 0.5) * 1.45;
  const x0 = cx - Math.sin(angle) * 1.8;
  const y0 = cy + Math.cos(angle) * 1.8;
  const x1 = cx + Math.sin(angle) * r;
  const y1 = cy - Math.cos(angle) * r;
  return lineOnTop([x0, y0], [x1, y1], cz + 0.25, D.P);
}

function place() {
  for (const node of nodes) {
    const share = piece[node.ride].x;
    const tx = (D.EX[0] * node.m[0] + D.EY[0] * node.m[1] + D.EZ[0] * node.m[2]) * share;
    const ty = (D.EX[1] * node.m[0] + D.EY[1] * node.m[1] + D.EZ[1] * node.m[2]) * share;
    const text = share === 0 ? "" : `translate(${tx.toFixed(2)} ${ty.toFixed(2)})`;
    if (text !== node.shown) {
      node.shown = text;
      if (text) node.el.setAttribute("transform", text);
      else node.el.removeAttribute("transform");
    }
  }
  const next = nodes
    .map((_, index) => index)
    .sort(
      (a, b) =>
        nodes[a].key +
        nodes[a].lift * piece[nodes[a].ride].x -
        (nodes[b].key + nodes[b].lift * piece[nodes[b].ride].x),
    );
  if (next.some((index, at) => index !== order[at])) {
    const fragment = document.createDocumentFragment();
    for (const index of next) fragment.appendChild(nodes[index].el);
    rig.appendChild(fragment);
    order = next;
  }
}

function pulseState(state) {
  if (state) pulseButton.dataset.state = state;
  else delete pulseButton.dataset.state;
}

function startPulse(fromTour = false) {
  if (pulse.on) return;
  setApart(false);
  select(null);
  pulse.on = true;
  pulse.armed = true;
  pulse.tour = fromTour;
  pulse.t = 0;
  pulse.stopping = -1;
  pulse.stopAt = fromTour ? 4.8 : 6.2;
  pulseState("armed");
  pulseLabel.textContent = "Reset";
  describe();
  run();
}

function stopPulse() {
  if (!pulse.on || pulse.stopping >= 0) return;
  pulse.stopping = pulse.t;
}

function stepPulse(dt, calm) {
  if (pulse.on && pulse.armed && IDS.every((id) => piece[id].x < 0.002 && !piece[id].pending)) {
    pulse.armed = false;
    pulseState("on");
    if (calm) pulse.t = 2.6;
  }
  if (pulse.on && !pulse.armed) pulse.t += dt;
  const t = pulse.t;
  if (pulse.on && pulse.stopping < 0 && t >= pulse.stopAt) pulse.stopping = t;

  const activeTarget = !pulse.on || pulse.armed || pulse.stopping >= 0 ? 0 : t < 0.7 ? 0.35 : 1;
  if (calm) {
    pulse.level = activeTarget;
    pulse.rate = 0;
  } else {
    const stiff = pulse.stopping >= 0 ? 18 : 36;
    const drag = 2 * Math.sqrt(stiff);
    for (let i = 0; i < 4; i++) {
      const h = dt / 4;
      pulse.rate += ((activeTarget - pulse.level) * stiff - pulse.rate * drag) * h;
      pulse.level = clamp(pulse.level + pulse.rate * h, 0, 1);
    }
  }

  for (let i = 0; i < 4; i++) {
    if (needles[i]) needles[i].setAttribute("d", needlePath(i, pulse.level));
  }
  stage.style.setProperty("--cf-glow", pulse.level.toFixed(3));

  if (screenText) {
    const hex = pulse.level > 0.65 ? "0x7A · 38.4T" : pulse.level > 0.2 ? "SET · 142uS" : "IDLE · 18uS";
    if (screenText.textContent !== hex) screenText.textContent = hex;
  }

  if (pulse.on) {
    const gVal = Math.round(18 + pulse.level * 124);
    const iSum = (2.2 + pulse.level * 16.2).toFixed(1);
    if (pulse.armed) {
      say("closing stack · arming pulse");
      announce("arming");
    } else if (pulse.stopping >= 0) {
      say(`resetting · G = ${gVal} µS · relaxing`);
      announce("reset");
    } else if (t < 0.8) {
      say("01–02 · DAC wordline encode · V = [1.8, 1.2, 0.8, 1.5] V");
      announce("wordline encode");
    } else if (t < 2.0) {
      say(`04–05 · SET filament bridging · E = 12 MV/m · G = ${gVal} µS`);
      announce("conductive filament potentiation");
    } else if (t < 3.6) {
      say(`03 & 07 · Kirchhoff VMM · ΣI_col0 = ${iSum} mA`);
      announce("analog vector-matrix multiply");
    } else {
      say(`08 · 8-bit SAR-ADC + Shift-Add · 0x7A · 38.4 TOPS/W`);
      announce("digital tensor latched");
    }
  }

  if (pulse.on && pulse.stopping >= 0 && pulse.level < 0.004 && Math.abs(pulse.rate) < 0.01) {
    pulse.on = false;
    pulse.t = -1;
    pulse.level = 0;
    pulse.rate = 0;
    pulseState("");
    pulseLabel.textContent = "Pulse VMM";
    announce("standby");
    describe();
    if (pulse.tour) tourClock = -0.4;
  }

  return pulse.on || pulse.level > 0.002;
}

const TOUR_STEP = 1.45;
function tourAt(time) {
  const apartFrom = 0.5;
  const listFrom = apartFrom + 0.8;
  const listTo = listFrom + D.order.length * TOUR_STEP;
  const fireAt = listTo + 1.1;
  if (time < apartFrom) return { apart: false, part: null, fire: false };
  if (time < listFrom) return { apart: true, part: null, fire: false };
  if (time < listTo) return { apart: true, part: D.order[Math.floor((time - listFrom) / TOUR_STEP)], fire: false };
  if (time < fireAt) return { apart: false, part: null, fire: false };
  return { apart: false, part: null, fire: true };
}

function quietTour() {
  touring = false;
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => {
    if (inside || pulse.on) return quietTour();
    touring = !still.matches;
    tourClock = -0.4;
    run();
  }, 3800);
}

function idleText() {
  if (selected) return D.pieces[selected].say;
  const moving = IDS.some((id) => Math.abs(piece[id].x - piece[id].target) > 0.002 || piece[id].pending);
  if (moving) return apart ? "exploding stack" : "closing stack";
  return apart ? "exploded · 8 full-stack layers" : "4×4 differential NPU · 18 µS HRS · standby";
}

function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  clock += dt;
  const calm = still.matches;
  if (touring && !pulse.on) {
    tourClock += dt;
    const step = tourAt(tourClock);
    setApart(step.apart);
    select(step.part);
    if (step.fire) startPulse(true);
  }
  let moving = false;
  for (const id of IDS) if (steerSpring(piece[id], dt, calm)) moving = true;
  const pulsing = stepPulse(dt, calm);
  place();
  if (!pulse.on) say(idleText());
  frame = visible && (moving || pulsing || touring) ? requestAnimationFrame(tick) : 0;
}

function run() {
  if (!frame && visible) {
    last = 0;
    frame = requestAnimationFrame(tick);
  }
}

new IntersectionObserver(
  (entries) => {
    visible = entries[entries.length - 1].isIntersecting;
    if (visible) run();
  },
  { rootMargin: "120px 0px" },
).observe(stage);

function pieceAt(event) {
  const hit = document.elementFromPoint(event.clientX, event.clientY);
  const item = hit && hit.closest ? hit.closest(".it") : null;
  return item ? item.dataset.piece : null;
}

stage.addEventListener("pointermove", (event) => {
  if (event.pointerType === "touch") return;
  inside = true;
  clearTimeout(leaveTimer);
  quietTour();
  if (pulse.on) return;
  setApart(true);
  select(pieceAt(event));
  run();
});

stage.addEventListener("pointerleave", () => {
  inside = false;
  clearTimeout(leaveTimer);
  leaveTimer = setTimeout(() => {
    if (inside) return;
    select(null);
    setApart(false);
  }, 260);
});

stage.addEventListener("pointerdown", (event) => {
  if (event.pointerType !== "touch" || pulse.on) return;
  quietTour();
  const id = pieceAt(event);
  if (!id || id === "stand") {
    select(null);
    setApart(!apart);
  } else {
    setApart(true);
    select(id);
  }
  run();
});

pulseButton.addEventListener("click", () => {
  quietTour();
  if (pulse.on) stopPulse();
  else startPulse(false);
  run();
});

partButtons.forEach((button) => {
  const show = () => {
    if (pulse.on) return;
    quietTour();
    clearTimeout(leaveTimer);
    setApart(true);
    select(button.dataset.part);
    run();
  };
  const hide = () => {
    clearTimeout(leaveTimer);
    leaveTimer = setTimeout(() => {
      if (inside || partButtons.some((other) => other.matches(":hover, :focus-visible"))) return;
      select(null);
      setApart(false);
    }, 260);
  };
  button.addEventListener("pointerenter", show);
  button.addEventListener("focus", show);
  button.addEventListener("pointerleave", hide);
  button.addEventListener("blur", hide);
  button.addEventListener("click", show);
});

stage.addEventListener("keydown", (event) => {
  const index = selected ? D.order.indexOf(selected) : -1;
  let next = null;
  if (event.key === "ArrowRight" || event.key === "ArrowDown") next = Math.min(D.order.length - 1, index + 1);
  else if (event.key === "ArrowLeft" || event.key === "ArrowUp") next = Math.max(0, index - 1);
  else if (event.key === "Home") next = 0;
  else if (event.key === "End") next = D.order.length - 1;
  else if (event.key === "Escape") {
    event.preventDefault();
    quietTour();
    if (pulse.on) stopPulse();
    select(null);
    setApart(false);
    run();
    return;
  } else if (event.key === "p" || event.key === "P" || event.key === "Enter") {
    event.preventDefault();
    quietTour();
    if (pulse.on) stopPulse();
    else startPulse(false);
    run();
    return;
  } else if (event.key === " ") {
    event.preventDefault();
    quietTour();
    if (!pulse.on) setApart(!apart);
    if (!apart) select(null);
    run();
    return;
  }
  if (next === null || pulse.on) return;
  event.preventDefault();
  quietTour();
  setApart(true);
  select(D.order[next]);
  run();
});

if (still.matches) touring = false;
place();
for (let i = 0; i < 4; i++) {
  if (needles[i]) needles[i].setAttribute("d", needlePath(i, 0));
}
