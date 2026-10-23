set -e
D=$(dirname $(readlink -f $0)); K=/home/user/khotta/khotah-skill/.claude/skills/khotah; PY=/tmp/claude-0/-home-user-khotta/de3f4663-d30c-5355-8c68-f1594fbdf5d2/scratchpad/pv/bin/python
OUT="$D/المكي_والمدني_عرض.html"; CFG=$D/../../khotah.config.json
python3 $K/engine/build_deck.py $D/makki2_slides.py "$OUT" --config $CFG --title "المكيّ والمدنيّ"
$PY $D/fonts.py "$OUT"
python3 $K/engine/build_deck.py $D/makki2_slides.py "$OUT" --config $CFG --title "المكيّ والمدنيّ"
# حذف خطّي Readex Pro وKDigits من المحرّك (لا يُستخدمان هنا)
python3 - "$OUT" <<'P'
import re,sys;p=sys.argv[1];h=open(p,encoding='utf-8').read()
h=re.sub(r"@font-face\s*\{\s*font-family:\s*'(Readex Pro|KDigits)'[^}]*\}","",h);open(p,'w',encoding='utf-8').write(h)
P
ls -la "$OUT"
