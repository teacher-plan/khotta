// عميل HTTP لمنصّة نور (Classera — lms.moe.gov.om) بلا متصفّح.
// يحاكي ما يرسله نموذج الموقع نفسه: تسجيل الدخول، قائمة المقرّرات وشُعَبها،
// شجرة الدروس، حصص يومٍ معيّن، نشر تحضير، رفع ملفٍّ مرفق بتحضير.
// يعمل في Deno (الدالّة) وفي Node 22 (اختبارٌ محلّي) — أنواعٌ فقط، بلا مكتبات.

export const BASE = "https://lms.moe.gov.om";
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36";

// معرّف تطبيق نور في Microsoft (من صفحة الدخول نفسها: msal clientId)
const NOOR_MS_CLIENT = "fecfb103-b416-464a-96b2-bd19dd058dc6";

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

  // الدخول بالبريد الوزاري (@moe.om): زرّ «البريد الإلكتروني الوزاري» في صفحة نور
  // يأخذ رمز Microsoft (تطبيق نور نفسه) ثم يرسله إلى /users/microsoft_login.
  // نأخذ الرمز هنا بالبريد وكلمة المرور مباشرةً (تدفّق ROPC) ثم نسلك الطريق نفسه.
  async msLogin(email: string, password: string) {
    this.jar = {};
    const t = await fetch("https://login.microsoftonline.com/organizations/oauth2/v2.0/token", {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ client_id: NOOR_MS_CLIENT, grant_type: "password", scope: "User.Read openid profile", username: email, password }).toString(),
    });
    // deno-lint-ignore no-explicit-any
    let j: any = {};
    try { j = await t.json(); } catch { j = {}; }
    if (!j.access_token) {
      const d = String(j.error_description || "");
      const code = (d.match(/AADSTS(\d+)/) || [])[1] || "";
      if (["50126", "50034", "50055", "50057", "50053"].includes(code)) throw new NoorError(code === "50055" ? "ms_pass_expired" : code === "50053" ? "ms_locked" : "bad_credentials", d);
      if (["50076", "50079", "50074", "53003", "50158"].includes(code)) throw new NoorError("ms_mfa", d);
      throw new NoorError("ms_unsupported", d.slice(0, 160) || String(j.error || t.status));
    }
    await this.req("/", { anon: true });
    const r = await this.req("/users/microsoft_login", {
      method: "POST", anon: true,
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ access_token: j.access_token }).toString(),
    });
    if (/\/users\/login/.test(r.url) || r.url.replace(/[#?].*$/, "") === BASE + "/") throw new NoorError("ms_noor_refused");
    if (!/\/teacher/.test(r.url)) throw new NoorError("not_teacher", r.url);
    return r;
  }

  async login(username: string, password: string) {
    if (username.includes("@")) {
      // بعض الحسابات تقبل البريد في نموذج الدخول العادي؛ نجرّب طريق Microsoft أولاً
      // ثم النموذج العادي إن رفض Microsoft الطريقة نفسها (لا كلمة المرور).
      try { return await this.msLogin(username, password); } catch (e) {
        if (!(e instanceof NoorError) || !["ms_unsupported", "ms_noor_refused"].includes(e.code)) throw e;
        try { return await this.formLogin(username, password); } catch { throw e; }
      }
    }
    return await this.formLogin(username, password);
  }

  async formLogin(username: string, password: string) {
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
    date: string; sections: string[]; file: Blob; filename: string; criteria?: string[]; kind?: "Material" | "Scorm";
  }) {
    const kind = p.kind || "Material";
    const page = await this.req(`/teacher/attachments/upload/${kind}/cid:${p.cid}` + (kind === "Scorm" ? "/prep:0" : ""));
    const action = (page.text.match(new RegExp(`<form action="(/teacher/attachments/upload/${kind}/cid:[^"]+)"`)) || [])[1];
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
    if (kind === "Scorm") add("data[Attachment][interactive_lesson_type]", "1"); // ١ = SCORM
    add("data[Base64Image][file]", "");
    if (kind === "Material") add("data[Attachment][allow_download]", "1");
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
  // ── تغيير تاريخ نشر واجبٍ قائم وموعد تسليمه (يُعيد إرسال نموذج التعديل كما هو
  //    بقيمه الحالية كلّها، ولا يغيّر إلا التواريخ — كما يفعل المتصفح تماماً) ──
  async rescheduleHomework(encCid: string, aid: string, publish: string, due: string) {
    const page = await this.req(`/teacher/homeworks/edit/${encCid}/aid:${aid}`);
    const i = page.text.indexOf('id="AssignmentEditForm"');
    if (i < 0) throw new NoorError("homework_form_missing");
    const fs = page.text.lastIndexOf("<form", i);
    const form = page.text.slice(fs, page.text.indexOf("</form>", i));
    const action = decodeEntities((form.match(/action="([^"]+)"/) || [])[1] || "");
    const fd = new FormData();
    const attr = (tag: string, a: string) => { const m = tag.match(new RegExp(`\\s${a}="([^"]*)"`)); return m ? decodeEntities(m[1]) : null; };
    for (const m of form.matchAll(/<(input|select|textarea)\b[^>]*>/g)) {
      const tag = m[0], name = attr(tag, "name");
      if (!name || /disabled/.test(tag)) continue;
      if (m[1] === "input") {
        const type = (attr(tag, "type") || "text").toLowerCase();
        if (type === "submit" || type === "button" || type === "file" || type === "image") continue;
        if ((type === "checkbox" || type === "radio") && !/\schecked/.test(tag)) continue;
        let v = attr(tag, "value") ?? (type === "checkbox" ? "on" : "");
        if (name === "data[Assignment][publishing_datetime]") v = publish;
        if (name === "data[Assignment][due_datetime]" || name === "data[Assignment][cutoff_datetime]") v = due;
        fd.append(name, v);
      } else if (m[1] === "select") {
        const end = form.indexOf("</select>", m.index!);
        const opts = [...form.slice(m.index!, end).matchAll(/<option\b[^>]*>/g)].map((o) => o[0]);
        const sel = opts.filter((o) => /\sselected/.test(o));
        const pick = sel.length ? sel : (/\smultiple/.test(tag) ? [] : opts.slice(0, 1));
        for (const o of pick) fd.append(name, attr(o, "value") ?? "");
      } else {
        const end = form.indexOf("</textarea>", m.index!);
        fd.append(name, decodeEntities(form.slice(m.index! + tag.length, end)));
      }
    }
    fd.append("data[Save]", "قبول التعديلات");
    const r = await this.req(action, { method: "POST", body: fd });
    return { status: r.status, url: r.url };
  }

  // ── واجب منزلي بأسئلة اختيار من متعدد ──
  async createHomework(p: {
    cid: string; title: string; publish: string; due: string; prepId?: string; lessonId?: string; sections: string[];
  }): Promise<string> {
    const page = await this.req(`/teacher/homeworks/create/cid:${p.cid}`);
    const action = (page.text.match(/<form action="(\/teacher\/homeworks\/create\/cid:[^"]+)"[^>]*id="AssignmentCreateForm"/) || [])[1]
      || (page.text.match(/<form action="(\/teacher\/homeworks\/create\/cid:[^"]+)"[^>]*multipart/) || [])[1];
    if (!action) throw new NoorError("homework_form_missing");
    const csrf = (page.text.match(/name="data\[Token\]\[csrf_token\]"[^>]*value="([^"]+)"/) || [])[1] || "";
    const fd = new FormData();
    const add = (k: string, v: string) => fd.append(k, v);
    add("_method", "POST");
    add("data[Token][csrf_token]", csrf);
    add("data[Assignment][title]", p.title);
    add("data[Assignment][type]", "Homework");
    add("data[Assignment][publishing_datetime]", p.publish);
    add("data[Assignment][due_datetime]", p.due);
    add("data[Assignment][cutoff_datetime]", p.due);
    add("data[Assignment][publish_later]", "0");
    add("data[Assignment][preparation_id]", p.prepId || "");
    add("data[Assignment][lessons]", "");
    if (p.lessonId) add("data[Assignment][lessons][]", p.lessonId);
    add("data[Assignment][comments]", "");
    add("data[AssignmentsSetting][map_with_gradebook]", "0");
    add("data[Assignment][enable_password]", "0");
    add("data[Assignment][assignment_password]", "");
    add("data[Assignment][private]", "0");
    add("data[Assignment][private]", "1");
    add("data[Assignment][show_event]", "0");
    add("data[Assignment][share_to_SGQB]", "0");
    add("data[Assignment][share_to_SGQB]", "1");
    add("data[Assignment][share_to_CQB]", "0");
    add("data[Assignment][share_to_CQB]", "1");
    add("data[Assignment][share_to_question_bank_id]", "0");
    add("data[AssignmentsSetting][allow_missed_student_view_answer]", "0");
    add("data[AssignmentsSetting][set_zero_after_cutoff]", "0");
    add("data[Assignment][view_answers_radio]", "view_answers_after_cutoff");
    add("data[Assignment][random_questions]", "0");
    add("data[Assignment][allow_multiple_submissions]", "0");
    add("data[Assignment][max_submissions_allowed]", "1");
    add("data[Assignment][accept_submission_attachment]", "0");
    add("data[Assignment][sub_attach_mark]", "");
    add("data[Assignment][new]", "true");
    add("data[Assignment][hide_score]", "0");
    add("data[Assignment][publish_to]", "0");
    for (const s of p.sections) { add(`data[Lecture][checkbox][${s}]`, "0"); add(`data[Lecture][checkbox][${s}]`, "1"); }
    add("data[Assignment][tier]", "0");
    add("data[Save]", "إضافة");
    const r = await this.req(action, { method: "POST", body: fd });
    if (!/\/questions\/index\//.test(r.url)) throw new NoorError("homework_not_created", r.url);
    return r.url.replace(/#.*$/, "");
  }

  // ══ مختبر نور (حساب المطوّر فقط) — قراءةٌ بحتة، لا تُغيّر شيئاً في نور ══
  // deno-lint-ignore no-explicit-any
  async ajaxJson(path: string): Promise<any> {
    const r = await this.req(path, { ajax: true });
    try { return JSON.parse(r.text || "{}"); } catch { return {}; }
  }

  // صفحة «بطاقتي»: نقاط اليوم والفصل وكل الفصول، والبطاقة، وتاريخ ١٥ يوماً، وأنشط معلّمي المدرسة
  async myScore() {
    const t = (await this.req("/teacher/scores/myscore")).text.replace(/<!--[\s\S]*?-->/g, "");
    const num = (re: RegExp) => +((t.match(re) || [])[1] || "0").replace(/[^\d.]/g, "") || 0;
    const nums = [...t.matchAll(/class="points_card_number">\s*([\d.,]+)/g)].map((m) => +m[1].replace(/,/g, ""));
    const table = (id: string) => {
      const i = t.indexOf(`id="${id}"`);
      if (i < 0) return [] as { d: string; v: number }[];
      const blk = t.slice(i, t.indexOf("</table>", i));
      return [...blk.matchAll(/<td>(\d{4}-\d{2}-\d{2})<\/td>\s*<td>([\d.]+)<\/td>/g)].map((m) => ({ d: m[1], v: +m[2] }));
    };
    const list = (id: string) => {
      const i = t.indexOf(`id="${id}"`);
      if (i < 0) return [] as { name: string; sub: string; pts: number }[];
      const j = t.indexOf('class="tab-pane', i + 80);
      const blk = t.slice(i, j > 0 ? j : i + 30000);
      return [...blk.matchAll(/class="main_text"[^>]*>([\s\S]*?)<\/span>([\s\S]*?)class="sub_text">\s*([\d.]+)/g)]
        .map((m) => ({ name: clean(m[1]), sub: clean((m[2].match(/sub_text_details">([^<]*)/) || [])[1] || ""), pts: +m[3] }));
    };
    const tierMatch = t.match(/class="card_info_Indicator">\s*([^<]+)/);
    return {
      total: num(/class="score_number">\s*([\d.,]+)/),
      today: nums[0] || 0, semester: nums[1] || 0,
      card: tierMatch ? clean(tierMatch[1]) : "",
      cumulative: table("gChart01"), daily: table("gChart02"),
      teachers: list("teachers_in_school"), students: list("students_in_school"),
    };
  }

  async homeworksList(cid: string) {
    const j = await this.ajaxJson(`/teacher/homeworks/index/cid:${cid}?start=0&length=500&draw=1`);
    // deno-lint-ignore no-explicit-any
    return ((j.data || []) as any[]).map((x) => x.Assignment || {}).map((a) => ({
      id: String(a.id || ""), title: clean(String(a.title || "")), q: +a.questions_count || 0,
      publish: String(a.publishing_datetime || ""), due: String(a.due_datetime || ""),
    })).filter((a) => a.id);
  }

  // رموز رابط «متابعة التسليمات» تأتي من صفحة الواجبات نفسها
  async monitorTokens(cid: string) {
    const t = (await this.req(`/teacher/homeworks/index/cid:${cid}`)).text;
    const m = t.match(/\/teacher\/assignments\/monitor\/(cid:[^/"]+)\/aid:%idx%\/(type:[^/"]+)\/(filter:[^/"]+)"/);
    return m ? { cid: m[1], type: m[2], filter: m[3] } : null;
  }

  async submissions(tok: { cid: string; type: string; filter: string }, aid: string) {
    const j = await this.ajaxJson(`/teacher/assignments/monitor/${tok.cid}/aid:${aid}/${tok.type}/${tok.filter}?start=0&length=1000&draw=1`);
    // deno-lint-ignore no-explicit-any
    return ((j.data || []) as any[]).map((x) => x.StudentSubmissionStatus || {}).map((s) => ({
      sid: String(s.std_u_id || s.student_number || ""), name: clean(String(s.full_name || "")), sec: clean(String(s.section_title || "")),
      at: String(s.submission_time || ""), mark: s.submission_mark === "" || s.submission_mark == null ? null : +s.submission_mark,
    }));
  }

  async attachmentsList(cid: string, kind: string) {
    const j = await this.ajaxJson(`/teacher/attachments/index/${kind}/cid:${cid}?start=0&length=500&draw=1`);
    // deno-lint-ignore no-explicit-any
    return ((j.data || []) as any[]).map((x) => x.Attachment || {}).map((a) => ({
      id: String(a.id || ""), title: clean(String(a.title || "")), publish: String(a.publish_date || ""), created: String(a.created || ""),
    })).filter((a) => a.id);
  }

  // قائمة التحاضير المنشورة (مع الشعبة وتاريخ الإنشاء)
  async prepsList(cid: string) {
    const j = await this.ajaxJson(`/teacher/courses/preparations_index/cid:${cid}?start=0&length=500&draw=1`);
    // deno-lint-ignore no-explicit-any
    return ((j.data || []) as any[]).map((x) => ({
      id: String(x?.PreparationsView?.id || ""), title: clean(String(x?.PreparationsView?.title || "")),
      created: String(x?.PreparationsView?.created || ""), lecture: String(x?.PreparationLectures?.lecture_id || ""),
    })).filter((p) => p.id);
  }

  async studentsScores(cid: string) {
    const j = await this.ajaxJson(`/teacher/scores/students_scores/cid:${cid}`);
    // deno-lint-ignore no-explicit-any
    return ((j.data || []) as any[]).map((s) => ({
      sid: String(s.student_user_id || ""), name: clean(String(s.student_full_name || "")), sec: clean(String(s.section_title || "")), score: +s.score || 0,
    }));
  }

  async addQuestions(qIndexUrl: string, items: { text: string; choices: string[]; answer: number }[]) {
    const bulk = qIndexUrl.replace("/questions/index/", "/questions/add_bulk_questions/");
    const page = await this.req(bulk);
    const csrf = (page.text.match(/name="data\[Token\]\[csrf_token\]"[^>]*value="([^"]+)"/) || [])[1] || "";
    const esc = (t: string) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const P = (t: string) => `<p dir="rtl">${esc(t)}</p>`;
    const f = new URLSearchParams();
    f.append("_method", "POST");
    f.append("data[Token][csrf_token]", csrf);
    items.forEach((q, i) => {
      f.append(`data[type][${i}]`, "mcq");
      f.append(`data[mark][${i}]`, "1");
      f.append(`data[text][${i}]`, P(q.text));
      f.append(`data[correct_answer][${i}]`, String(q.answer));
      f.append(`data[number_of_choices][${i}]`, String(q.choices.length));
      for (let j = 1; j <= 6; j++) f.append(`data[option][${i}][${j}]`, q.choices[j - 1] != null ? P(q.choices[j - 1]) : "");
    });
    f.append("data[Question][number]", "");
    f.append("data[Question][sub-text]", "");
    const r = await this.req(bulk, { method: "POST", headers: { "content-type": "application/x-www-form-urlencoded" }, body: f.toString() });
    return { status: r.status, url: r.url, ok: /\/questions\/index\//.test(r.url) };
  }
}

