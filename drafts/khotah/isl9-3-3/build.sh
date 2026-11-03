set -e
D=$(dirname $(readlink -f $0)); K=/home/user/khotta/khotah-skill/.claude/skills/khotah; PY=/tmp/claude-0/-home-user-khotta/f5654d07-49aa-5233-a52c-577789df6918/scratchpad/venv/bin/python
OUT="$D/أكبر_الكبائر_عرض.html"; CFG=$D/khotah.config.json
python3 $K/engine/build_deck.py $D/kabair_slides.py "$OUT" --config $CFG --title "أكبر الكبائر"
$PY $D/fonts.py "$OUT"
python3 $K/engine/build_deck.py $D/kabair_slides.py "$OUT" --config $CFG --title "أكبر الكبائر"
# حذف خطّي Readex Pro وKDigits من المحرّك (لا يُستخدمان هنا)
python3 - "$OUT" <<'P'
import re,sys;p=sys.argv[1];h=open(p,encoding='utf-8').read()
h=re.sub(r"@font-face\s*\{\s*font-family:\s*'(Readex Pro|KDigits)'[^}]*\}","",h);open(p,'w',encoding='utf-8').write(h)
P
ls -la "$OUT"
