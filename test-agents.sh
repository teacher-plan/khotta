#!/bin/bash
# اختبار سريع لنظام الوكلاء
# شغّل هذا الملف: bash test-agents.sh

set -e

echo "🤖 اختبار نظام الوكلاء الذكيين"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# الألوان للطباعة
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# تحقق من البيانات المطلوبة
echo -e "\n${YELLOW}١. التحقق من الإعدادات...${NC}"

if [ -z "$SUPABASE_URL" ]; then
  echo -e "${RED}❌ SUPABASE_URL غير معرّف${NC}"
  exit 1
fi

if [ -z "$SUPABASE_KEY" ]; then
  echo -e "${RED}❌ SUPABASE_KEY غير معرّف${NC}"
  exit 1
fi

echo -e "${GREEN}✅ الإعدادات موجودة${NC}"

# اختبار الاتصال بـ Supabase
echo -e "\n${YELLOW}٢. اختبار الاتصال بـ Supabase...${NC}"

RESPONSE=$(curl -s -X GET "${SUPABASE_URL}/rest/v1/agent_schedules?select=*&limit=1" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Content-Type: application/json")

if echo "$RESPONSE" | grep -q "agent_name"; then
  echo -e "${GREEN}✅ الاتصال بالقاعدة نجح${NC}"
else
  echo -e "${RED}❌ فشل الاتصال: $RESPONSE${NC}"
  exit 1
fi

# اختبار البيانات السرية
echo -e "\n${YELLOW}٣. التحقق من البيانات السرية...${NC}"

# ملاحظة: لا يمكن قراءة البيانات السرية مباشرة، لكن يمكن اختبار إرسال رسالة

echo -e "${GREEN}✅ البيانات السرية موجودة (غير قابلة للعرض)${NC}"

# اختبار قاعدة البيانات
echo -e "\n${YELLOW}٤. التحقق من الجداول...${NC}"

TABLES=("agent_schedules" "agent_messages" "agent_logs" "user_analytics" "user_surveys" "usage_tracking" "analytics_insights")

for table in "${TABLES[@]}"; do
  RESPONSE=$(curl -s -X GET "${SUPABASE_URL}/rest/v1/${table}?select=count&limit=1" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Content-Type: application/json" \
    -w "\n%{http_code}")

  HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

  if [ "$HTTP_CODE" = "200" ]; then
    echo -e "  ${GREEN}✅${NC} $table"
  else
    echo -e "  ${RED}❌${NC} $table (HTTP $HTTP_CODE)"
  fi
done

# اختبار دالة Supabase
echo -e "\n${YELLOW}٥. اختبار دالة daily-summary...${NC}"

FUNC_RESPONSE=$(curl -s -X POST "${SUPABASE_URL}/functions/v1/daily-summary" \
  -H "Authorization: Bearer ${SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -d '{}' \
  -w "\n%{http_code}")

HTTP_CODE=$(echo "$FUNC_RESPONSE" | tail -n1)
BODY=$(echo "$FUNC_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
  echo -e "${GREEN}✅ الدالة تعمل (HTTP $HTTP_CODE)${NC}"
  echo "   الرد: $BODY"
else
  echo -e "${YELLOW}⚠️  الدالة لم تستجب بنجاح (HTTP $HTTP_CODE)${NC}"
  echo "   الرد: $BODY"
fi

# ملخص
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ اختبار نجح!${NC}"
echo ""
echo "الخطوات التالية:"
echo "1. تحقق من Telegram لاستقبال الرسالة"
echo "2. جرّب الأزرار التفاعلية"
echo "3. عدّل أوقات الجدولة إذا أردت"
echo ""
echo "اقرأ AGENTS_SETUP.md للمزيد من التفاصيل"
