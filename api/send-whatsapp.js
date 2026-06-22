export default async function handler(req, res) {
  // فقط POST مسموح
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { phone, name } = req.body;

  // التحقق من البيانات
  if (!phone || !name) {
    return res.status(400).json({ error: 'Missing phone or name' });
  }

  // بيانات Meta API
  const PHONE_NUMBER_ID = '454509567739176';
  const ACCESS_TOKEN = process.env.WHATSAPP_ACCESS_TOKEN; // ستُضاف من Vercel
  const WABA_ID = '357977684074548';

  // الرسالة
  const message = `مرحباً ${name}! 👋

شكراً لتسجيلك في خطتي الفصلية 🎉

نحن سعداء بانضمامك لنا. قريباً جداً ستبدأ رحلتك مع أفضل منظومة تخطيط دراسي للمعلم العُماني.

📅 الإطلاق الرسمي: قريباً جداً
💬 للاستفسارات: تواصل معنا من خلال هذه الرسائل

في الوقت ذاته، يمكنك زيارة موقعنا: https://khotati.com

🌟 أنت الآن في قائمة الأوائل!`;

  try {
    const response = await fetch(
      `https://graph.instagram.com/v18.0/${PHONE_NUMBER_ID}/messages`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${ACCESS_TOKEN}`
        },
        body: JSON.stringify({
          messaging_product: 'whatsapp',
          to: phone,
          type: 'text',
          text: { body: message }
        })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({ error: data.error || 'Failed to send message' });
    }

    return res.status(200).json({ success: true, message_id: data.messages[0].id });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
