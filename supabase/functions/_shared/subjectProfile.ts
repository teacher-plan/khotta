// ملفّ المادة: تعليماتٌ خاصة تُلحق بتعليمات النظام حسب المادة.
// اللغة الإنجليزية: كل التعليمات الأصلية مكتوبة بالعربية وتطلب ناتجاً عربياً، فكان التحضير
// واللعبة والإنفوجرافيك للإنجليزية يخرج بالعربية. هنا تعليماتٌ إنجليزية تُضاف في آخر النظام
// وتتقدّم صراحةً على قواعد اللغة والأرقام السابقة.

export function isEnglishSubject(subject: string): boolean {
  return /إنجليزي|انجليزي|الإنكليزي|english/i.test(String(subject || ""));
}

export type ContentTask = "plan" | "game" | "infographic" | "mindmap" | "exam" | "summary" | "chat" | "extract";

const COMMON = [
  "### SUBJECT OVERRIDE — ENGLISH LANGUAGE (these rules take precedence over ANY earlier rule about language, script or numerals)",
  "The subject is English as a second language, taught in Omani state schools with the Ministry's customised Cambridge/Pearson series «Team Together Oman» (Class Book + Activity Book + Teacher's Book), benchmarked to the Global Scale of English (GSE) and CEFR (Pre-A1 to A2; Grade 5 is around A1, preparing for A1 Movers).",
  "Write ALL lesson content in clear, simple English exactly as the book uses it: target words, phrases, grammar patterns, instructions, questions, answers, examples, dialogues. Never translate the lesson content into Arabic.",
  "Arabic is allowed ONLY for short glosses of new words (e.g. a vocabulary item's meaning) or a brief note to the teacher where a field explicitly asks for a translation. Keep JSON keys exactly as given.",
  "Use Western digits 0-9 everywhere (not Arabic-Indic digits). Left-to-right English text.",
  "Stay strictly inside the lesson's actual content from the book pages / teacher's guide provided: its vocabulary set, grammar structure, story characters (e.g. the Discovery Team: Sami, Fatma, Lottie, Bo), songs, audio track numbers, and activities. Do not introduce vocabulary or grammar from other units.",
  "Language level: short sentences and high-frequency words suitable for 10–11-year-old A1 learners; model sentences must follow the unit's target structure.",
].join("\n");

// نوع الدرس من اسمه في المنهج (Lesson 1: Vocabulary …، Story، Grammar …)
const LESSON_TYPES = [
  "Lesson types in Team Together (detect from the lesson title and pages):",
  "- Vocabulary: present new words with pictures/flashcards and audio (Listen, point and repeat), drill (choral → individual), TPR, then controlled practice and a chant or song.",
  "- Story (Discovery Team): before-you-read prediction, Watch or listen and read, comprehension, act out the story; the story recycles the unit vocabulary and introduces the grammar.",
  "- Grammar: 'Look back!' noticing from the story, the grammar box, controlled practice (choose/complete/match), then freer speaking practice using the structure.",
  "- Vocabulary and Grammar: second word set + second structure, song, personalised speaking.",
  "- Culture + Project: read about cultures around the world and Oman, Find out more video, then a collaborative project with presentation.",
  "- English in action: a functional dialogue (e.g. describing people, asking for a price), pronunciation focus, role-play.",
  "- Skills: Reading (text type, before you read, comprehension, sub-skill tip) / Listening, Speaking and Writing (listening task, speaking task, process writing with a model and a tip).",
  "- Review: recycle unit vocabulary and grammar, self-assessment.",
  "- Get ready for… A1 Movers: exam-style practice of the named Movers part with an exam tip.",
  "- Graded reader: extensive reading — before you read, listen and read, after-you-read tasks, values discussion.",
  "Plan the lesson in the communicative PPP sequence: Warm-up → Presentation → Practice → Production → Wrap-up, about 40 minutes, with classroom language the teacher actually says in English.",
].join("\n");

const TASK: Record<ContentTask, string> = {
  plan: [
    LESSON_TYPES,
    "Fill every field of the JSON in English: outcomes as 'I can …' statements (level = Bloom level in English, e.g. Remember, Understand, Apply, Analyse, Create), strategies, resources (flashcards, audio track numbers, Class Book page, Activity Book page), concepts (target vocabulary and structures), warmup and procedures with the teacher's exact words in English in quotation marks, formative, summative questions with model answers, homework (usually the Activity Book page), tip.",
    "vocabulary: en = the English word/phrase from the lesson, ar = its short Arabic meaning.",
    "misconceptions: typical errors of Arabic-speaking learners for this lesson (pronunciation, spelling, word order, grammar) with a practical fix.",
  ].join("\n"),
  game: [
    "Write every question, option, answer, hint and feedback in English, at A1 level, using ONLY the lesson's target vocabulary and structures (e.g. spelling, matching words to meanings, choosing the correct form of the grammar structure, completing sentences from the story).",
    "No Arabic text in the game content except, if a field explicitly asks for it, a short Arabic gloss.",
  ].join("\n"),
  infographic: [
    "All text that appears in the infographic (titles, labels, examples, captions) must be in English, short and child-friendly, showing the lesson's target words and the grammar pattern with example sentences. Any text drawn in the image must be English with correct spelling.",
  ].join("\n"),
  mindmap: "All node labels in English: the lesson's topic in the centre, branches for vocabulary groups, the grammar structure with an example sentence, the story/text, and the skill of the lesson.",
  exam: "Write all questions, options, instructions and answers in English (A1 level, Team Together style: look and match, read and circle, complete the sentences, listen-style picture tasks described in text, short writing). Test only the target vocabulary and structures of the selected lessons.",
  summary: "Write the summary in English. Quote the exact target words, phrases, grammar examples, story lines, audio track numbers and activity instructions as printed in the book. Do not translate.",
  chat: "When the teacher asks for student-facing material for this English lesson, produce it in English; explanations addressed to the teacher may be in Arabic.",
  extract: "This is an English textbook/teacher's book: keep all extracted lesson content (vocabulary, structures, examples, activity instructions, objectives) in English exactly as printed.",
};

export function subjectRules(subject: string, task: ContentTask): string {
  if (!isEnglishSubject(subject)) return "";
  return `${COMMON}\n${TASK[task]}`;
}

// يُلحق تعليمات المادة في آخر تعليمات النظام (فتتقدّم على ما قبلها)
export function withSubject(system: string, subject: string, task: ContentTask): string {
  const r = subjectRules(subject, task);
  return r ? `${system}\n\n${r}` : system;
}
