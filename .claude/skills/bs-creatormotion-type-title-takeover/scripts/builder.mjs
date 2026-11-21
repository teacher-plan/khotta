import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {themes,themeCSS,assertStyle,aspects,resolutions,safeAreas,backdropHTML,backdropJS} from './themes.mjs';

export const esc = value => String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const sha = data=>crypto.createHash('sha256').update(data).digest('hex');
// Footage frame size from ffprobe, with 90/270 degree rotation applied; null when unknown.
function probeSize(file){
  const run=spawnSync('ffprobe',['-v','error','-select_streams','v:0','-show_entries','stream=width,height:stream_side_data=rotation:stream_tags=rotate','-of','json',file],{encoding:'utf8'});
  if(run.status!==0)return null;
  try{const s=JSON.parse(run.stdout).streams?.[0];if(!s?.width)return null;const r=Math.abs(Number(s.tags?.rotate??s.side_data_list?.[0]?.rotation??0))%180;return r===90?{width:s.height,height:s.width}:{width:s.width,height:s.height};}catch{return null;}
}
// object-position for footage cover-fitted into a w×h region so the presenter's face (focus, fractions of the
// footage frame) lands on the target point of the region (fractions, default its centre), as far as the crop allows.
export function framing(size,focus,w,h,{x=.5,y=.5,zoom=1}={}){
  if(!size)return '50% 40%';
  const s=Math.max(w/size.width,h/size.height)*zoom,sw=size.width*s,sh=size.height*s;
  const axis=(scaled,box,f,t)=>scaled-box<1?50:Math.min(100,Math.max(0,(scaled*f-t*box)/(scaled-box)*100));
  return `${axis(sw,w,focus.x,x).toFixed(1)}% ${axis(sh,h,focus.y,y).toFixed(1)}%`;
}
// Graphics-only segments: sample the timeline at several moments, ignoring invisible elements and anything clipped
// by an overflow container, then centre the content block between the top margin and the lowest tenth of the frame
// and enlarge it (up to 1.2x) when it fills too little of that space.
function centreScript(width,height,safe){
  return `(()=>{const root=document.getElementById('cm-content'),stage=document.getElementById('cm-stage');if(!root||!stage)return;
const W=${width},H=${height},top=${safe.top},bottom=H-${safe.bottom},s=stage.getBoundingClientRect(),k=s.height/H;let t=Infinity,b=-Infinity,l=Infinity,r=-Infinity;
const box=el=>{const q=el.getBoundingClientRect();return {x0:(q.left-s.left)/k,x1:(q.right-s.left)/k,y0:(q.top-s.top)/k,y1:(q.bottom-s.top)/k};};
const clip=(el,q)=>{for(let a=el.parentElement;a&&a!==root;a=a.parentElement){const cs=getComputedStyle(a);if(cs.overflow!=='visible'||cs.overflowX!=='visible'||cs.overflowY!=='visible'){const c=box(a);q={x0:Math.max(q.x0,c.x0),x1:Math.min(q.x1,c.x1),y0:Math.max(q.y0,c.y0),y1:Math.min(q.y1,c.y1)};}}return q;};
const visit=el=>{const cs=getComputedStyle(el);if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity<.05)return;const leaf=['svg','img','video','canvas'].includes(el.tagName.toLowerCase())||!el.children.length;
if(!leaf){for(const c of el.children)visit(c);return;}let q=clip(el,box(el));q={x0:Math.max(0,q.x0),x1:Math.min(W,q.x1),y0:Math.max(0,q.y0),y1:Math.min(H,q.y1)};
if(q.x1-q.x0<1||q.y1-q.y0<1||(q.x1-q.x0)*(q.y1-q.y0)>W*H*.6)return;t=Math.min(t,q.y0);b=Math.max(b,q.y1);l=Math.min(l,q.x0);r=Math.max(r,q.x1);};
for(const p of [.3,.5,.7,.9,1]){tl.progress(p,true);for(const c of root.children)visit(c);}tl.progress(0,true);if(!isFinite(t))return;
const scale=Math.max(1,Math.min(1.2,(bottom-top)*.86/(b-t),W*.9/(r-l))),cx=(l+r)/2,cy=(t+b)/2,dy=(top+bottom)/2-cy;
if(Math.abs(dy)<8&&scale<1.03)return;root.style.transformOrigin=cx.toFixed(1)+'px '+cy.toFixed(1)+'px';
root.style.transform='translateY('+dy.toFixed(1)+'px)'+(scale>=1.03?' scale('+scale.toFixed(3)+')':'');})();`;
}
const hasChinese = value=>/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/.test(JSON.stringify(value??''));
// Smiley Sans (Deyi Hei) is the default face for every language; Noto Sans SC stays behind it for rare characters.
const zhFonts = {'smiley-sans':'Smiley Sans','noto-sans-sc':'Noto Sans SC'};

