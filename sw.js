// ══ Service Worker - خطتي الفصلية ══
const CACHE_NAME = 'khotta-v3';

self.addEventListener('install', e => { self.skipWaiting(); });

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    // حذف الكاشات القديمة من إصدارات سابقة
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)));
    await clients.claim();
  })());
});

// ═══ استراتيجية التخزين المؤقت (تعمل دون إنترنت + فتح فوري) ═══
// HTML/التنقّل: الشبكة أولاً → تحديثات فورية دائماً، ورجوع للكاش عند انقطاع النت.
// الملفات الثابتة (أيقونات/manifest): الكاش أولاً مع تحديث بالخلفية → فتح فوري.
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
      try {
        const fresh = await fetch(req);
        if (fresh && fresh.ok) {
          const cache = await caches.open(CACHE_NAME);
          cache.put(req, fresh.clone());
        }
        return fresh;
      } catch (err) {
        const cached = await caches.match(req)
          || await caches.match('/index.html')
          || await caches.match('/');
        if (cached) return cached;
        throw err;
      }
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
