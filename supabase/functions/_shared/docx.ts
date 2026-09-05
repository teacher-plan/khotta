// أداة توليد ملف Word بسيط (.docx) لتحضير درسٍ — تنزيلٌ إضافي مريح فقط.
// لا يقلّد أي قالبٍ ورقي: التسليم الفعلي هو نسخ كل قسمٍ من معاينة الشاشة
// إلى حقول منصة نور مباشرة (انظر NOOR_SECTIONS في generate-lesson-prep-guided).
import JSZip from "https://esm.sh/jszip@3.10.1";

function xmlEscape(s: string): string {
  return String(s ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}

export interface PrepSection { heading: string; body: string }

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
