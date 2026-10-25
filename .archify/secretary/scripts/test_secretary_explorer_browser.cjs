const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { chromium } = require('/Users/tai/.hermes/hermes-agent/node_modules/playwright');

const ROOT = '/Users/tai/.agents';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PROFILE = path.join(ROOT, '.archify/secretary/native/profile-legacy.html');
const SCRATCH = path.join(process.env.HOME, '.hermes/cache/scratch');

function luminance(rgb) {
  const m = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!m) return 0;
  const [r, g, b] = m.slice(1).map(Number).map(v => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

async function main() {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const detachedDir = fs.mkdtempSync(path.join(SCRATCH, 'secretary-standalone-'));
  const detachedProfile = path.join(detachedDir, 'profile.html');
  fs.copyFileSync(PROFILE, detachedProfile);
  try {
    const page = await browser.newPage();
    const consoleErrors = [];
    page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
    page.on('pageerror', e => consoleErrors.push(e.message));

    await page.goto('file://' + detachedProfile, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);

    assert.equal(await page.locator('iframe').count(), 0, 'expected no diagram iframes');
    assert.equal(await page.locator('#secretary-primary-graph').count(), 1, 'expected one primary graph');

    // both detail groups toggle
    const details = page.locator('details.cap-group');
    assert.ok(await details.count() >= 2, 'expected at least two detail groups');
    const firstDetails = details.nth(0);
    const initialOpen = await firstDetails.getAttribute('open') !== null;
    await firstDetails.locator('summary').click();
    await page.waitForTimeout(100);
    const afterToggle = await firstDetails.getAttribute('open') !== null;
    assert.notEqual(initialOpen, afterToggle, 'detail group should toggle');
    await firstDetails.locator('summary').click();

    // immutable authority summary
    const authority = page.locator('#authority-summary');
    assert.ok(await authority.isVisible(), 'authority summary must be visible');
    let authorityText = await authority.textContent();
    for (const phrase of [
      'active ~/.hermes/SOUL.md',
      'docs/profiles/secretary/SOUL.md',
      '~/.agents',
      'other Spaces are read-only',
      'preapproved Hermes runtime/profile maintenance',
      'Tai approval gates',
      'Hindsight desired bank',
      'localhost:8888',
    ]) {
      assert.ok(authorityText.includes(phrase), `authority summary missing: ${phrase}`);
    }

    // opencode affects exactly delegate
    const opencode = page.locator('input.cap-switch[data-cap-id="opencode"]');
    await opencode.uncheck();
    await page.waitForTimeout(200);
    let affected = await page.locator('.stage-card.affected').evaluateAll(nodes => nodes.map(n => n.dataset.stageId).sort());
    assert.deepStrictEqual(affected, ['delegate'], 'opencode should affect only delegate');
    let delegateStatus = await page.locator('.stage-card[data-stage-id="delegate"] .stage-status').textContent();
    assert.match(delegateStatus, /opencode disabled/);
    const delegateNodeAffected = await page.locator('#secretary-primary-graph [data-node-id="delegate"]').evaluate(n => n.classList.contains('affected'));
    assert.equal(delegateNodeAffected, true, 'delegate graph node should be affected');

    // hindsight affects exactly memory_context
    await page.locator('#reset-all').click();
    await page.waitForTimeout(200);
    const hindsight = page.locator('input.cap-switch[data-cap-id="hindsight"]');
    await hindsight.uncheck();
    await page.waitForTimeout(200);
    affected = await page.locator('.stage-card.affected').evaluateAll(nodes => nodes.map(n => n.dataset.stageId).sort());
    assert.deepStrictEqual(affected, ['memory_context'], 'hindsight should affect only memory_context');
    let memoryStatus = await page.locator('.stage-card[data-stage-id="memory_context"] .stage-status').textContent();
    assert.match(memoryStatus, /hindsight disabled/);
    const memoryNodeAffected = await page.locator('#secretary-primary-graph [data-node-id="memory_context"]').evaluate(n => n.classList.contains('affected'));
    assert.equal(memoryNodeAffected, true, 'memory_context graph node should be affected');

    // reset
    await page.locator('#reset-all').click();
    await page.waitForTimeout(200);
    affected = await page.locator('.stage-card.affected').count();
    assert.equal(affected, 0, 'reset should clear affected stages');
    const allChecked = await page.locator('input.cap-switch').evaluateAll(nodes => nodes.every(n => n.checked));
    assert.ok(allChecked, 'reset should check all switches');

    // keyboard Space toggle + Enter reset
    const firstCheckbox = page.locator('input.cap-switch').first();
    await firstCheckbox.focus();
    const beforeKey = await firstCheckbox.isChecked();
    await page.keyboard.press('Space');
    await page.waitForTimeout(100);
    const afterKey = await firstCheckbox.isChecked();
    assert.notEqual(beforeKey, afterKey, 'Space should toggle checkbox');
    await firstCheckbox.focus();
    await page.keyboard.press('Space');
    await page.waitForTimeout(100);
    await page.locator('#reset-all').focus();
    await page.keyboard.press('Enter');
    await page.waitForTimeout(100);
    const restored = await page.locator('input.cap-switch').evaluateAll(nodes => nodes.every(n => n.checked));
    assert.ok(restored, 'Enter should reset all switches');

    // authority summary remains visible and unchanged after toggles
    assert.ok(await authority.isVisible(), 'authority summary hidden after toggles');
    const afterToggleText = await authority.textContent();
    assert.equal(afterToggleText, authorityText, 'authority summary changed');

    // primary graph renders SVG nodes and edges
    const graph = page.locator('#secretary-primary-graph');
    assert.ok(await graph.count() === 1, 'primary graph missing');
    const nodeCount = await page.locator('#secretary-primary-graph [data-node-id]').count();
    assert.ok(nodeCount > 0, 'primary graph has no nodes');
    const edgeCount = await page.locator('#secretary-primary-graph [data-edge-id]').count();
    assert.ok(edgeCount > 0, 'primary graph has no edges');

    // empty external tools
    const html = await page.content();
    assert.ok(html.includes('External tools (0)'), 'external tools count missing');
    assert.ok(html.includes('None approved'), 'empty category marker missing');

    // overflow in light and dark
    for (const scheme of ['light', 'dark']) {
      await page.emulateMedia({ colorScheme: scheme });
      await page.waitForTimeout(100);
      for (const width of [1440, 390]) {
        await page.setViewportSize({ width, height: 900 });
        await page.waitForTimeout(100);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
        assert.equal(overflow, false, `overflow at ${width}px in ${scheme} mode`);
      }
    }

    // dark panel legible
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.waitForTimeout(100);
    const styles = await page.evaluate(() => {
      const p = document.querySelector('.panel');
      const s = getComputedStyle(p);
      return { bg: s.backgroundColor, color: s.color };
    });
    assert.ok(luminance(styles.bg) < 0.35, `dark panel not dark: ${styles.bg}`);
    assert.ok(luminance(styles.color) > 0.6, `dark panel text not legible: ${styles.color}`);

    assert.deepStrictEqual(consoleErrors, [], `console errors: ${consoleErrors.join('; ')}`);

    // malicious label fixture
    const fixtureRoot = fs.mkdtempSync(path.join(SCRATCH, 'secretary-explorer-malicious-'));
    const profileDir = path.join(fixtureRoot, 'docs/profiles/secretary');
    fs.mkdirSync(profileDir, { recursive: true });
    fs.writeFileSync(path.join(profileDir, 'capabilities.yaml'),
      "skills: ['<img src=x onerror=alert(1)>']\nplugins: []\nmcps: []\nexternal_tools: []\nautomation: []\n");
    const mappingDir = path.join(fixtureRoot, 'automation/profile-capabilities');
    fs.mkdirSync(mappingDir, { recursive: true });
    const nativeDir = path.join(fixtureRoot, '.archify/secretary/native');
    fs.mkdirSync(nativeDir, { recursive: true });
    fs.copyFileSync(path.join(ROOT, '.archify/secretary/native/unified-baseline.html'),
      path.join(nativeDir, 'unified-baseline.html'));
    fs.writeFileSync(path.join(mappingDir, 'workflow-mapping.yaml'),
      "profile: secretary\nstages:\n  - id: s1\n    label: Stage one\n    capability_ids: ['<img src=x onerror=alert(1)>']\n");
    try {
      execFileSync('python3', ['automation/profile-capabilities/secretary_explorer.py', '--repo-root', fixtureRoot],
        { cwd: ROOT, stdio: 'pipe' });
      const fixtureUrl = 'file://' + path.join(nativeDir, 'profile-legacy.html');
      const fixturePage = await browser.newPage();
      const dialogs = [];
      fixturePage.on('dialog', d => { dialogs.push(d.message()); d.dismiss(); });
      await fixturePage.goto(fixtureUrl, { waitUntil: 'domcontentloaded' });
      await fixturePage.waitForTimeout(500);
      const fixtureHtml = await fixturePage.content();
      assert.ok(!fixtureHtml.includes('<img src=x onerror=alert(1)>'), 'malicious tag rendered as HTML');
      assert.ok(fixtureHtml.includes('&lt;img src=x onerror=alert(1)&gt;'), 'malicious label not escaped');
      assert.deepStrictEqual(dialogs, [], 'unexpected dialog from malicious label');
      await fixturePage.close();
    } finally {
      fs.rmSync(fixtureRoot, { recursive: true, force: true });
    }

    console.log('PASS: secretary explorer browser assertions');
  } finally {
    await browser.close();
    fs.rmSync(detachedDir, { recursive: true, force: true });
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});