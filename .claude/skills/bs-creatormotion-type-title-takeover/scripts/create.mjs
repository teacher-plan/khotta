import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createComposition} from './builder.mjs';
import {resolveImageAssets,recordImageAssets} from './image-assets.mjs';
import {resolvePresenterMatte} from './presenter-matte.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const packageRoot=path.resolve(here,'..');
const help=`CreatorMotion: create one editable video project for one effect.

  node scripts/create.mjs [--skill bs-creatormotion-EFFECT] --out PATH [--data content.json]
    [--style white-yellow|charcoal-lime|midnight-ice] [--aspect 16:9|9:16|4:3|3:4]
    [--resolution 4k|2k|1080p] [--media presenter.mp4] [--focus x,y]
    [--images images.json] [--overrides style.json] [--font custom-font.woff2]
    [--zh-font smiley-sans|noto-sans-sc] [--matte auto|off|presenter-matte.webm]

--skill picks the effect in the complete bundle (a bs-creatormotion-* name or its short bs-* alias);
a single-effect Skill builds its own effect without it. --aspect defaults to 16:9 and --resolution to 4k
(short side 2160; 2k = 1440, 1080p = 1080). --focus is the presenter's face centre in the footage as
x,y fractions of the frame. midnight-ice selects Black & White. Smiley Sans sets all text;
--zh-font noto-sans-sc switches Chinese content to Noto Sans SC, and --font always wins. --matte applies only to the six presenter-cutout
effects: auto (default) cuts the presenter out of --media with HyperFrames remove-background,
off disables that, and a file path supplies an existing cutout. Other effects ignore it.`;
const args=process.argv.slice(2), options={};
for(let i=0;i<args.length;i++){
  if(args[i]==='--help'){console.log(help);process.exit(0);}
  if(!args[i].startsWith('--')||args[i+1]===undefined)throw new Error('Expected --option value. Run with --help.');
  options[args[i].slice(2)]=args[++i];
}
const config=JSON.parse(await fs.readFile(path.join(packageRoot,'references/entry.json'),'utf8'));
const requested=options.skill||config.slug;
// Accept the public child name or its short bs-CATEGORY-EFFECT alias.
const slug=requested&&requested.startsWith('bs-')&&!requested.startsWith('bs-creatormotion-')?`bs-creatormotion-${requested.slice(3)}`:requested;
if(!config.allowed.includes(slug))throw new Error(`Unknown CreatorMotion effect: ${requested||'(none)'}. Pass --skill with a bs-creatormotion-* name from references/catalog.md.`);
if(!options.out)throw new Error('--out PATH is required. The output directory contains the editable composition.');
const effect=await import(pathToFileURL(path.join(here,'effects',slug+'.mjs')));
const jsonFile=async file=>file?JSON.parse(await fs.readFile(file,'utf8')):{};
const imageResolution=await resolveImageAssets({manifestPath:path.join(packageRoot,'references/default-images/manifest.json'),slug,userImagesPath:options.images});
// The bundle maps each effect to its cutout policy; a single-effect Skill stores its own policy as a string.
const mattePolicy=typeof config.presenterMatte==='string'?config.presenterMatte:config.presenterMatte?.[slug];
await resolvePresenterMatte({policy:mattePolicy,matteOption:options.matte||'auto',media:options.media,imageResolution});
const result=await createComposition({effect,out:options.out,assets:path.join(packageRoot,'references/runtime-assets'),style:options.style||'white-yellow',aspect:options.aspect||'16:9',focus:options.focus,resolution:(options.resolution||'4k').toLowerCase(),data:await jsonFile(options.data),media:options.media,images:imageResolution.images,overrides:await jsonFile(options.overrides),fontFile:options.font,zhFont:options['zh-font']||'smiley-sans',designPath:path.join(packageRoot,'references/DESIGN.md'),skillPath:path.join(packageRoot,'SKILL.md')});
result.imageAssets=await recordImageAssets(result.out,imageResolution);
// Record the bundle that built the project; build.json already names the effect in "slug".
if(config.allowed.length>1){
  const buildPath=path.join(result.out,'build.json');
  await fs.writeFile(buildPath,JSON.stringify({...JSON.parse(await fs.readFile(buildPath,'utf8')),masterSkill:'bs-creatormotion'},null,2)+'\n');
  result.masterSkill='bs-creatormotion';
}
console.log(JSON.stringify(result,null,2));
console.log(`Render: npx --yes hyperframes@0.8.30 render ${JSON.stringify(result.out)} --fps 30 --quality high --strict --output ${JSON.stringify(path.join(result.out,'output.mp4'))}`);
