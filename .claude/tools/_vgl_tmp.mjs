import { chromium } from 'playwright';
import fs from 'fs';
const [altRoot, neuRoot, out, ...namen] = process.argv.slice(2);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const res = [];
for (const n of namen) {
  const shots = {};
  for (const [tag, root] of [['alt', altRoot], ['neu', neuRoot]]) {
    await p.goto('file://' + fs.realpathSync(root + '/clips/' + n + '.html') + '?render');
    await p.waitForTimeout(200);
    const dauer = await p.evaluate(() => Math.max(0, ...[...document.querySelectorAll('[data-out]')].map(e => parseFloat(e.dataset.out))));
    shots[tag] = [];
    for (let t = 0.5; t < dauer; t += 1.0) {
      await p.evaluate(s => window.__seek(s), t);
      shots[tag].push([t, await p.screenshot()]);
    }
  }
  for (let i = 0; i < shots.alt.length; i++) {
    const [t, a] = shots.alt[i], bb = shots.neu[i][1];
    if (!a.equals(bb)) { fs.writeFileSync(`${out}/${n}_${t.toFixed(1)}_alt.png`, a); fs.writeFileSync(`${out}/${n}_${t.toFixed(1)}_neu.png`, bb); res.push(n + ' ' + t.toFixed(1)); }
  }
}
console.log(res.join('\n')); console.log('Abweichende Bilder:', res.length);
await b.close();
