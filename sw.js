// ══ Service Worker - خطتي الفصلية ══
const CACHE_NAME = 'khotta-551b734'; // يُرقَّى تلقائياً عبر GitHub Actions عند كل نشر

self.addEventListener('install', e => {
  // تجهيز الصفحة الرئيسية في الكاش فور التثبيت — حتى أول فتحة بعد التحديث تكون فورية
  e.waitUntil((async () => {
    try {
      const cache = await caches.open(CACHE_NAME);
      await cache.addAll(['/', '/index.html']);
    } catch (_) { /* اجتهادي */ }
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    // حذف الكاشات القديمة من إصدارات سابقة
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)));
    await clients.claim();
  })());
});

// ═══ استراتيجية التخزين المؤقت (فتح فوري + تحديث بالخلفية) ═══
// HTML/التنقّل: الكاش فوراً (لا شاشة بيضاء أبداً) + جلب النسخة الجديدة بالخلفية
//   للفتحة التالية. سلامة التحديثات مضمونة: كل نشر يرقّي إصدار الكاش تلقائياً
//   (GitHub Actions) فيتجدد كل شيء خلال فتحتين على الأكثر.
// الملفات الثابتة (أيقونات/manifest): الكاش أولاً مع تحديث بالخلفية.
// الطلبات الخارجية (Supabase, Google Fonts): لا تُعترض إطلاقاً → بيانات حيّة دائماً.
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url;
  try { url = new URL(req.url); } catch (_) { return; }
  if (url.origin !== self.location.origin) return; // خارجي → الشبكة كالعادة

  const isHTML = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').includes('text/html');

  // لا نخزّن صفحة إلا بعد قراءتها كاملة والتأكد من سلامتها —
  // يمنع تسميم الكاش بنسخة مبتورة إذا انقطع التنزيل في المنتصف
  const MIN_HTML_BYTES = 200000; // صفحتنا ~1MB؛ أقل من هذا = مبتورة
  const cacheFullHtml = async (request, fresh) => {
    try {
      if (!fresh || !fresh.ok) return;
      const buf = await fresh.clone().arrayBuffer();
      if (buf.byteLength < MIN_HTML_BYTES) return; // مبتورة — لا تُخزَّن
      const c = await caches.open(CACHE_NAME);
      await c.put(request, new Response(buf, { status: 200, headers: fresh.headers }));
    } catch (_) { /* التخزين اجتهادي */ }
  };
  const validCached = async (request) => {
    const hit = await caches.match(request);
    if (!hit) return null;
    try {
      const buf = await hit.clone().arrayBuffer();
      if (buf.byteLength < MIN_HTML_BYTES) {
        (await caches.open(CACHE_NAME)).delete(request); // نسخة فاسدة قديمة — تُحذف
        return null;
      }
      return new Response(buf, { status: 200, headers: hit.headers });
    } catch (_) { return null; }
  };

  if (isHTML) {
    e.respondWith((async () => {
      // التراجع لكاش index مسموح للصفحة الرئيسية فقط — صفحات أخرى (manager/cycle1…) لا تُستبدل بها أبداً
      const isRoot = url.pathname === '/' || url.pathname === '/index.html';
      const cached = await validCached(req)
        || (isRoot ? (await validCached('/index.html') || await validCached('/')) : null);
      // تحديث بالخلفية دائماً (لا ننتظره)
      const refresh = fetch(req).then(fresh => {
        cacheFullHtml(req, fresh);
        return fresh;
      }).catch(() => cached);
      if (cached) return cached;       // ⚡ فتح فوري من كاش سليم مؤكد
      return refresh;                   // لا كاش سليم؟ من الشبكة
    })());
    return;
  }

  // ملفات ثابتة: كاش أولاً + تحديث بالخلفية
  e.respondWith((async () => {
    const cached = await caches.match(req);
    const fetchPromise = fetch(req).then(resp => {
      if (resp && resp.ok) caches.open(CACHE_NAME).then(c => c.put(req, resp.clone()));
      return resp;
    }).catch(() => cached);
    return cached || fetchPromise;
  })());
});

// ═══ استقبال Push من السيرفر ═══
self.addEventListener('push', e => {
  if (!e.data) return;
  let data = {};
  try { data = e.data.json(); } catch { data = { title: 'خطتي الفصلية', body: e.data.text() }; }

  e.waitUntil(
    self.registration.showNotification(data.title || 'خطتي الفصلية 📚', {
      body: data.body || '',
      icon: '/khottah_icon_192.png',
      badge: '/khottah_icon_192.png',
      dir: 'rtl',
      lang: 'ar',
      tag: data.tag || 'khotta',
      renotify: true,
      data: { url: 'https://khotati.com/' }
    })
  );
});

// ═══ إشعارات محلية من الصفحة ═══
self.addEventListener('message', e => {
  if (e.data?.type === 'SHOW_NOTIFICATION') {
    self.registration.showNotification(e.data.title, {
      body: e.data.body,
      dir: 'rtl', lang: 'ar',
      tag: e.data.tag || 'khotta',
      icon: '/khottah_icon_192.png',
      data: { url: 'https://khotati.com/' }
    });
  }
});

// ═══ فتح الموقع عند الضغط على الإشعار ═══
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = e.notification.data?.url || 'https://khotati.com/';
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      for (const c of list) {
        if (c.url.includes('khotati.com') && 'focus' in c) return c.focus();
      }
      if (clients.openWindow) return clients.openWindow(url);
    })
  );
});
