// عميل HTTP لمنصّة نور (Classera — lms.moe.gov.om) بلا متصفّح.
// يحاكي ما يرسله نموذج الموقع نفسه: تسجيل الدخول، قائمة المقرّرات وشُعَبها،
// شجرة الدروس، حصص يومٍ معيّن، نشر تحضير، رفع ملفٍّ مرفق بتحضير.
// يعمل في Deno (الدالّة) وفي Node 22 (اختبارٌ محلّي) — أنواعٌ فقط، بلا مكتبات.

export const BASE = "https://lms.moe.gov.om";
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36";

export type Jar = Record<string, string>;
export type Course = { cid: string; enc: string; name: string; sections: { id: string; label: string }[] };
export type Slot = { lts: string; timeslot: string; section: string; period: string; has_prep: boolean };

export class NoorError extends Error {
  code: string;
  constructor(code: string, msg?: string) { super(msg || code); this.code = code; }
}

function decodeEntities(s: string): string {
  return s.replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#039;|&#39;/g, "'")
    .replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n));
}
const clean = (s: string) => decodeEntities(s.replace(/<[^>]*>/g, " ")).replace(/\s+/g, " ").trim();

// تطبيعٌ للمطابقة بين اسم الدرس في خطة واسمه في نور: بلا تشكيلٍ ولا شدّة ولا مسافات،
// وبأرقامٍ لاتينية، وتوحيد الهمزات والتاء المربوطة والألف المقصورة.
export function normName(s: string): string {
  return String(s || "")
    .replace(/[ً-ْٰـ]/g, "")
    .replace(/[٠-٩]/g, (d) => String("٠١٢٣٤٥٦٧٨٩".indexOf(d)))
    .replace(/[أإآ]/g, "ا").replace(/ة/g, "ه").replace(/ى/g, "ي")
    .replace(/[^\p{L}\p{N}]+/gu, "");
}

export class Noor {
  jar: Jar;
  constructor(jar?: Jar) { this.jar = { ...(jar || {}) }; }

  private eat(h: Headers) {
    // deno-lint-ignore no-explicit-any
    const list: string[] = (h as any).getSetCookie ? (h as any).getSetCookie() : [];
    for (const c of list) {
      const kv = c.split(";")[0];
      const i = kv.indexOf("=");
      if (i < 1) continue;
      const k = kv.slice(0, i).trim(), v = kv.slice(i + 1);
      if (v === "deleted" || /max-age=0|expires=thu, 01 jan 1970/i.test(c)) delete this.jar[k];
      else this.jar[k] = v;
    }
  }
  private cookie() { return Object.entries(this.jar).map(([k, v]) => `${k}=${v}`).join("; "); }

  async req(path: string, o: { method?: string; body?: BodyInit; headers?: Record<string, string>; ajax?: boolean; anon?: boolean } = {}) {
    let url = path.startsWith("http") ? path : BASE + path;
    let method = o.method || "GET";
    let body = o.body;
    for (let i = 0; i < 8; i++) {
      const headers: Record<string, string> = { cookie: this.cookie(), "user-agent": UA, "accept-language": "ar", ...(o.headers || {}) };
      if (o.ajax) headers["x-requested-with"] = "XMLHttpRequest";
      if (method !== "GET") { headers.origin = BASE; headers.referer = url; }
      const r = await fetch(url, { method, body, redirect: "manual", headers });
      this.eat(r.headers);
      if (r.status >= 300 && r.status < 400 && r.headers.get("location")) {
        await r.body?.cancel();
        url = new URL(r.headers.get("location")!, url).href;
        method = "GET"; body = undefined;
        if (o.headers) { const { "content-type": _c, ...rest } = o.headers; o = { ...o, headers: rest }; }
        continue;
      }
      const text = await r.text();
      if (!o.anon && /\/users\/login/.test(url)) throw new NoorError("session_expired");
      return { status: r.status, url, text };
    }
    throw new NoorError("redirect_loop");
  }

