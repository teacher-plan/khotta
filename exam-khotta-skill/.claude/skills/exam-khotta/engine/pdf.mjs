// يحوّل صفحة HTML إلى PDF بـ Chromium (Playwright): node pdf.mjs in.html out.pdf
import { chromium } from './pw.mjs';
import { pathToFileURL } from 'url';
const [,, inp, out] = process.argv;
const b = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const p = await b.newPage();
await p.goto(pathToFileURL(inp).href, { waitUntil: 'load' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await b.close();
