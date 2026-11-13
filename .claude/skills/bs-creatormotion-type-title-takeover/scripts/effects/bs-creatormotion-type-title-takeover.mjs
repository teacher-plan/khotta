export const meta={slug:'bs-creatormotion-type-title-takeover',name:'Title Scene Takeover',category:'type',duration:5.4,description:'An oversized condensed headline punches in behind a presenter. A clean edit removes the presenter while the same lettering holds its scale and position.'};
export const defaults={title:'BUILD WITH US',supportingLine:'One small project every week'};

// The headline and its supporting line form one block centred between the top margin and the caption band.
// Landscape sets the headline as one condensed line across the frame; portrait stacks it in up to two lines.
// While the presenter is on screen the headline sits behind the cutout; after the cut it is fully readable in place.
const layout={
 '16:9':{lines:1,max:440,margin:96,sub:46,gap:44,align:'right'},
 '4:3':{lines:1,max:380,margin:64,sub:40,gap:40,align:'right'},
 '3:4':{lines:2,max:330,margin:52,sub:50,gap:44,align:'center'},
 '9:16':{lines:2,max:420,margin:48,sub:60,gap:52,align:'center'},
};
const units=s=>[...s].reduce((u,c)=>u+(/[\u3000-\u9fff\uff00-\uffef]/.test(c)?1:c===' '?.26:/[A-Z0-9]/.test(c)?.58:/[a-z]/.test(c)?.5:.4),0);
const split=t=>{const w=t.split(/\s+/).filter(Boolean);if(w.length>1){let best=1,diff=1e9;for(let i=1;i<w.length;i++){const d=Math.abs(units(w.slice(0,i).join(' '))-units(w.slice(i).join(' ')));if(d<diff){diff=d;best=i}}return [w.slice(0,best).join(' '),w.slice(best).join(' ')]}const c=[...t];if(c.length<5)return [t];const h=Math.ceil(c.length/2);return [c.slice(0,h).join(''),c.slice(h).join('')];};

export default function build({data:d,media,images={},esc:e,aspect='16:9',width:W,height:H,safe,frame}) {
  if(!images['presenter-matte']) throw new Error('An aligned presenter-matte alpha video is required.');
  const title=String(d.title??defaults.title).trim();
  if(!title) throw new Error('A short title is required.');
  if([...title].length>32) throw new Error('Keep the takeover title to 32 characters or fewer; this is an oversized headline, not a paragraph.');
  const L=layout[aspect],pos=frame(W,H,{x:.5,y:.44}),lines=L.lines===2?split(title):[title],avail=W-2*L.margin,sk=.0699;
  // Condensed sizing: glyphs may compress to 42% of their natural width before the size drops.
  const fs=Math.min(L.max,...lines.map(s=>avail/(units(s)*.42)));
  const support=String(d.supportingLine??'').trim(),subH=support?L.gap+L.sub*1.25:0;
  const blockH=lines.length*.8*fs+(lines.length-1)*.2*fs+subH,top=Math.max(safe.top+16,(safe.top+H-safe.bottom)/2-blockH/2);
  const base=lines.map((_,i)=>top+.8*fs+i*fs);
  const svg=lines.map((s,i)=>`<text x="${W/2}" y="${base[i].toFixed(1)}" text-anchor="middle" textLength="${Math.min(avail,units(s)*fs*1.05).toFixed(1)}" lengthAdjust="spacingAndGlyphs" font-size="${fs.toFixed(1)}" transform="translate(${(sk*base[i]).toFixed(1)} 0) skewX(-4)">${e(s)}</text>`).join('');
  const subTop=base[base.length-1]+L.gap,titleW=Math.min(avail,Math.max(...lines.map(s=>units(s)*fs*1.05)));
  const subBox=L.align==='right'?`left:${L.margin}px;width:${(W+titleW)/2-L.margin}px;text-align:right`:`left:${L.margin}px;right:${L.margin}px;text-align:center`;
  return {
    duration:5.4,
    html:`<video id="takeover-base" class="takeover-video" src="${e(media)}" muted playsinline data-start="0" data-duration="1.8" data-track-index="0"></video>
<div id="takeover-grade" class="takeover-grade"></div>
<div id="takeover-cover" class="takeover-cover"></div>
<div class="takeover-type-stage"><div id="takeover-title" data-layout-allow-occlusion class="takeover-title"><svg role="img" aria-label="${e(title)}" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">${svg}</svg></div></div>
<div id="takeover-subject" class="takeover-subject"><video id="takeover-matte" class="takeover-video" src="${e(images['presenter-matte'])}" muted playsinline data-start="0" data-duration="1.8" data-track-index="1"></video></div>
<div class="takeover-support-stage"><p id="takeover-support">${e(support)}</p></div>`,
    css:`.takeover-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${pos}}.takeover-subject{position:absolute;inset:0}.takeover-grade{position:absolute;inset:0;background:#000;opacity:.35}.takeover-cover{position:absolute;inset:0;background:var(--canvas-bg);opacity:0}.takeover-type-stage{position:absolute;inset:0;pointer-events:none}.takeover-title{position:absolute;inset:0;transform-origin:50% ${((top+blockH/2)/H*100).toFixed(1)}%;color:#F5F5F5}.takeover-title svg{display:block;width:100%;height:100%;overflow:visible}.takeover-title text{font-family:var(--font),"Noto Sans SC",sans-serif;letter-spacing:-.025em;fill:currentColor}.takeover-support-stage{position:absolute;inset:0;pointer-events:none}.takeover-support-stage p{position:absolute;top:${subTop.toFixed(0)}px;${subBox};font-size:${L.sub}px;line-height:1.25;letter-spacing:-.01em;color:var(--ink);opacity:0;text-wrap:balance}`,
    js:`tl.fromTo('#takeover-title',{scale:.67,opacity:0},{scale:1.035,opacity:1,duration:.23,ease:'expo.out'},.36);
tl.fromTo('#takeover-title',{scale:1.035},{scale:1,duration:.17,ease:'power2.out',immediateRender:false},.59);
tl.set(['#takeover-base','#takeover-subject','#takeover-grade'],{opacity:0},1.8);
tl.set('#takeover-cover',{opacity:1},1.8);
tl.set('#takeover-title',{color:'var(--ink)'},1.8);
tl.fromTo('#takeover-support',{opacity:1,clipPath:'inset(0 100% 0 0)'},{opacity:1,clipPath:'inset(0 0% 0 0)',duration:.27,ease:'power2.out',immediateRender:false},2.08);
`
  };
}
