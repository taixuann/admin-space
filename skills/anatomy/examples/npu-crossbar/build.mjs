import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../kit/iso-kit.mjs";
import * as G from "../../kit/lathe.mjs";
import * as A from "../../kit/audit.mjs";
import { kitScript } from "../../scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const THEME = process.argv.includes("--light") ? "light" : "dark";

const W = 880;
const H = 680;
const AZIMUTH = 42;
const ELEVATION = 30;

const PLATE = { x: -156, y: -108, w: 312, d: 216, r: 8 };
const PLATE_H = 14;
const FOOT_H = 6;

const P = k.fitProjection(
  [
    ...k.boxCorners(PLATE, -PLATE_H - FOOT_H, 0),
    [-168, -110, 155],
    [168, 110, 145],
  ],
  W,
  H,
  { pad: 30, azimuth: AZIMUTH, elevation: ELEVATION },
);

const V = G.viewOf(P);
const at = (point) => k.iso(point, P);
const S = (paths, style) => k.solidSvg(paths, style);
const Ln = (d, style) => k.lineSvg(d, style);
const Dots = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) =>
  [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

const ZF = G.frameOf([0, 0, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0]);

const PIECES = {
  app: {
    name: "Application & spike-stream encoder",
    say: "01 Application layer · vision/LLM tensor features encoded into 4 parallel spike streams",
    move: [0, 0, 42],
  },
  dac: {
    name: "Wordline DAC & pulse driver bank",
    say: "02 Hardware input · 4-ch DAC quantizes activations into analog wordline voltages V_i",
    move: [-64, 0, 18],
  },
  crossbar: {
    name: "Differential memristive crossbar tile",
    say: "03 Computation layer · 4×4 crosspoint array computes I_j = Σ V_i · (G_ij⁺ − G_ij⁻) in O(1)",
    move: [0, 0, 44],
  },
  te: {
    name: "Top electrode & Ti oxygen reservoir",
    say: "04 Materials stack (top) · TiN barrier + Ti oxygen-gettering layer supplying Vo•• vacancies",
    move: [46, -24, 58],
  },
  filament: {
    name: "Switching oxide & conductive filament",
    say: "05 Dynamic mechanism · HfO2-x / PDA dielectric with field-driven Vo•• conductive filament",
    move: [68, 0, 26],
  },
  be: {
    name: "Bottom electrode & substrate pedestal",
    say: "06 Materials stack (bottom) · inert Pt bottom electrode on SiO2/Si heatsink wafer",
    move: [46, -24, 0],
  },
  adc: {
    name: "Bitline TIA & SAR-ADC readout bank",
    say: "07 Hardware output · virtual-ground TIAs sum column currents into 4 D'Arsonval meters & SAR-ADCs",
    move: [-26, 48, 12],
  },
  accum: {
    name: "Shift-and-add digital accumulator",
    say: "08 Bit-slicing & NoC output · reconstructs multi-bit weights into digital output tensor",
    move: [52, 48, 10],
  },
  stand: {
    name: "Granite bedplate & gantry",
    say: "",
    move: [0, 0, 0],
  },
};

const STAGGER = ["app", "te", "filament", "be", "dac", "crossbar", "adc", "accum", "stand"];
const SPRING = { stagger: 0.035, stiffness: 64, damping: 14.2, substeps: 4 };
const R = A.recorder(P, { order: STAGGER, spring: SPRING });
const { items, nameFor } = R;
const record = R.solid;

function put(piece, ref, svg, { bias = 0, move, ride, shapes = [], name } = {}) {
  const actualMove = move ?? PIECES[piece].move;
  const actualRide = ride ?? piece;
  R.put({
    piece,
    ride: actualRide,
    at: ref,
    bias,
    svg,
    move: actualMove,
    shapes,
    name: name ?? nameFor(`${piece}.item`),
  });
}

function boxAt(piece, plan, z0, h, style = {}, { steps = 4, bevel = 0.6, bias = 0, name, inner = "", extra = "" } = {}) {
  const id = name ?? nameFor(`${piece}.box`);
  const shape = record(A.slab(plan, z0, h, { name: id }, steps));
  const svg = S(k.slabOf(plan, z0, h, P, steps, bevel), { tone: "mid", ...style, inner }) + extra;
  put(piece, [plan.x + plan.w / 2, plan.y + plan.d / 2, z0 + h / 2], svg, {
    bias,
    name: id,
    shapes: [shape],
  });
  return shape;
}

function cylAt(piece, x, y, r, z0, h, style = {}, { steps = 32, bevel = 0, bias = 0, name, inner = "", extra = "" } = {}) {
  const id = name ?? nameFor(`${piece}.cyl`);
  const F = G.frameOf([x, y, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0]);
  const shape = record(A.disc(F, z0, z0 + h, r, { name: id }));
  const svg = S(k.cylinder(x, y, r, z0, h, P, steps, bevel), { tone: "mid", ...style, inner }) + extra;
  put(piece, [x, y, z0 + h / 2], svg, {
    bias,
    name: id,
    shapes: [shape],
  });
  return shape;
}

function planeMatrix(o, ex, ey) {
  const p0 = at(o);
  const px = at(G.add3(o, ex));
  const py = at(G.add3(o, ey));
  const v = (x) => x.toFixed(4);
  return `matrix(${v(px[0] - p0[0])} ${v(px[1] - p0[1])} ${v(py[0] - p0[0])} ${v(py[1] - p0[1])} ${p0[0].toFixed(2)} ${p0[1].toFixed(2)})`;
}

// ---------------------------------------------------------------------------
// 0. BASE PLATE & STAND
// ---------------------------------------------------------------------------
const back = [];
back.push(`<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>`);
for (const [x, y] of byDepth(k.corners(PLATE, 22))) {
  back.push(S(k.cylinder(x, y, 8, -PLATE_H - FOOT_H, 2, P, 28), { tone: "lo" }));
  back.push(S(k.cylinder(x, y, 6.2, -PLATE_H - FOOT_H + 2, FOOT_H - 2, P, 28), { tone: "mid" }));
}
back.push(
  S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 8, 1.6), {
    tone: "mid",
    inner: Ln(k.sideSeam(PLATE, -5, P, 8), { tone: "faint" }),
  }),
);
back.push(Ln(k.planOutline(k.insetPlan(PLATE, 5), 0, P), { tone: "lo" }));
const plateScrews = k.corners(PLATE, 11);
back.push(Ln(plateScrews.map(([x, y]) => k.ring(x, y, 2.4, 0, P, 16)).join(""), { tone: "lo" }));
back.push(Dots(plateScrews.map(([x, y]) => at([x, y, 0])), { size: 0.52 }));
record(A.slab(PLATE, -PLATE_H, PLATE_H, { name: "stand.plate", ground: true }, 8));

