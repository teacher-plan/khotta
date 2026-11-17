// node render.js page.html W H dur out.mp4 [workers] [sub]
const {chromium}=require('playwright');const {spawn,execFileSync}=require('child_process');const fs=require('fs');
const [page,W,H,dur,out,workers='4',sub='2']=process.argv.slice(2);const FPS=60,N=Math.round(+dur*FPS),K=+workers;
(async()=>{const b=await chromium.launch();const parts=[];
await Promise.all([...Array(K).keys()].map(async w=>{const a=Math.floor(N*w/K),e=Math.floor(N*(w+1)/K);const part=`${out}.part${w}.mp4`;parts[w]=part;
 const pg=await b.newPage({viewport:{width:+W>+H?960:540,height:+W>+H?540:960}});pg.on('pageerror',x=>console.log('ERR',x.message));
 await pg.goto(`http://127.0.0.1:8766/${page}?w=${W}&h=${H}`);await pg.waitForFunction(()=>window.ready);await pg.evaluate(()=>window.ready);
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',''+FPS,'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','fast',part]);
 for(let f=a;f<e;f++){const d=await pg.evaluate(([t,s])=>{frame(t,s);return document.getElementById('c').toDataURL('image/jpeg',.95)},[f/FPS,+sub]);
  if(!ff.stdin.write(Buffer.from(d.split(',')[1],'base64')))await new Promise(r=>ff.stdin.once('drain',r));if(w==0&&f%300==0)console.log('frame',f,'/',e)}
 ff.stdin.end();await new Promise(r=>ff.on('close',r))}));
await b.close();fs.writeFileSync(out+'.txt',parts.map(p=>`file '${require('path').resolve(p)}'`).join('\n'));
execFileSync('ffmpeg',['-y','-loglevel','error','-f','concat','-safe','0','-i',out+'.txt','-c','copy',out]);parts.forEach(p=>fs.unlinkSync(p));fs.unlinkSync(out+'.txt');console.log('OK',out)})();
