// node stills.js page.html W H t1,t2,... prefix
const {chromium}=require('playwright');const [page,W,H,ts,pre]=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:+W,height:+H}});pg.on('pageerror',x=>console.log('ERR',x.message));
await pg.goto(`http://127.0.0.1:8766/${page}?w=${W}&h=${H}`);await pg.waitForFunction(()=>window.ready);await pg.evaluate(()=>window.ready);
for(const t of ts.split(',')){await pg.evaluate(t=>frame(+t,1),t);await pg.locator('#c').screenshot({path:`${pre}_${t}.png`})}await b.close()})();