  async login(username: string, password: string) {
    this.jar = {};
    await this.req("/", { anon: true });
    const r = await this.req("/users/login", {
      method: "POST", anon: true,
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ _method: "POST", "data[Token][csrf_token]": "", "data[User][username]": username, "data[User][password]": password }).toString(),
    });
    if (/\/users\/login/.test(r.url) || r.url.replace(/[#?].*$/, "") === BASE + "/") {
      if (/recaptcha/i.test(r.text) && /يرجى التحقق|verify you are/i.test(r.text)) throw new NoorError("captcha");
      throw new NoorError("bad_credentials");
    }
    if (!/\/teacher/.test(r.url)) throw new NoorError("not_teacher", r.url);
    return r;
  }

  async logout() { try { await this.req("/users/logout", { anon: true }); } catch { /* */ } }

  async alive(): Promise<boolean> {
    try { const r = await this.req("/teacher"); return /\/teacher/.test(r.url); } catch { return false; }
  }

  // ── المقرّرات وشُعَبها ──
  async courses(): Promise<Course[]> {
    const r = await this.req("/teacher/lectures/teachersCoursesListTitles", { ajax: true });
    // deno-lint-ignore no-explicit-any
    let j: any = {};
    try { j = JSON.parse(r.text || "{}"); } catch { j = {}; }
    const out: Course[] = [];
    for (const x of (j.courses || [])) {
      const v = x?.LectureDetailsView || {};
      const cid = String(v.course_id || "");
      if (!cid || out.some((c) => c.cid === cid)) continue;
      out.push({ cid, enc: "", name: clean(`${v.course_title || ""} / ${v.level_title || ""}`), sections: [] });
    }
    for (const c of out) {
      try { Object.assign(c, await this.courseInfo(c.cid)); } catch { /* يُكمل لاحقاً */ }
    }
    return out;
  }

  async courseInfo(cid: string): Promise<{ enc: string; sections: { id: string; label: string }[] }> {
    const r = await this.req(`/teacher/attachments/upload/Material/cid:${cid}`);
    const enc = (r.text.match(/cid:([A-Za-z0-9_\-]+_OMAN)/) || [])[1] || "";
    const sections: { id: string; label: string }[] = [];
    for (const m of r.text.matchAll(/<input type="checkbox" name="data\[Lecture\]\[checkbox\]\[(\d+)\]"[^>]*>([\s\S]{0,300}?)<\/label>/g)) {
      if (sections.some((s) => s.id === m[1])) continue;
      sections.push({ id: m[1], label: clean(m[2]) });
    }
    if (!sections.length) {
      for (const m of r.text.matchAll(/id="checkbox_(\d+)"[\s\S]{0,300}?<\/label>/g)) {
        if (sections.some((s) => s.id === m[1])) continue;
        const lab = (r.text.match(new RegExp(`for="checkbox_${m[1]}"[^>]*>([\\s\\S]{0,200}?)</label>`)) || [])[1] || "";
        sections.push({ id: m[1], label: clean(lab) || m[1] });
      }
    }
    return { enc, sections };
  }

  // ── شجرة الدروس ──
  async semesters(enc: string): Promise<{ id: string; name: string }[]> {
    const r = await this.req(`/teacher/courses/add_preparation/cid:${enc}`);
    const out: { id: string; name: string }[] = [];
    for (const m of r.text.matchAll(/node_id=\s*(\d+)\s*>([^<]+)</g)) {
      const name = clean(m[2]);
      if (/عرض الشجرة/.test(name)) continue;
      out.push({ id: m[1], name });
    }
    return out;
  }

  async subNodes(parent: string): Promise<{ id: string; name: string }[]> {
    const r = await this.req("/schadmin/nodes/get_sub_nodes", {
      method: "POST", ajax: true,
      headers: { "content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
      body: `parent_node_id=${encodeURIComponent(parent)}&custom_lessons=`,
    });
    let j: Record<string, string> = {};
    try { j = JSON.parse(r.text || "{}") || {}; } catch { j = {}; }
    if (Array.isArray(j)) return [];
    return Object.entries(j).map(([id, name]) => ({ id, name: clean(String(name)) }));
  }

  async criteria(lessonId: string): Promise<{ id: string; text: string }[]> {
    const r = await this.req(`/teacher/nodes/get_associated_criteria?id=${encodeURIComponent(lessonId)}&_=${Date.now()}`, { ajax: true });
    let j: Record<string, string> = {};
    try { j = JSON.parse(r.text || "{}") || {}; } catch { j = {}; }
    if (Array.isArray(j)) return [];
    return Object.entries(j).map(([id, text]) => ({ id, text: clean(String(text)) }));
  }

  // ── حصص يوم ──
  async slots(cid: string, date: string): Promise<Slot[]> {
    const r = await this.req("/teacher/timeslots/ajaxSelectLectureTimeslotsByDate", {
      method: "POST", ajax: true,
      headers: { "content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
      body: `date=${date}&cid=${cid}&pub=${date}`,
    });
    // deno-lint-ignore no-explicit-any
    let j: any = {};
    try { j = JSON.parse(r.text || "{}"); } catch { j = {}; }
    // deno-lint-ignore no-explicit-any
    const arr: any[] = j.timeslots || j.data || (Array.isArray(j) ? j : []);
    return arr.map((t) => ({
      lts: String(t?.LecturesTimeslot?.id || ""),
      timeslot: String(t?.LecturesTimeslot?.timeslot_id || t?.Timeslot?.id || ""),
      section: clean(String(t?.LecturesTimeslot?.section_title || "")),
      period: clean(String(t?.Timeslot?.title || "")),
      has_prep: !!(t?.LecturesTimeslot?.has_preparation && t.LecturesTimeslot.has_preparation !== "0"),
    })).filter((s) => s.lts && s.timeslot);
  }

  // ── التحاضير الموجودة (من صفحة رفع الملفات) ──
  async preps(cid: string): Promise<{ id: string; title: string }[]> {
    const r = await this.req(`/teacher/attachments/upload/Material/cid:${cid}`);
    const i = r.text.indexOf('id="prep_title"');
    if (i < 0) return [];
    const block = r.text.slice(i, r.text.indexOf("</select>", i));
    return [...block.matchAll(/<option value="(\d+)"[^>]*>([^<]*)</g)].map((m) => ({ id: m[1], title: clean(m[2]) }));
  }

  // ── نشر تحضير ──
  async publishPrep(p: {
    enc: string; lessonId: string; title: string; date: string; weekId?: string;
    slots: { lts: string; timeslot: string }[]; criteria: string[];
    taxonomy: string[]; strategies: string[]; aids: string[];
    fields: Record<string, string>; // objective, lesson_vocabulary, description, pre_learning, thinking_skills, activities, formative_assessment, closing_assessment, weekly_study_plan_comments
  }) {
    const page = await this.req(`/teacher/courses/add_preparation/cid:${p.enc}`);
    const csrf = (page.text.match(/name="data\[Token\]\[csrf_token\]"[^>]*value="([^"]+)"/) || [])[1] || "";
    let week = p.weekId || "";
    if (!week) {
      for (const m of page.text.matchAll(/<option value="(\d+)">[^<]*?(\d{4}-\d{2}-\d{2})[^<]*?(\d{4}-\d{2}-\d{2})\s*<\/option>/g)) {
        if (p.date >= m[2] && p.date <= m[3]) { week = m[1]; break; }
      }
    }
    if (!week) throw new NoorError("no_week", p.date);
    const fd = new FormData();
    const add = (k: string, v: string) => fd.append(k, v);
    add("_method", "POST");
    add("data[Token][csrf_token]", csrf);
    add("data[Preparation][title]", p.title);
    p.criteria.forEach((c) => add(`Preparation[criteria][${c}]`, "1"));
    add("data[Preparation][objective]", p.fields.objective || "");
    add("data[Preparation][taxonomy_id]", "");
    p.taxonomy.forEach((t) => add("data[Preparation][taxonomy_id][]", t));
    add("data[Preparation][strategies]", "");
    p.strategies.forEach((t) => add("data[Preparation][strategies][]", t));
    add("data[Preparation][strategies_other]", p.fields.strategies_other || "");
    add("data[Preparation][teaching_aids]", "");
    p.aids.forEach((t) => add("data[Preparation][teaching_aids][]", t));
    add("data[Preparation][teaching_aids_other]", p.fields.teaching_aids_other || "");
    for (const k of ["lesson_vocabulary", "description", "thinking_skills", "formative_assessment", "closing_assessment", "weekly_study_plan_comments"]) {
      add(`data[Preparation][${k}]`, p.fields[k] || "");
    }
    add("data[Preparation][show_in_weekly_study_plan]", "1");
    add("data[Preparation][semester_plan]", "0");
    add("data[Preparation][lesson_id]", p.lessonId);
    add("data[Preparation][pre_learning]", p.fields.pre_learning || "");
    add("data[Preparation][activities]", p.fields.activities || "");
    add("data[Preparation][allowSharePreparations]", "0");
    add("data[plane][date1][publish_date]", p.date);
    add("data[plane][date1][week_id]", week);
    p.slots.forEach((s) => add("data[plane][date1][timeslot][]", s.timeslot));
    add("data[Preparation][global]", "0");
    p.slots.forEach((s) => add("data[plane][date1][lectures_timeslots_id][]", s.lts));
    const r = await this.req(`/teacher/courses/add_preparation/cid:${p.enc}`, { method: "POST", body: fd });
    return { status: r.status, url: r.url, week };
  }

  // ── رفع ملفٍّ مرفق ──
  async uploadFile(p: {
    cid: string; prepId: string; lessonId: string; title: string; comments?: string;
    date: string; sections: string[]; file: Blob; filename: string; criteria?: string[];
  }) {
    const page = await this.req(`/teacher/attachments/upload/Material/cid:${p.cid}`);
    const action = (page.text.match(/<form action="(\/teacher\/attachments\/upload\/Material\/cid:[^"]+)"/) || [])[1];
    if (!action) throw new NoorError("upload_form_missing");
    const csrf = (page.text.match(/name="data\[Token\]\[csrf_token\]"[^>]*value="([^"]+)"/) || [])[1] || "";
    const fd = new FormData();
    const add = (k: string, v: string) => fd.append(k, v);
    add("_method", "POST");
    add("data[Token][csrf_token]", csrf);
    add("data[Attachment][title]", p.title);
    add("data[Attachment][title_cleaned]", p.title);
    add("data[Attachment][comments]", p.comments || "");
    add("data[Attachment][language_id]", "2");
    add("data[Attachment][upload_from]", "2");
    fd.append("data[UploadedFile][file][]", p.file, p.filename);
    add("data[Base64Image][file]", "");
    add("data[Attachment][allow_download]", "1");
    add("data[Attachment][publish_date]", p.date);
    add("data[Attachment][preparation_id]", "");
    add("data[Attachment][preparation_id][]", p.prepId);
    add("data[Attachment][lessons]", "");
    add("data[Attachment][lessons][]", p.lessonId);
    add("data[Attachment][ibooks_checkbox]", "0");
    add("data[Attachment][timeline_sharing]", "0");
    add("data[Attachment][sharing_status]", "1");
    add("data[Tags][tags]", "");
    add("data[Attachment][lesson_id]", "");
    add("data[Attachment][criterion_id]", "");
    (p.criteria || []).forEach((c) => add("data[Attachment][criterion_id][]", c));
    add("data[publish_to]", "0");
    for (const s of p.sections) add(`data[Lecture][checkbox][${s}]`, "1");
    add("data[Attachment][tier]", "0");
    const r = await this.req(action, { method: "POST", body: fd });
    const ok = /تم حفظ الملف|تم رفع|successfully/i.test(r.text);
    const err = /يجب رفع ملف/.test(r.text) ? "no_file" : "";
    return { ok, err, status: r.status, url: r.url };
  }
}