// Front calibration ruler strip
const STRIP = { x: -136, y: PLATE.y + PLATE.d - 14, w: 272, d: 6.5, r: 1 };
back.push(S(k.slabOf(STRIP, 0, 0.6, P, 3), { tone: "lo", crease: "none" }));
const stripTicks = k.topTicks(STRIP.x + 6, STRIP.x + STRIP.w - 6, 4, 5, STRIP.y + 0.8, 0.6, [2, 3.6], P);
back.push(Ln(stripTicks.minor, { tone: "lo" }), Ln(stripTicks.major, { tone: "mid" }));

// Engraved label plate on bedplate
const LABEL = { x: -144, y: 52, w: 38, d: 16, r: 1.4 };
back.push(S(k.slabOf(LABEL, 0, 0.8, P, 3), { tone: "lo", crease: "none" }));
back.push(Ln(k.planOutline(k.insetPlan(LABEL, 1.5), 0.8, P, 3), { tone: "faint" }));
back.push(
  Ln(
    [24, 18, 21]
      .map((w, i) => k.lineOnTop([LABEL.x + 4, LABEL.y + 4 + i * 3.6], [LABEL.x + 4 + w, LABEL.y + 4 + i * 3.6], 0.8, P))
      .join(""),
    { tone: "lo", free: true },
  ),
);
back.push(
  Dots([at([LABEL.x + LABEL.w - 3, LABEL.y + 3, 0.8]), at([LABEL.x + LABEL.w - 3, LABEL.y + LABEL.d - 3, 0.8])], {
    size: 0.45,
  }),
);

