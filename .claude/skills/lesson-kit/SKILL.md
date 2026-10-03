---
name: lesson-kit
description: سير عمل تحضير درس رياضيات (الصف السابع، منهج سلطنة عُمان) للأستاذ عيسى الحارثي — العرض التفاعلي وورقة الملخّص وفيديو التعليق الصوتي وصفحة «تحضير الدرس» ورفعها إلى Drive. استخدمها عند «الدرس التالي» أو طلب درس/وحدة/مراجعة، أو تعديل عروض الدروس وملخّصاتها وفيديوهاتها.
---

# تحضير الدرس (lesson-kit)

المرجع الكامل والمُلزِم: `tools/presentations/GUIDELINES.md` (اقرأه أولاً) و`tools/presentations/DRIVE.md` و`CLAUDE.md`.
هذه المهارة خريطةٌ مختصرة للخطوات، ولمتى أستعين بالمهارات التربوية المثبّتة في `.claude/skills/`.

## الخطوات (لكل درس)
1. **المصادر** (`sources/g7-math/lessons.json`): صفحات كتاب الطالب ودليل المعلم وكتاب النشاط وملخّص «درسي في صفحة».
   أتحقّق من كل إجابات الدليل حسابياً، وأسجّل أخطاء الكتاب أو الدليل لأبلغ عنها.
2. **العرض** `examples/<key>_slides.py` ← `gen_powers.py`. أعتمد أنا ← نحن ← أنتم، وحصصاً من ٤٠ دقيقة، ثم ملحق تمارين الكتابين (`launch` و`ex`).
   الفحص: `ovf.mjs` و`boxovf.mjs` نظيفان، ولقطات `snap.mjs`.
3. **الرسومات** (القسم ٥-ج): صورة كل سؤال مصوّر في الكتابين عبر `FIG()`، ورسومٌ توضيحية من `figs.py` و`vcol.py`.
4. **الملخّص** `gen_<key>_summary.py` (summary2) ← `sheet.mjs`. صفحتان، ومثالٌ محلول لكل فكرة، ولا شَرطة فاصلة.
5. **الفيديو** `gen_<key>_video_dc.py` ← الصوت المصري ← `render.sh`. المدة ٥ إلى ٦ دقائق، ويُرسل في المحادثة.
6. **صفحة التحضير** `kit.py` مع مجلد Drive، ثم أحدّث `DRIVE.md` وصفحة «رفع الكل»، وأحفظ التغييرات وأرفعها إلى المستودع (commit و push).

## متى أستعين بالمهارات المثبّتة
| الحاجة في الدرس | المهارة |
|---|---|
| بطاقات الخروج وأسئلة «أنتم» بخيارات خاطئة من الأخطاء الشائعة | `k12-check-for-understanding`، `hinge-question-designer` |
| تسلسل أنا ← نحن ← أنتم وشرح المعلّم بصوتٍ عالٍ | `explicit-instruction-sequence-builder`، `think-aloud-script-generator` |
| الأمثلة المحلولة في العرض والملخّص والانتقال إلى الحل المستقل | `worked-example-fading-designer`، `worked-example-to-problem-solving-transition-designer`، `self-explanation-prompt-designer` |
| شرائح «انتبه: خطأ شائع» | `erroneous-example-designer`، `error-analysis-protocol` |
| الرسوم التوضيحية وتقليل ازدحام الشرائح | `dual-coding-designer`، `cognitive-load-analyser` |
| التهيئة والإحماء | `lesson-opening-designer`، `retrieval-practice-generator` |
| تدرّج تمارين «تدرّب» والواجب | `practice-problem-sequence-designer`، `interleaving-unit-planner`، `spaced-practice-scheduler` |
| تلميحات متدرّجة لمسائل التفكير | `adaptive-hint-sequence-designer`، `progressive-hint-ladder` |
| مراجعة الوحدة والتقييم الذاتي | `backwards-design-unit-planner`، `metacognitive-prompt-library`، `criterion-referenced-rubric-generator` |
| طلب نسخٍ متمايزة لمستويات الطلاب | `k12-lesson-differentiation`، `differentiation-adapter` |
| تحليل أوراق الطلاب أو اختيار أسلوب التقويم | `gap-analysis-from-student-work`، `formative-assessment-technique-selector` |
| مذكّرة تحضير قصيرة للمعلّم | `k12-lesson-prep` |

قواعد عند استخدامها:
- المحتوى من مرجع المعلم فقط، وما أضيفه من المهارات يُذكر في ملاحظة المعلّم أنه «من خارج المرجع».
- مهارات k12 مبنية على المعايير الأمريكية: آخذ منها الطريقة لا المعايير ولا المحتوى.
- المخرجات بالعربية وتبقى في قالبنا (العرض والملخّص والفيديو)، لا ملفات Word منفصلة إلا إن طُلبت.
