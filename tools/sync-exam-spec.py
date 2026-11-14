#!/usr/bin/env python3
"""ينسخ مواصفات الرياضيات وقواعد الكتابة من exam-khotta-skill إلى دالّة exam-khotta (supabase/functions/exam-khotta/spec.ts)."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(R, 'exam-khotta-skill/.claude/skills/exam-khotta')
spec = json.load(open(os.path.join(S, 'specs/math-5-10.json'), encoding='utf-8'))
writing = open(os.path.join(S, 'guides/WRITING.md'), encoding='utf-8').read()
mathr = open(os.path.join(S, 'subjects/math.md'), encoding='utf-8').read()
out = '''// مولَّد من exam-khotta-skill (specs/math-5-10.json، guides/WRITING.md، subjects/math.md) — لا يُعدَّل يدوياً.
// أعد توليده بعد أي تحديث للمهارة: python3 tools/sync-exam-spec.py
// deno-lint-ignore no-explicit-any
export const SPEC_MATH: any = %s;
export const WRITING = %s;
export const MATH_RULES = %s;
''' % (json.dumps(spec, ensure_ascii=False, indent=1), json.dumps(writing, ensure_ascii=False), json.dumps(mathr, ensure_ascii=False))
open(os.path.join(R, 'supabase/functions/exam-khotta/spec.ts'), 'w', encoding='utf-8').write(out)
print('ok')