// Rear gantry columns & bridge beam supporting the Application layer
for (const [gx, tag] of [
  [-124, "L"],
  [-16, "R"],
]) {
  cylAt("stand", gx, -82, 6.8, 0, 4, { tone: "lo" }, { name: `stand.col.${tag}.base`, bevel: 0.4 });
  cylAt("stand", gx, -82, 4.2, 4, 84, { tone: "mid", crease: "none" }, {
    name: `stand.col.${tag}.shaft`,
    inner: Ln(k.sideArc(gx, -82, 4.2, 32, P, 18) + k.sideArc(gx, -82, 4.2, 62, P, 18), { tone: "faint" }),
  });
  cylAt("stand", gx, -82, 5.8, 88, 4, { tone: "mid" }, { name: `stand.col.${tag}.cap`, bevel: 0.3 });
}
const GANTRY = { x: -132, y: -88, w: 124, d: 12, r: 2 };
boxAt("stand", GANTRY, 92, 8, { tone: "mid" }, {
  name: "stand.gantry",
  bevel: 0.7,
  inner: Ln(k.sideSeam(GANTRY, 96, P, 4), { tone: "faint" }),
  extra: Dots([-124, -96, -70, -44, -16].map((x) => at([x, -82, 100])), { size: 0.48 }),
});

// ---------------------------------------------------------------------------
// 01. APPLICATION & SPIKE-STREAM ENCODER (Layer 1)
// ---------------------------------------------------------------------------
const APP_BOX = { x: -114, y: -87, w: 88, d: 10, r: 1.8 };
boxAt("app", APP_BOX, 100, 12, { tone: "mid" }, {
  name: "app.chassis",
  bevel: 0.7,
  inner: Ln(k.sideSeam(APP_BOX, 106, P, 4), { tone: "faint" }),
  extra: Dots([at([-108, -82, 112]), at([-32, -82, 112])], { size: 0.48 }),
});

cylAt("app", -70, -82, 13, 112, 5, { tone: "mid" }, { name: "app.turret.base", bevel: 0.4 });
{
  const drumTop = 127;
  const ticks = k.radialTicks(-70, -82, 9.8, 36, 6, drumTop, [1.1, 2.2], P);
  cylAt("app", -70, -82, 11, 117, 10, { tone: "hi", crease: "lo" }, {
    name: "app.turret.drum",
    bevel: 0.6,
    extra:
      Ln(k.knurl(-70, -82, 11, 119, 125, 42, P, 0.25), { tone: "lo" }) +
      Ln(k.ring(-70, -82, 9.2, drumTop, P, 36), { tone: "lo" }) +
      Ln(ticks.minor, { tone: "lo" }) +
      Ln(ticks.major, { tone: "mid" }) +
      Dots([at([-70, -82, drumTop])], { size: 0.55, tone: "hi" }),
  });
}
for (const [idx, cx] of [-104, -90, -50, -36].entries()) {
  cylAt("app", cx, -82, 3.2, 112, 7, { tone: "hi" }, {
    name: `app.ch.${idx}`,
    bevel: 0.3,
    extra:
      Ln(k.knurl(cx, -82, 3.2, 114, 118, 16, P), { tone: "lo" }) +
      Dots([at([cx, -82, 119])], { size: 0.45, tone: "hi" }),
  });
}

// ---------------------------------------------------------------------------
// 02. WORDLINE DAC & PULSE DRIVER BANK (Layer 3A)
// ---------------------------------------------------------------------------
const DAC_BASE = { x: -138, y: -48, w: 62, d: 80, r: 3 };
boxAt("dac", DAC_BASE, 0, 12, { tone: "mid" }, {
  name: "dac.base",
  bevel: 0.9,
  inner: Ln(k.sideSeam(DAC_BASE, 6, P, 4), { tone: "faint" }),
  extra: Ln(k.planOutline(k.insetPlan(DAC_BASE, 3), 12, P), { tone: "faint" }),
});

const DAC_DECK = { x: -132, y: -42, w: 50, d: 68, r: 2.2 };
boxAt("dac", DAC_DECK, 12, 6, { tone: "mid" }, {
  name: "dac.deck",
  bevel: 0.6,
  extra: Dots(k.corners(DAC_DECK, 4).map(([x, y]) => at([x, y, 18])), { size: 0.45 }),
});

