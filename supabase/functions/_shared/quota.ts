// حصص استخدام الذكاء الاصطناعي — تُفرض على الخادم (لا يمكن تجاوزها من المتصفح)
// kind: 'text' (خطط/اختبارات/محادثة...) أو 'img' (إنفوجرافيك/شرائح مرسومة)
// الحدود من ai_settings: quota_text (افتراضي 300/شهر) و quota_img (افتراضي 80/شهر)
// المشرف بلا حدود. أي عطل داخلي في نظام الحصص لا يمنع المعلم (fail-open) لكنه يُسجَّل.

const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

async function ensureUsageTable() {
  const dbUrl = Deno.env.get("SUPABASE_DB_URL");
  if (!dbUrl) throw new Error("no SUPABASE_DB_URL");
  const { default: postgres } = await import("https://deno.land/x/postgresjs@v3.4.5/mod.js");
  const sql = postgres(dbUrl, { prepare: false });
  try {
    await sql.unsafe(`
      create table if not exists ai_usage (
        user_id uuid not null,
        month text not null,
        kind text not null,
        count int not null default 0,
        primary key (user_id, month, kind)
      );
      alter table ai_usage enable row level security;
      drop policy if exists "usage_read_own" on ai_usage;
      create policy "usage_read_own" on ai_usage for select to authenticated using (user_id = auth.uid());
    `);
  } finally {
    await sql.end({ timeout: 3 });
  }
}

// deno-lint-ignore no-explicit-any
export async function takeQuota(admin: any, userId: string, email: string, kind: "text" | "img", st: Record<string, string>) {
  if ((email || "").toLowerCase() === ADMIN_EMAIL) return { ok: true, used: 0, limit: 0 };
  const month = new Date().toISOString().slice(0, 7);
  const limit = parseInt(st[kind === "img" ? "quota_img" : "quota_text"] || "") || (kind === "img" ? 80 : 300);

  const attempt = async () => {
    const { data, error } = await admin.from("ai_usage").select("count")
      .eq("user_id", userId).eq("month", month).eq("kind", kind).maybeSingle();
    if (error) throw error;
    const used = data?.count || 0;
    if (used >= limit) return { ok: false, used, limit };
    if (data) {
      const { error: e2 } = await admin.from("ai_usage").update({ count: used + 1 })
        .eq("user_id", userId).eq("month", month).eq("kind", kind);
      if (e2) throw e2;
    } else {
      const { error: e3 } = await admin.from("ai_usage").insert({ user_id: userId, month, kind, count: 1 });
      if (e3) throw e3;
    }
    return { ok: true, used: used + 1, limit };
  };

  try { return await attempt(); }
  catch (e) {
    const msg = String((e as { message?: string })?.message || e);
    if (/does not exist|42P01|schema cache/i.test(msg)) {
      try { await ensureUsageTable(); return await attempt(); }
      catch (e2) { console.error("quota bootstrap failed", e2); return { ok: true, used: 0, limit }; }
    }
    console.error("quota check failed", msg);
    return { ok: true, used: 0, limit };
  }
}
