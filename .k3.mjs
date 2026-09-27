import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1280,height:900}, deviceScaleFactor:2});
await p.goto('file:///home/paps/tals-physik/themen/p6-2-elektrizitaet.html'); await p.waitForTimeout(1500);
const cv = await p.$('#ws-cv'); await cv.scrollIntoViewIfNeeded(); await p.waitForTimeout(500);
await p.evaluate(()=>{ if(wsLoop.running) document.getElementById('ws-btn').click(); });
const r = await p.evaluate(async ()=>{ let t=0; const N=64; for(let i=0;i<N;i++){ const a=performance.now(); wsT=(wsT+0.3)%40; wsRender(); await Promise.resolve(); await Promise.resolve(); t+=performance.now()-a; await new Promise(r=>setTimeout(r,16)); } return (t/N).toFixed(2); });
console.log('Animation, ms pro Bild:', r);
await b.close();