const ROW_YS = [-33, -13, 7, 23];
ROW_YS.forEach((ry, i) => {
  const dx = -114;
  const topZ = 27;
  cylAt("dac", dx, ry, 5.8, 18, 9, { tone: "hi", crease: "lo" }, {
    name: `dac.dial.${i}`,
    bevel: 0.5,
    extra:
      Ln(k.knurl(dx, ry, 5.8, 20, 25.5, 28, P, 0.25), { tone: "lo" }) +
      Ln(k.ring(dx, ry, 4.2, topZ, P, 24), { tone: "lo" }) +
      Ln(k.lineOnTop([dx - 2, ry], [dx + 3.6, ry], topZ, P), { tone: "hi", free: true }) +
      Dots([at([dx, ry, topZ])], { size: 0.48, tone: "hi" }),
  });
  cylAt("dac", -92, ry, 3.1, 18, 5, { tone: "mid" }, {
    name: `dac.post.${i}`,
    bevel: 0.3,
    extra: Dots([at([-92, ry, 23])], { size: 0.42, tone: "hi" }),
  });
});

// ---------------------------------------------------------------------------
// 03. DIFFERENTIAL MEMRISTIVE CROSSBAR TILE (Layer 2)
// ---------------------------------------------------------------------------
const XBAR_PLINTH = { x: -58, y: -48, w: 84, d: 80, r: 3 };
boxAt("crossbar", XBAR_PLINTH, 0, 8, { tone: "lo" }, {
  name: "crossbar.plinth",
  bevel: 0.8,
  inner: Ln(k.sideSeam(XBAR_PLINTH, 4, P, 4), { tone: "faint" }),
  extra:
    Ln(k.planOutline(k.insetPlan(XBAR_PLINTH, 2.5), 8, P), { tone: "faint" }) +
    Dots(k.corners(XBAR_PLINTH, 5).map(([x, y]) => at([x, y, 8])), { size: 0.45 }),
});

const COL_XS = [-43, -23, -3, 17];
ROW_YS.forEach((ry, r) => {
  const wlPlan = { x: -54, y: ry - 2.2, w: 76, d: 4.4, r: 0.8 };
  boxAt("crossbar", wlPlan, 8, 3, { tone: "mid" }, {
    name: `crossbar.wl.${r}`,
    steps: 2,
    bevel: 0.3,
  });
});

COL_XS.forEach((cx, c) => {
  const blPlan = { x: cx - 2.4, y: -44, w: 4.8, d: 72, r: 0.8 };
  boxAt("crossbar", blPlan, 11, 3, { tone: "mid" }, {
    name: `crossbar.bl.${c}`,
    steps: 2,
    bevel: 0.3,
  });
});

for (let r = 0; r < 4; r++) {
  for (let c = 0; c < 4; c++) {
    const cx = COL_XS[c];
    const cy = ROW_YS[r];
    const topZ = 22;
    const rt = k.radialTicks(cx, cy, 3.4, 12, 3, topZ, [0.6, 1.1], P);
    cylAt("crossbar", cx, cy, 4.4, 14, 8, { tone: "hi", crease: "lo" }, {
      name: `crossbar.cell.${r}.${c}`,
      steps: 24,
      bevel: 0.4,
      extra:
        Ln(k.knurl(cx, cy, 4.4, 15.5, 20.5, 20, P, 0.25), { tone: "lo" }) +
        Ln(rt.minor, { tone: "faint" }) +
        Ln(rt.major, { tone: "lo" }) +
        Dots([at([cx, cy, topZ])], { size: 0.45, tone: "hi" }),
    });
  }
}

// ---------------------------------------------------------------------------
// 06. BOTTOM ELECTRODE & SUBSTRATE PEDESTAL (Layer 5B — Pt / SiO2 / Si)
// ---------------------------------------------------------------------------
const CELL_X = 86;
const CELL_Y = -34;
const BE_WAFER = { x: 48, y: -72, w: 76, d: 76, r: 3.5 };
boxAt("be", BE_WAFER, 0, 8, { tone: "lo" }, {
  name: "be.wafer",
  bevel: 0.9,
  inner: Ln(k.sideSeam(BE_WAFER, 4, P, 4), { tone: "faint" }),
  extra: Dots(k.corners(BE_WAFER, 6).map(([x, y]) => at([x, y, 8])), { size: 0.48 }),
});

const BE_OXIDE = { x: 54, y: -66, w: 64, d: 64, r: 3 };
boxAt("be", BE_OXIDE, 8, 6, { tone: "mid" }, {
  name: "be.oxide",
  bevel: 0.6,
  extra: Ln(k.planOutline(k.insetPlan(BE_OXIDE, 2.5), 14, P), { tone: "faint" }),
});

