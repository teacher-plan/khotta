// أدوات مشتركة للتعامل مع ملفات Word (.docx) — قراءة نصّها الخام، وحقن محتوىً
// مولَّد داخل نسخةٍ من القالب المعتمد نفسه (لا إعادة بناء الملف من الصفر)،
// فيخرج التحضير بنفس تنسيق القالب (الخط، الألوان، الجداول) بالضبط.
//
// .docx هو أرشيف ZIP يحوي word/document.xml (المحتوى كـXML). نُعدّل ذلك
// الملف نصّياً (نُدرج فقرات <w:p> جديدة) ونُبقي كل شيءٍ آخر (الأنماط،
// الخطوط، الرأس/التذييل) كما هو تماماً — هذا ما يضمن التطابق الحرفي.
import JSZip from "https://esm.sh/jszip@3.10.1";

export interface DocxParagraph {
  xml: string;   // الفقرة كاملة <w:p ...>...</w:p>
  text: string;  // نصّها المستخرَج (كل <w:t> مُلحَقة)
}

function xmlEscape(s: string): string {
  return String(s ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}

// تطبيعٌ بسيط للمقارنة: يُسقط التشكيل والمسافات الزائدة وعلامات الترقيم
// الشائعة، حتى تُطابَق «أولاً: الأهداف» مع «الأهداف» أو «الأهداف:».
export function normalizeArabic(s: string): string {
  return String(s || "")
    .replace(/[ً-ٰٟ]/g, "")   // تشكيل
    .replace(/[:\-–—.،,]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();
}

// يقتطع كل فقرات <w:p ...>...</w:p> من document.xml بترتيبها.
function splitParagraphs(xml: string): DocxParagraph[] {
  const out: DocxParagraph[] = [];
  const re = /<w:p\b[^>]*>[\s\S]*?<\/w:p>/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(xml))) {
    const pXml = m[0];
    const text = [...pXml.matchAll(/<w:t[^>]*>([\s\S]*?)<\/w:t>/g)].map((t) => t[1]).join("");
    out.push({ xml: pXml, text });
  }
  return out;
}

export async function readDocxBytes(bytes: Uint8Array): Promise<{ zip: JSZip; documentXml: string }> {
  const zip = await JSZip.loadAsync(bytes);
  const docFile = zip.file("word/document.xml");
  if (!docFile) throw new Error("not_a_docx");
  const documentXml = await docFile.async("string");
  return { zip, documentXml };
}

// نصٌّ خام بالفقرات (سطر لكل فقرة) — يُستعمل كمرجع تنسيقٍ نصّي للذكاء
// الاصطناعي عند توليد التحضير (يرى عناوين أقسام القالب وترتيبها).
export function docxPlainText(documentXml: string): string {
  return splitParagraphs(documentXml)
    .map((p) => p.text.trim())
    .filter(Boolean)
    .join("\n");
}

// يبني فقرة Word جديدة تحمل نصّ body (قد يكون عدّة أسطر)، بخصائص فقرةٍ
// (pPr) وخطٍّ (rPr) منسوخة من فقرةٍ مرجعية موجودة أصلاً في القالب — حتى
// يُطابق النصّ المُدرَج نفس اتجاه الكتابة (RTL) والخط والحجم المستخدمَين
// فعلياً في الملف، لا قيماً افتراضية مخمَّنة.
function buildParagraphsFrom(refP: string, lines: string[]): string {
  const pPrM = refP.match(/<w:pPr>[\s\S]*?<\/w:pPr>/);
  const pPr = pPrM ? pPrM[0] : "";
  const rPrM = refP.match(/<w:rPr>[\s\S]*?<\/w:rPr>/);
  const rPr = rPrM ? rPrM[0] : "";
  return lines.filter((l) => l.trim()).map((l) =>
    `<w:p>${pPr}<w:r>${rPr}<w:t xml:space="preserve">${xmlEscape(l)}</w:t></w:r></w:p>`
  ).join("");
}

export interface PrepSection { heading: string; body: string }

