// ══ Service Worker - خطتي الفصلية ══
const CACHE_NAME = 'khotta-42c5b80'; // يُرقَّى تلقائياً عبر GitHub Actions عند كل نشر

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

  if (isHTML) {
    e.respondWith((async () => {
      const cached = await caches.match(req)
        || await caches.match('/index.html')
        || await caches.match('/');
      // تحديث بالخلفية دائماً (لا ننتظره)
      const refresh = fetch(req).then(fresh => {
        if (fresh && fresh.ok) caches.open(CACHE_NAME).then(c => c.put(req, fresh.clone()));
        return fresh;
      }).catch(() => cached);
      if (cached) return cached;       // ⚡ فتح فوري من الكاش
      return refresh;                   // لا كاش بعد؟ من الشبكة
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