{
  const ptTop = 22;
  const ptTicks = k.radialTicks(CELL_X, CELL_Y, 24.5, 48, 6, ptTop, [1.2, 2.4], P);
  const bolts = Array.from({ length: 8 }, (_, i) => {
    const a = (i * Math.PI) / 4;
    return at([CELL_X + Math.cos(a) * 22.5, CELL_Y + Math.sin(a) * 22.5, ptTop]);
  });
  cylAt("be", CELL_X, CELL_Y, 26, 14, 8, { tone: "hi", crease: "lo" }, {
    name: "be.pt",
    steps: 48,
    bevel: 0.6,
    extra:
      Ln(k.knurl(CELL_X, CELL_Y, 26, 15.5, 20.5, 64, P, 0.25), { tone: "lo" }) +
      Ln(ptTicks.minor, { tone: "lo" }) +
      Ln(ptTicks.major, { tone: "mid" }) +
      Dots(bolts, { size: 0.46, tone: "mid" }),
  });
}
cylAt("be", CELL_X, CELL_Y, 20, 22, 3, { tone: "mid" }, {
  name: "be.seat",
  steps: 40,
  bevel: 0.3,
  extra: Ln(k.ring(CELL_X, CELL_Y, 17.5, 25, P, 36), { tone: "lo" }),
});

// ---------------------------------------------------------------------------
// 05. SWITCHING OXIDE & DYNAMIC CONDUCTIVE FILAMENT (Layer 4 — HfO2-x / PDA)
// ---------------------------------------------------------------------------
cylAt("filament", CELL_X, CELL_Y, 19.5, 25, 6, { tone: "lo" }, {
  name: "filament.collar.lo",
  steps: 40,
  bevel: 0.4,
  inner: Ln(k.sideArc(CELL_X, CELL_Y, 19.5, 28, P, 28), { tone: "faint" }),
  extra: Ln(k.ring(CELL_X, CELL_Y, 16, 31, P, 36), { tone: "faint" }),
});

// Central conical/stepped Conductive Filament (Vo•• vacancy percolation path)
cylAt("filament", CELL_X, CELL_Y, 7.5, 31, 6, { tone: "hi" }, {
  name: "filament.cf.base",
  steps: 28,
  bevel: 0.3,
  extra: Ln(k.knurl(CELL_X, CELL_Y, 7.5, 32, 36, 24, P, 0.2), { tone: "lo" }),
});
{
  const glowRing = k.ring(CELL_X, CELL_Y, 5.6, 40.5, P, 28);
  const glowExtras = `<path class="npu-cf-glow npu-cf-soft" d="${glowRing}"/><path class="npu-cf-glow" d="${glowRing}"/>`;
  cylAt("filament", CELL_X, CELL_Y, 4.8, 37, 7, { tone: "hi", lit: true }, {
    name: "filament.cf.neck",
    steps: 28,
    bevel: 0.3,
    extra: Ln(k.knurl(CELL_X, CELL_Y, 4.8, 38, 43, 20, P, 0.25), { tone: "lo" }) + glowExtras,
  });
}
cylAt("filament", CELL_X, CELL_Y, 9.2, 44, 7, { tone: "hi" }, {
  name: "filament.cf.top",
  steps: 32,
  bevel: 0.4,
  extra:
    Ln(k.knurl(CELL_X, CELL_Y, 9.2, 45.5, 50, 32, P, 0.25), { tone: "lo" }) +
    Ln(k.ring(CELL_X, CELL_Y, 7.4, 51, P, 28), { tone: "lo" }),
});

// Two cutaway dielectric stator columns supporting the top electrode
for (const [px, py, tag] of [
  [CELL_X - 13, CELL_Y - 8, "L"],
  [CELL_X + 13, CELL_Y + 8, "R"],
]) {
  cylAt("filament", px, py, 3.2, 31, 20, { tone: "mid", crease: "none" }, {
    name: `filament.stator.${tag}`,
    steps: 20,
    inner: Ln(k.sideArc(px, py, 3.2, 38, P, 14) + k.sideArc(px, py, 3.2, 44, P, 14), { tone: "faint" }),
  });
}

// ---------------------------------------------------------------------------
// 04. TOP ELECTRODE & Ti OXYGEN-GETTERING CAP (Layer 5A — TiN / Ti)
// ---------------------------------------------------------------------------
cylAt("te", CELL_X, CELL_Y, 20, 51, 7, { tone: "mid" }, {
  name: "te.ti",
  steps: 40,
  bevel: 0.5,
  inner: Ln(k.sideArc(CELL_X, CELL_Y, 20, 54.5, P, 28), { tone: "faint" }),
});

