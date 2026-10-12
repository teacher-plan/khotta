// يحدّد مكان Playwright تلقائياً (محلّي، أو عامّ عبر npm root -g، أو متغيّر البيئة PLAYWRIGHT_MODULE).
// التثبيت إن لم يوجد: npm i -g playwright && npx playwright install chromium
import { execSync } from 'child_process';
const cands = [process.env.PLAYWRIGHT_MODULE, 'playwright'];
try { cands.push(execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim() + '/playwright/index.mjs'); } catch (e) {}
cands.push('/opt/node22/lib/node_modules/playwright/index.mjs', '/usr/local/lib/node_modules/playwright/index.mjs', '/usr/lib/node_modules/playwright/index.mjs');
let m = null;
for (const c of cands) { if (!c) continue; try { m = await import(c); break; } catch (e) {} }
if (!m) { console.error('Playwright غير مثبّت: npm i -g playwright && npx playwright install chromium'); process.exit(2); }
export const chromium = m.chromium || (m.default && m.default.chromium);
