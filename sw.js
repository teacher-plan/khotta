// ══ Service Worker - خطتي الفصلية ══
const CACHE_NAME = 'khotta-v2';

self.addEventListener('install', e => { self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(clients.claim()); });

// ═══ استقبال Push من السيرفر ═══
self.addEventListener('push', e => {
  if (!e.data) return;
  let data = {};
  try { data = e.data.json(); } catch { data = { title: 'خطتي الفصلية', body: e.data.text() }; }

  e.waitUntil(
    self.registration.showNotification(data.title || 'خطتي الفصلية 📚', {
      body: data.body || '',
      icon: '/khotta/favicon.ico',
      badge: '/khotta/favicon.ico',
      dir: 'rtl',
      lang: 'ar',
      tag: data.tag || 'khotta',
      renotify: true,
      data: { url: 'https://teacher-plan.github.io/khotta/' }
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
      icon: '/khotta/favicon.ico',
      data: { url: 'https://teacher-plan.github.io/khotta/' }
    });
  }
});

// ═══ فتح الموقع عند الضغط على الإشعار ═══
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = e.notification.data?.url || 'https://teacher-plan.github.io/khotta/';
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      for (const c of list) {
        if (c.url.includes('khotta') && 'focus' in c) return c.focus();
      }
      if (clients.openWindow) return clients.openWindow(url);
    })
  );
});
