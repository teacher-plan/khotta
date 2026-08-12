import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.38.4";

const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
const sb = createClient(supabaseUrl, supabaseServiceKey);

interface GenerateRequest {
  grade: string;
  subject: string;
  lessonNames?: string[];
  bookContext?: string;
  instructions?: string;
  edit?: boolean;
  currentHtml?: string;
  editRequest?: string;
}

async function getAiModel() {
  const { data } = await sb
    .from("ai_settings")
    .select("value")
    .eq("key", "ai_model_worksheet")
    .maybeSingle();
  return data?.value || "google/gemini-2.5-flash-lite";
}

async function invokeOpenRouter(model: string, messages: Array<{role: string, content: string}>) {
  const apiKey = Deno.env.get("OPENROUTER_API_KEY") || "";

  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: 0.7,
      max_tokens: 4000,
    }),
  });

  const data = await response.json();
  if (data.error) throw new Error(data.error.message || "OpenRouter error");
  return data.choices?.[0]?.message?.content || "";
}

serve(async (req: Request) => {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });

  try {
    const { grade, subject, lessonNames = [], bookContext = "", instructions = "", edit = false, currentHtml = "", editRequest = "" } = await req.json() as GenerateRequest;
    const model = await getAiModel();

    if (edit && currentHtml && editRequest) {
      // تعديل ورقة العمل الموجودة
      const prompt = `أنتِ معلمة ذكية. لديك ورقة عمل HTML بالصيغة التالية:
${currentHtml.substring(0, 2000)}

المستخدم يطلب التعديل التالي:
"${editRequest}"

طبّقي التعديل والعودي بكامل HTML المعدّل (ورقة عمل A4 كاملة). يجب أن تكون صحيحة تماماً وجاهزة للطباعة.`;

      const editedHtml = await invokeOpenRouter(model, [
        { role: "user", content: prompt }
      ]);

      // استخراج HTML من الاستجابة إذا كانت مغلفة بـ markdown
      const htmlMatch = editedHtml.match(/```html\n?([\s\S]*?)\n?```/) || editedHtml.match(/```\n?([\s\S]*?)\n?```/);
      const cleanHtml = htmlMatch ? htmlMatch[1] : editedHtml;

      return new Response(JSON.stringify({ html: cleanHtml }), { status: 200 });
    }

    // توليد ورقة عمل جديدة
    const lessonContext = lessonNames.length > 0 ? `الدروس: ${lessonNames.join(", ")}` : "درس عام";

    const prompt = `أنتِ معلمة ذكية في سلطنة عمان. طُلب منك إنشاء ورقة عمل للصف ${grade} في ${subject}.
${lessonContext}
محتوى الدرس: ${bookContext.substring(0, 1500)}
${instructions ? `تعليمات إضافية: ${instructions}` : ""}

تطلب مني إنشاء ورقة عمل A4 قابلة للطباعة (أبيض وأسود فقط) بـ HTML/SVG. يجب أن تحتوي على:
1. عنوان وتاريخ واسم الطالب
2. ٣-٥ أسئلة/أنشطة مناسبة للصف من محتوى الدرس
3. رسومات SVG بسيطة (أشكال هندسية، خطوط للكتابة)
4. مسافات بيضاء كافية للإجابة

أعيدي كود HTML كاملاً بسمات A4 صحيحة، جاهز للطباعة مباشرة. يجب أن يكون بلا أي أخطاء HTML.`;

    const worksheetHtml = await invokeOpenRouter(model, [
      { role: "user", content: prompt }
    ]);

    // استخراج HTML من الاستجابة
    const htmlMatch = worksheetHtml.match(/```html\n?([\s\S]*?)\n?```/) || worksheetHtml.match(/```\n?([\s\S]*?)\n?```/);
    const cleanHtml = htmlMatch ? htmlMatch[1] : worksheetHtml;

    return new Response(JSON.stringify({ html: cleanHtml }), { status: 200 });
  } catch (err) {
    return new Response(
      JSON.stringify({
        error: String(err),
      }),
      { status: 400 }
    );
  }
});