// يحقن كل قسمٍ مولَّد بعد فقرة عنوانه المطابقة في القالب. لا يُزال أي شيءٍ
// من القالب الأصلي — فقط إدراجٌ بعد كل عنوانٍ وُجدت له مطابقة. عنوانٌ لم
// يُطابَق يُلحَق في نهاية الملف صراحةً (بدل أن يضيع صامتاً).
export function fillDocxTemplate(documentXml: string, sections: PrepSection[]): { xml: string; unmatched: string[] } {
  const paragraphs = splitParagraphs(documentXml);
  const normParas = paragraphs.map((p) => normalizeArabic(p.text));
  let xml = documentXml;
  const unmatched: string[] = [];

  // من الأخير إلى الأول: الإدراج يُغيّر مواضع النصوص اللاحقة، فالمعالجة
  // العكسية تُبقي مواضع الفقرات السابقة (غير المعالَجة بعد) صحيحة.
  for (let i = sections.length - 1; i >= 0; i--) {
    const s = sections[i];
    const target = normalizeArabic(s.heading);
    if (!target) continue;
    const idx = normParas.findIndex((t) => t && (t.includes(target) || target.includes(t)) && t.length > 1);
    if (idx < 0) { unmatched.unshift(s.heading); continue; }
    const headingP = paragraphs[idx];
    // نمط التنسيق: نسخة من الفقرة التالية إن وُجدت (غالباً سطرٌ فارغٌ
    // مُعَدّ للتعبئة بنفس تنسيق النص العادي)، وإلا فمن فقرة العنوان نفسها.
    const styleRef = paragraphs[idx + 1] ? paragraphs[idx + 1].xml : headingP.xml;
    const inserted = buildParagraphsFrom(styleRef, s.body.split(/\r?\n/));
    const pos = xml.indexOf(headingP.xml);
    if (pos < 0) continue;
    const insertAt = pos + headingP.xml.length;
    xml = xml.slice(0, insertAt) + inserted + xml.slice(insertAt);
  }
  return { xml, unmatched };
}

// يُلحق أقساماً لم تُطابَق أي عنوانٍ في القالب — قبل </w:body> مباشرة —
// بعنوانٍ بارز فوقها، حتى لا يضيع محتوًى وُلِّد فعلاً بصمت.
export function appendUnmatchedSections(documentXml: string, sections: PrepSection[], headings: string[]): string {
  if (!headings.length) return documentXml;
  const extra = sections.filter((s) => headings.includes(s.heading));
  if (!extra.length) return documentXml;
  const bodyClose = documentXml.lastIndexOf("</w:body>");
  if (bodyClose < 0) return documentXml;
  const blocks = extra.map((s) =>
    `<w:p><w:pPr><w:bidi/></w:pPr><w:r><w:rPr><w:b/><w:rtl/></w:rPr><w:t xml:space="preserve">${xmlEscape(s.heading)}</w:t></w:r></w:p>` +
    s.body.split(/\r?\n/).filter((l) => l.trim()).map((l) =>
      `<w:p><w:pPr><w:bidi/></w:pPr><w:r><w:rPr><w:rtl/></w:rPr><w:t xml:space="preserve">${xmlEscape(l)}</w:t></w:r></w:p>`
    ).join("")
  ).join("");
  return documentXml.slice(0, bodyClose) + blocks + documentXml.slice(bodyClose);
}

export async function writeDocxBytes(zip: JSZip, documentXml: string): Promise<Uint8Array> {
  zip.file("word/document.xml", documentXml);
  return await zip.generateAsync({ type: "uint8array" });
}

// بديلٌ عامّ عند غياب قالب Word فعلي (مثلاً القالب المرفوع PDF فقط) —
// مستندٌ بسيط بعناوين غامقة RTL بلا محاولة تقليد تنسيقٍ غير متوفّر لدينا.
export async function buildGenericDocx(title: string, sections: PrepSection[]): Promise<Uint8Array> {
  const paras = [
    `<w:p><w:pPr><w:bidi/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/><w:rtl/><w:sz w:val="32"/></w:rPr><w:t xml:space="preserve">${xmlEscape(title)}</w:t></w:r></w:p>`,
    ...sections.flatMap((s) => [
      `<w:p><w:pPr><w:bidi/></w:pPr><w:r><w:rPr><w:b/><w:rtl/><w:sz w:val="26"/></w:rPr><w:t xml:space="preserve">${xmlEscape(s.heading)}</w:t></w:r></w:p>`,
      ...s.body.split(/\r?\n/).filter((l) => l.trim()).map((l) =>
        `<w:p><w:pPr><w:bidi/></w:pPr><w:r><w:rPr><w:rtl/></w:rPr><w:t xml:space="preserve">${xmlEscape(l)}</w:t></w:r></w:p>`
      ),
    ]),
  ].join("");
  const documentXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>${paras}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/><w:bidi/></w:sectPr></w:body>
</w:document>`;
  const zip = new JSZip();
  zip.file("[Content_Types].xml", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>`);
  zip.file("_rels/.rels", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>`);
  zip.file("word/_rels/document.xml.rels", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>`);
  return await zip.generateAsync({ type: "uint8array" });
}