{
  const teTop = 67;
  const teTicks = k.radialTicks(CELL_X, CELL_Y, 23.5, 48, 6, teTop, [1.2, 2.5], P);
  const teBolts = Array.from({ length: 8 }, (_, i) => {
    const a = (i * Math.PI) / 4;
    return at([CELL_X + Math.cos(a) * 20.5, CELL_Y + Math.sin(a) * 20.5, teTop]);
  });
  cylAt("te", CELL_X, CELL_Y, 25, 58, 9, { tone: "hi", crease: "lo" }, {
    name: "te.tin",
    steps: 48,
    bevel: 0.7,
    extra:
      Ln(k.knurl(CELL_X, CELL_Y, 25, 60, 65.5, 64, P, 0.28), { tone: "lo" }) +
      Ln(k.ring(CELL_X, CELL_Y, 18, teTop, P, 40), { tone: "lo" }) +
      Ln(teTicks.minor, { tone: "lo" }) +
      Ln(teTicks.major, { tone: "mid" }) +
      Dots(teBolts, { size: 0.48, tone: "mid" }),
  });
}

cylAt("te", CELL_X, CELL_Y, 11.5, 67, 6, { tone: "mid" }, {
  name: "te.boss",
  steps: 32,
  bevel: 0.4,
  extra: Ln(k.ring(CELL_X, CELL_Y, 9.2, 73, P, 28), { tone: "lo" }),
});

cylAt("te", CELL_X, CELL_Y, 6.8, 73, 6, { tone: "hi" }, {
  name: "te.crown",
  steps: 28,
  bevel: 0.4,
  extra:
    Ln(k.knurl(CELL_X, CELL_Y, 6.8, 74, 78, 28, P, 0.25), { tone: "lo" }) +
    Ln(k.lineOnTop([CELL_X - 4, CELL_Y], [CELL_X + 4, CELL_Y], 79, P), { tone: "hi", free: true }) +
    Dots([at([CELL_X, CELL_Y, 79])], { size: 0.55, tone: "hi" }),
});

// ---------------------------------------------------------------------------
// 07. BITLINE TIA & SAR-ADC READOUT BANK (Layer 3B)
// ---------------------------------------------------------------------------
const ADC_MANIFOLD = { x: -62, y: 42, w: 92, d: 44, r: 3 };
boxAt("adc", ADC_MANIFOLD, 0, 10, { tone: "mid" }, {
  name: "adc.manifold",
  bevel: 0.8,
  inner: Ln(k.sideSeam(ADC_MANIFOLD, 5, P, 4), { tone: "faint" }),
  extra: Ln(k.planOutline(k.insetPlan(ADC_MANIFOLD, 2.5), 10, P), { tone: "faint" }),
});

const METERS = COL_XS.map((cx) => [cx, 70]);
const METER_R = 8.8;
const METER_TOP = 17;
const COL_CURRENTS = [18.4, 14.2, 11.6, 16.8];

METERS.forEach(([mx, my], c) => {
  // SAR-ADC comparator block behind each meter
  cylAt("adc", mx, 51, 4.6, 10, 9, { tone: "mid" }, {
    name: `adc.sar.${c}`,
    steps: 24,
    bevel: 0.4,
    extra:
      Ln(k.knurl(mx, 51, 4.6, 12, 17, 20, P, 0.2), { tone: "lo" }) +
      Dots([at([mx, 51, 19])], { size: 0.45, tone: "hi" }),
  });

  // D'Arsonval current-summing galvanometer dial
  const ticks = k.radialTicks(mx, my, METER_R - 1.8, 36, 6, METER_TOP, [0.9, 1.8], P);
  const angle = (0.12 - 0.5) * 1.45;
  const initNeedle = k.lineOnTop(
    [mx - Math.sin(angle) * 1.8, my + Math.cos(angle) * 1.8],
    [mx + Math.sin(angle) * (METER_R - 2.4), my - Math.cos(angle) * (METER_R - 2.4)],
    METER_TOP + 0.25,
    P,
  );
  const needleSvg = `<path data-needle="${c}" class="iso-line" data-tone="${c === 0 ? "lit" : "hi"}" data-free="start" d="${initNeedle}" style="stroke-width:1.1"/>`;

  cylAt("adc", mx, my, METER_R, 10, 7, { tone: "hi", crease: "lo" }, {
    name: `adc.meter.${c}`,
    steps: 36,
    bevel: 0.5,
    extra:
      Ln(k.knurl(mx, my, METER_R, 13.5, METER_TOP, 44, P, 0.25), { tone: "lo" }) +
      Ln(k.ring(mx, my, METER_R - 1.4, METER_TOP, P, 36), { tone: "lo" }) +
      Ln(ticks.minor, { tone: "lo" }) +
      Ln(ticks.major, { tone: "mid" }) +
      needleSvg +
      Dots([at([mx, my, METER_TOP])], { size: 0.48, tone: "hi" }),
  });
});

