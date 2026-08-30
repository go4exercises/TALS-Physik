import { chromium } from 'playwright';
const br = await chromium.launch();
for (const [seite, sel] of [['themen/p0-5-si-einheiten.html','#a2-modi .typ-btn, #a3-modi .typ-btn'],
                            ['themen/p6-2-elektrizitaet.html','.typ-btn, .preset-btn, button']]) {
  const p = await br.newPage({viewportSize:{width:1280,height:900}});
  const err=[]; p.on('pageerror', e=>err.push(String(e).slice(0,110)));
  await p.addInitScript(() => {
    window.__cv=[];
    const o = CanvasRenderingContext2D.prototype.fillText;
    CanvasRenderingContext2D.prototype.fillText = function(t,x,y){
      try{ window.__cv.push({t:String(t),x,br:this.measureText(String(t)).width,
                             cw:this.canvas.width,al:this.textAlign}); }catch(e){}
      return o.apply(this,arguments); };
  });
  await p.goto(`http://127.0.0.1:8774/${seite}`,{waitUntil:'networkidle'});
  await p.waitForTimeout(900);
  await p.evaluate(async (s)=>{
    const warte = ms=>new Promise(r=>setTimeout(r,ms));
    for (const b of document.querySelectorAll(s)) { b.click(); await warte(200);
      for (const r of document.querySelectorAll('input[type=range]')) {
        for (const v of [r.min, r.max]) { r.value=v; r.dispatchEvent(new Event('input',{bubbles:true})); await warte(90); } } }
  }, sel);
  await p.waitForTimeout(400);
  const t = await p.evaluate(()=> (window.__cv||[]).filter(e=>/;/.test(e.t)).map(e=>{
    const l = e.al==='center'?e.x-e.br/2:e.al==='right'?e.x-e.br:e.x;
    return {t:e.t,l:Math.round(l),r:Math.round(l+e.br),cw:e.cw};}));
  const u=[...new Map(t.map(x=>[x.t,x])).values()];
  console.log(`\n${seite}`);
  for(const x of u) console.log(`   ${(x.l>=-1&&x.r<=x.cw+1)?'ok ':'!! '}[${x.l}..${x.r}]/${x.cw}  «${x.t}»`);
  console.log('   JS-Fehler:', err.length?err:'keine');
  await p.close();
}
await br.close();
