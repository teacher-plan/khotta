// ══ Service Worker - خطتي الفصلية ══
const CACHE_NAME = 'khotta-v1';

self.addEventListener('install', e => {
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(clients.claim());
});

// استقبال إشعار Push
self.addEventListener('push', e => {
  if (!e.data) return;
  try {
    const data = e.data.json();
    const options = {
      body: data.body || '',
      icon: data.icon || '/khotta/icon.png',
      badge: data.badge || '/khotta/icon.png',
      dir: 'rtl',
      lang: 'ar',
      tag: data.tag || 'khotta-notif',
      renotify: true,
      requireInteraction: false,
      data: { url: data.url || 'https://teacher-plan.github.io/khotta/' }
    };
    e.waitUntil(
      self.registration.showNotification(data.title || 'خطتي الفصلية', options)
    );
  } catch (err) {
    // إذا لم يكن JSON، اعرضه كنص عادي
    const text = e.data.text();
    e.waitUntil(
      self.registration.showNotification('خطتي الفصلية 📚', {
        body: text,
        dir: 'rtl',
        lang: 'ar'
      })
    );
  }
});

// عند الضغط على الإشعار - فتح الموقع
self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url)
    ? e.notification.data.url
    : 'https://teacher-plan.github.io/khotta/';
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      // إذا الموقع مفتوح → فعّله
      for (const client of list) {
        if (client.url.includes('khotta') && 'focus' in client) {
          return client.focus();
        }
      }
      // إذا مغلق → افتحه
      if (clients.openWindow) return clients.openWindow(url);
    })
  );
});

// إشعارات محلية (بدون Push Server) - يُشغَّل من الصفحة
self.addEventListener('message', e => {
  if (e.data && e.data.type === 'SHOW_NOTIFICATION') {
    const { title, body, tag } = e.data;
    self.registration.showNotification(title, {
      body,
      dir: 'rtl',
      lang: 'ar',
      tag: tag || 'khotta',
      icon: 'https://teacher-plan.github.io/khotta/favicon.ico',
      badge: 'https://teacher-plan.github.io/khotta/favicon.ico',
      requireInteraction: false,
      data: { url: 'https://teacher-plan.github.io/khotta/' }
    });
  }
});
