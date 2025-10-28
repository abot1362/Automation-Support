// user_portal_public/service-worker.js
const CACHE_NAME = 'user-portal-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/style.css',
  '/app.js',
  'https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css'
];

self.addEventListener('install', e => e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(urlsToCache))));
self.addEventListener('fetch', e => e.respondWith(caches.match(e.request).then(r => r || fetch(e.request))));
self.addEventListener('push', e => {
  const data = e.data.json();
  const options = { body: data.body, icon: '/img/icons/user-192.png' };
  e.waitUntil(self.registration.showNotification(data.title, options));
});