// ---------------------------------------------------------------------------
// 08. SHIFT-AND-ADD DIGITAL ACCUMULATOR & OUTPUT BUS (Layer 2B & 3C)
// ---------------------------------------------------------------------------
const ACCUM_BODY = { x: 44, y: 24, w: 92, d: 62, r: 3 };
{
  const faceM = planeMatrix([58, 86.05, 13], [1, 0, 0], [0, 0, -1]);
  const screenSvg = `<g transform="${faceM}"><rect class="npu-screen-rect" x="0" y="0" width="64" height="9" rx="1.2"/><text class="npu-screen-text" data-screen-text x="4" y="6.4" font-size="5.2">IDLE · 18uS</text></g>`;
  boxAt("accum", ACCUM_BODY, 0, 16, { tone: "mid" }, {
    name: "accum.body",
    bevel: 0.9,
    inner: Ln(k.sideSeam(ACCUM_BODY, 8, P, 4), { tone: "faint" }),
    extra: Ln(k.planOutline(k.insetPlan(ACCUM_BODY, 3), 16, P), { tone: "faint" }) + screenSvg,
  });
}

const ACCUM_DECK = { x: 52, y: 32, w: 76, d: 46, r: 2.2 };
boxAt("accum", ACCUM_DECK, 16, 6, { tone: "mid" }, {
  name: "accum.deck",
  bevel: 0.6,
  extra: Dots(k.corners(ACCUM_DECK, 4).map(([x, y]) => at([x, y, 22])), { size: 0.45 }),
});

for (const [rIdx, by] of [43, 65].entries()) {
  for (const [cIdx, bx] of [62, 80, 98, 116].entries()) {
    const bitIdx = rIdx * 4 + cIdx;
    cylAt("accum", bx, by, 3.4, 22, 6, { tone: "hi" }, {
      name: `accum.bit.${bitIdx}`,
      steps: 20,
      bevel: 0.3,
      extra:
        Ln(k.knurl(bx, by, 3.4, 23.5, 27, 16, P, 0.2), { tone: "lo" }) +
        Dots([at([bx, by, 28])], { size: 0.45, tone: "hi" }),
    });
  }
}

// ---------------------------------------------------------------------------
// SETTLE PAINTER'S KEYS & ASSEMBLE PAGE
// ---------------------------------------------------------------------------
A.settle(R, P);
items.sort((a, b) => a.key - b.key);

const groups = items.map((item, index) => {
  const [mx, my, mz] = item.move;
  return `<g class="it" data-piece="${item.piece}"${item.ride !== item.piece ? ` data-ride="${item.ride}"` : ""} data-k="${item.key.toFixed(2)}" data-m="${mx.toFixed(1)},${my.toFixed(1)},${mz.toFixed(1)}" data-i="${index}">${item.svg}</g>`;
});

const LABEL_TEXT =
  "Full-stack Neuromorphic Processing Unit (NPU) characterization and in-memory compute rig across 8 assemblies: (01) overhead application spike-stream encoder, (02) 4-channel wordline DAC driver bank, (03) 4x4 differential memristive crossbar array tile, (04) TiN/Ti top electrode and oxygen reservoir cap, (05) HfO2-x / Polydopamine switching dielectric with dynamic Vo•• conductive filament, (06) Pt/SiO2/Si bottom electrode pedestal, (07) virtual-ground TIA and 4 D'Arsonval current-summing galvanometers with SAR-ADCs, and (08) digital shift-and-add bit-slice accumulator.";

