// Three palettes. Each pairs a base with a light-grey grid and frosted-glass surfaces.
export const themes = {
  'white-yellow': {name:'White & Yellow',bg:'#FAFAF8',surface:'#FFFFFF',ink:'#18201D',muted:'#58615A',accent:'#F4CE36','accent-ink':'#18201D',rule:'#D8DED5',radius:'28px',shadow:'0 8px 24px #18201D08',
    glass:'rgba(255,255,255,.56)','glass-strong':'rgba(255,255,255,.74)','glass-border':'rgba(255,255,255,.9)','glass-edge':'rgba(24,32,29,.07)','glass-hi':'rgba(255,255,255,.95)','glass-shadow':'0 30px 70px -28px rgba(24,32,29,.22)',
    grid:'rgba(24,32,29,.055)','grid-major':'rgba(24,32,29,.085)'},
  'charcoal-lime': {name:'Charcoal & Lime',bg:'#0A0D0B',surface:'#1C211D',ink:'#F6F8EF',muted:'#AEBBAE',accent:'#CAED79','accent-ink':'#18201D',rule:'#39463D',radius:'28px',shadow:'0 8px 24px #00000024',
    glass:'rgba(18,24,20,.58)','glass-strong':'rgba(22,28,24,.74)','glass-border':'rgba(255,255,255,.11)','glass-edge':'rgba(0,0,0,.35)','glass-hi':'rgba(255,255,255,.14)','glass-shadow':'0 40px 90px -30px rgba(0,0,0,.7)',
    grid:'rgba(220,224,220,.06)','grid-major':'rgba(220,224,220,.10)'},
  // Retain the existing style ID so saved commands keep working.
  'midnight-ice': {name:'Black & White',bg:'#09090A',surface:'#1D1D1D',ink:'#F5F5F5',muted:'#ADADAD',accent:'#F0F0F0','accent-ink':'#141414',rule:'#414141',radius:'28px',shadow:'0 8px 24px #00000024',
    glass:'rgba(20,20,22,.58)','glass-strong':'rgba(26,26,28,.74)','glass-border':'rgba(255,255,255,.13)','glass-edge':'rgba(0,0,0,.4)','glass-hi':'rgba(255,255,255,.16)','glass-shadow':'0 40px 90px -30px rgba(0,0,0,.75)',
    grid:'rgba(225,225,225,.06)','grid-major':'rgba(225,225,225,.10)'},
};
export const removedStyles = {'paper-orange':'Paper & Orange was retired in 2.0.0'};
export const darkStyles=new Set(['charcoal-lime','midnight-ice']);

// Canvas sizes at the 1080-short-side design scale; --resolution multiplies them.
export const aspects = {'16:9':[1920,1080],'9:16':[1080,1920],'4:3':[1440,1080],'3:4':[1080,1440]};
export const resolutions = {'1080p':1,'2k':4/3,'4k':2};
// Caption safe area in design pixels. The bottom band belongs to the creator's subtitles (and, on vertical
// platforms, to their caption and button overlays); the top band clears platform UI. Effects keep cards,
// labels and readable text between the two.
export const safeAreas = {'16:9':{top:72,bottom:250},'4:3':{top:64,bottom:250},'9:16':{top:170,bottom:560},'3:4':{top:72,bottom:360}};

const stack=(primary,fallback)=>[...new Set([primary,...fallback])].map(f=>`"${f}"`).join(',');
const tokens=['bg','surface','ink','muted','accent','accent-ink','rule','radius','shadow','font','monoFont','glass','glass-strong','glass-border','glass-edge','glass-hi','glass-shadow','grid','grid-major'];

export function assertStyle(style){
  if(removedStyles[style])throw new Error(`--style ${style}: ${removedStyles[style]}. Choose ${Object.keys(themes).join(', ')}.`);
  if(!themes[style])throw new Error(`Unknown style: ${style}. Choose ${Object.keys(themes).join(', ')}.`);
}

export function themeCSS(style='white-yellow', overrides={}, {cjkFallback=[],width=1920,height=1080,scale=1}={}) {
  assertStyle(style);
  const t={...themes[style],...overrides};
  for(const [key,value] of Object.entries(overrides)) {
    if(!tokens.includes(key)) throw new Error(`Unknown style token: ${key}`);
    if(/[{};<>]/.test(String(value))) throw new Error(`Invalid style token: ${key}`);
  }
  const W=Math.round(width*scale),H=Math.round(height*scale);
  return `:root{${Object.entries(t).filter(([k])=>!['name','nameZh','font','monoFont'].includes(k)).map(([k,v])=>`--${k}:${v}`).join(';')};--font:${stack(t.font||'Smiley Sans',cjkFallback)};--mono:${stack(t.monoFont||'IBM Plex Mono',cjkFallback)};--W:${width}px;--H:${height}px;--blur:30px;--canvas-bg:linear-gradient(90deg,var(--grid-major) 1.5px,transparent 1.5px) center/240px 240px,linear-gradient(var(--grid-major) 1.5px,transparent 1.5px) center/240px 240px,linear-gradient(90deg,var(--grid) 1px,transparent 1px) center/60px 60px,linear-gradient(var(--grid) 1px,transparent 1px) center/60px 60px,var(--bg)}
*{box-sizing:border-box}html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--font),"Smiley Sans","Noto Sans SC",sans-serif;font-weight:400;font-synthesis:none;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
#composition{width:${W}px;height:${H}px;position:relative;overflow:hidden;background:var(--bg)}
#cm-stage{position:absolute;left:0;top:0;width:${width}px;height:${height}px;zoom:${scale};overflow:hidden}
#cm-backdrop{position:absolute;inset:0;overflow:hidden;background:var(--canvas-bg)}
.scene-content{width:100%;height:100%;padding:80px 96px;display:flex;flex-direction:column;gap:24px;box-sizing:border-box}h1,h2,h3,p{margin:0}h1,h2,h3{font-weight:400;letter-spacing:-.01em}svg{overflow:visible}.mono{font-family:var(--mono),monospace;font-variant-numeric:tabular-nums}.eyebrow{font:400 24px/1.3 var(--mono),monospace;text-transform:uppercase;letter-spacing:.09em}.muted{color:var(--muted)}.accent{color:var(--accent)}
.glass{background:linear-gradient(180deg,var(--glass-strong),var(--glass));-webkit-backdrop-filter:blur(var(--blur)) saturate(150%);backdrop-filter:blur(var(--blur)) saturate(150%);border:1.5px solid var(--glass-border);border-radius:var(--radius);box-shadow:inset 0 1.5px 0 var(--glass-hi),0 0 0 1px var(--glass-edge),var(--glass-shadow)}
.accent-panel{background:var(--accent);color:var(--accent-ink)}.rule{height:2px;background:var(--rule)}
`;
}

// The grid is static; glass surfaces blur it, and the presenter plate where one is supplied.
export function backdropHTML(){return '<div id="cm-backdrop" aria-hidden="true"></div>';}
export function backdropJS(){return '';}