export async function createComposition({effect,out,assets,style='white-yellow',data={},media,images={},overrides={},fontFile,zhFont='smiley-sans',aspect='16:9',resolution='4k',focus,designPath,skillPath}) {
  if(!aspects[aspect])throw new Error(`Unknown --aspect ${aspect}. Choose ${Object.keys(aspects).join(', ')}.`);
  if(!resolutions[resolution])throw new Error(`Unknown --resolution ${resolution}. Choose ${Object.keys(resolutions).join(', ')}.`);
  const [baseWidth,baseHeight]=aspects[aspect],scale=resolutions[resolution],width=Math.round(baseWidth*scale),height=Math.round(baseHeight*scale);
  if(!zhFonts[zhFont])throw new Error(`Unknown --zh-font ${zhFont}. Choose ${Object.keys(zhFonts).join(', ')}.`);
  if(!effect.meta?.slug||typeof effect.default!=='function')throw new Error('Effect requires meta.slug and a default build function.');
  assertStyle(style);const selected=themes[style];
  const slug=effect.meta.slug;
  const resolved=path.resolve(out);
  await fs.mkdir(resolved,{recursive:true});
  await fs.mkdir(path.join(resolved,'assets'),{recursive:true});
  await fs.cp(path.join(assets,'fonts'),path.join(resolved,'assets/fonts'),{recursive:true});
  // Keep explicit faces in the composition so the strict renderer sees them too.
  const bundledFontCSS=(await Promise.all(['inter.css','noto-sans-sc.css','ibm-plex-mono.css','smiley-sans.css'].map(async file=>(await fs.readFile(path.join(assets,'fonts',file),'utf8')).replace(/url\(([^)]+)\)/g,'url(assets/fonts/$1)')))).join('\n');
  await fs.copyFile(path.join(assets,'gsap.min.js'),path.join(resolved,'assets/gsap.min.js'));
  let customFontCSS='';
  if(fontFile){
    const extension=path.extname(fontFile).toLowerCase();
    if(!['.woff2','.woff','.ttf','.otf'].includes(extension))throw new Error('Custom font must be WOFF2, WOFF, TTF or OTF.');
    overrides={...overrides,font:overrides.font||'Custom Font'};
    await fs.copyFile(fontFile,path.join(resolved,'assets','custom-font'+extension));
    customFontCSS=`@font-face{font-family:"${overrides.font}";src:url("assets/custom-font${extension}");font-weight:100 900;font-display:block;}`;
  }
  let mediaPath='';
  if(media){const ext=path.extname(media)||'.mp4';mediaPath='assets/presenter'+ext;}
  const imagePaths={};
  for(const [name,input] of Object.entries(images)){
    if(!/^[a-z0-9_-]+$/i.test(name))throw new Error(`Invalid image key ${name}`);
    imagePaths[name]=`assets/${name}${path.extname(input)}`;
  }
  const content={...effect.defaults,...data};
  const chinese=hasChinese(content);
  const typography={language:chinese?'zh':'en',font:fontFile||overrides.font?overrides.font:chinese?zhFonts[zhFont]:'Smiley Sans',source:fontFile?'custom-file':overrides.font?'override':chinese?'zh-default':'default'};
  // Mono labels and a Latin custom font still need the Chinese face for CJK glyphs.
  const cjkFallback=chinese?[zhFonts[zhFont]]:[];
  if(chinese&&typography.source==='zh-default')overrides={...overrides,font:zhFonts[zhFont]};
  // The face position in the footage defaults to a typical presenter framing when the agent does not pass --focus.
  const [fx,fy]=String(focus||'0.5,0.4').split(',').map(Number);
  if(!(fx>=0&&fx<=1&&fy>=0&&fy<=1))throw new Error('--focus takes the face centre as "x,y" fractions of the footage frame, for example 0.52,0.38.');
  const mediaSize=media?probeSize(media):null,presenterFocus={x:fx,y:fy};
  // Portrait splits put the content on top and the presenter below. The split sits high enough that the
  // presenter's whole head, forehead included, fits between the split and the caption band.
  // Full caption band only where footage plays; graphics-only segments are centred in the whole frame and
  // keep just the lowest tenth clear.
  const safe=media?safeAreas[aspect]:{top:safeAreas[aspect].top,bottom:Math.round(baseHeight*.1)},portraitCanvas=baseHeight>baseWidth;
  const presenterTop=portraitCanvas?Math.round(baseHeight-safe.bottom-(aspect==='9:16'?560:480)):null;
  const split=portraitCanvas?{contentTop:safe.top,contentBottom:presenterTop-28,presenterTop,presenterHeight:baseHeight-presenterTop}:null;
  // A wide presenter region at the bottom of a portrait canvas centres the head in the visible space above the
  // caption band. The face centre sits slightly below the head centre (hair above, chin below).
  const presenterTarget=(w,h,target={})=>{
    if(target.y!==undefined||!portraitCanvas||w/h<=.95||h>baseHeight*.66)return target;
    const scale=mediaSize?Math.max(w/mediaSize.width,h/mediaSize.height):1,mh=(mediaSize?.height??baseHeight)*scale,top=baseHeight-h;
    const faceCentre=(top+baseHeight-safe.bottom)/2+.03*mh;
    return {...target,y:Math.min(.6,Math.max(.05,(faceCentre-top)/h))};
  };
  const ctx={data:content,media:mediaPath,images:imagePaths,esc,theme:{...selected,...overrides},style,aspect,width:baseWidth,height:baseHeight,portrait:baseHeight>baseWidth,safe,split,mediaSize,focus:presenterFocus,frame:(w,h,target)=>framing(mediaSize,presenterFocus,w,h,presenterTarget(w,h,target))};
  const result=effect.default(ctx);
  if(!result.html||!result.js||!Number.isFinite(result.duration)||result.duration<=0)throw new Error(`Invalid composition result from ${slug}`);
  if(result.html.includes('src="undefined"')||result.html.includes('src=""'))throw new Error('A required media input is missing.');
  const assetReferences=result.html+'\n'+(result.css||'')+'\n'+result.js;
  if(mediaPath&&assetReferences.includes(mediaPath))await fs.copyFile(media,path.join(resolved,mediaPath));
  for(const [name,target] of Object.entries(imagePaths))if(assetReferences.includes(target))await fs.copyFile(images[name],path.join(resolved,target));
  const metadata={slug,style,aspect,resolution,focus:media?presenterFocus:undefined,duration:result.duration,width,height,designWidth:baseWidth,designHeight:baseHeight,fps:30,typography,content,overrides};
  const html=`<!doctype html>\n<html lang="${chinese?'zh-CN':'en'}"><head><meta charset="utf-8"><title>${esc(effect.meta.name)} · ${esc(selected.name)}</title><style>${bundledFontCSS}\n${themeCSS(style,overrides,{cjkFallback,width:baseWidth,height:baseHeight,scale})}\n${customFontCSS}\n${result.css||''}</style></head><body><div id="composition" data-composition-id="${slug}" data-start="0" data-duration="${result.duration}" data-width="${width}" data-height="${height}" data-fps="30"><div id="cm-stage">${backdropHTML()}${media?result.html:`<div id="cm-content" style="position:absolute;inset:0">${result.html}</div>`}</div></div><script src="assets/gsap.min.js"></script><script>\nconst tl=gsap.timeline({paused:true,defaults:{ease:'power3.out'}});\n${backdropJS(result.duration)}${result.js}\n${media?'':centreScript(baseWidth,baseHeight,safe)}\nwindow.__timelines=window.__timelines||{};window.__timelines[${JSON.stringify(slug)}]=tl;\n</script></body></html>`;
  await fs.writeFile(path.join(resolved,'index.html'),html);
  await fs.writeFile(path.join(resolved,'hyperframes.json'),JSON.stringify({$schema:'https://hyperframes.heygen.com/schema/hyperframes.json',registry:'https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry',paths:{blocks:'compositions',components:'compositions/components',assets:'assets'},media:{autoProxy:false},skill:slug},null,2));
  await fs.writeFile(path.join(resolved,'package.json'),JSON.stringify({name:slug,private:true,type:'module',scripts:{preview:'npx --yes hyperframes@0.8.30 preview',check:'npx --yes hyperframes@0.8.30 check',render:'npx --yes hyperframes@0.8.30 render --fps 30 --quality high --strict'}},null,2));
  if(designPath)await fs.copyFile(designPath,path.join(resolved,'DESIGN.md'));
  const skillHash=skillPath?sha(await fs.readFile(skillPath)):null;
  await fs.writeFile(path.join(resolved,'build.json'),JSON.stringify({...metadata,builtAt:new Date().toISOString(),htmlSha256:sha(html),skillSha256:skillHash},null,2));
  return {...metadata,out:resolved,htmlSha256:sha(html),skillSha256:skillHash};
}