const backSvg = k.figureSvg({ width: W, height: H, label: LABEL_TEXT, body: back, className: "npu-back" });
const frontSvg = `<svg xmlns="http://www.w3.org/2000/svg" class="iso-svg npu-front" viewBox="0 0 ${W} ${H}" aria-hidden="true"><g class="npu-rig">${groups.join("")}</g></svg>`;

const unit = (vector) => {
  const o = at([0, 0, 0]);
  const p = at(vector);
  return [p[0] - o[0], p[1] - o[1]];
};

const DATA = {
  W,
  H,
  P,
  V,
  EX: unit([1, 0, 0]),
  EY: unit([0, 1, 0]),
  EZ: unit([0, 0, 1]),
  meters: METERS,
  meterR: METER_R,
  meterTop: METER_TOP,
  colCurrents: COL_CURRENTS,
  pieces: Object.fromEntries(Object.entries(PIECES).map(([id, piece]) => [id, { name: piece.name, say: piece.say }])),
  stagger: STAGGER,
  spring: SPRING,
  order: ["app", "dac", "crossbar", "te", "filament", "be", "adc", "accum"],
};

const PARTS = DATA.order
  .map(
    (id, index) =>
      `<button type="button" class="npu-part" data-part="${id}"><span class="npu-num">${String(index + 1).padStart(2, "0")}</span>${PIECES[id].name}</button>`,
  )
  .join("");

const corners = `<div class="iso-plate-corners" aria-hidden="true"><span class="iso-plate-corner" data-corner="fig">Fig 1</span><span class="iso-plate-corner" data-corner="title">Full-Stack NPU · Application to Device Stack</span><span class="iso-plate-corner" data-corner="readout" data-readout>4×4 differential NPU · 18 µS HRS · standby</span></div>`;

const controls = `<div class="npu-controls"><button type="button" class="npu-pulse" data-pulse><span class="npu-lamp" aria-hidden="true"></span><span data-pulse-label>Pulse VMM</span></button><span class="npu-hint">Hover to explode all 8 layers · click pills or press P to pulse</span><span class="npu-live" aria-live="polite" data-live></span></div>`;

const stage = `<div class="npu-stage" tabindex="0" role="slider" aria-label="Full-stack NPU rig. Hover or use arrow keys to explode and inspect the 8 layers from application down to materials; press P or the Pulse VMM button to execute a live SET and Vector-Matrix Multiplication cycle." aria-valuemin="0" aria-valuemax="${DATA.order.length}" aria-valuenow="0" aria-valuetext="Assembled · standby · 18 µS HRS">${backSvg}${frontSvg}</div>`;

const caption =
  "End-to-end physical hierarchy of a memristive Neural Processing Unit (NPU). Top-level application tensors (01) are converted by wordline DAC drivers (02) into analog voltages across a 4×4 differential crossbar array (03), computing I_j = Σ V_i · (G_ij⁺ − G_ij⁻) in one step via Ohm's and Kirchhoff's laws. Beside the array sits a magnified 20× cutaway of a single crosspoint cell: a TiN/Ti top electrode (04) scavenges oxygen from the sub-stoichiometric HfO2-x / Polydopamine switching dielectric (05), where electric fields (E ~ 12 MV/m) drive oxygen vacancies (Vo••) into a non-volatile Conductive Filament bridging to the inert Pt bottom electrode (06). Column currents sum into virtual-ground TIAs, analog galvanometer meters, and SAR-ADCs (07), before bit-sliced shift-and-add registers (08) reconstruct the digital output tensor.";

const body = `<figure class="iso-figure npu"><div class="iso-plate">${corners}${stage}${controls}</div><figcaption class="iso-legend"><span class="npu-parts">${PARTS}</span><span class="iso-caption">${caption}</span></figcaption></figure>`;

const CSS = readFileSync(join(HERE, "npu.css"), "utf8");
const LIVE = readFileSync(join(HERE, "live.js"), "utf8").replace("__DATA__", JSON.stringify(DATA));
const page = k.pageHtml({
  title: "Full-Stack Neuromorphic NPU",
  theme: THEME,
  body: `<style>${CSS}</style>${body}`,
  script: kitScript() + LIVE,
  width: 940,
});
const outName = THEME === "light" ? "npu-crossbar-light.html" : "npu-crossbar.html";
writeFileSync(join(HERE, outName), page);
console.log("wrote", outName, `${(page.length / 1024).toFixed(0)} KB`, `${items.length} items`);

if (process.argv.includes("--audit")) {
  A.auditOrExit(R, P);
}
