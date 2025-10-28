// user_portal_public/service-worker.js

const CACHE_NAME = 'user-portal-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/style.css',
  '/app.js',
  'https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css',
  'https://unpkg.com/lucide@latest/dist/lucide.js'
];

// 1. Install Event: Cache the core assets
self.addEventListener('install', event => {
  console.log('User Service Worker: Install');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('User Service Worker: Caching app shell');
        return cache.addAll(urlsToCache);
      })
  );
});

// 2. Fetch Event: Serve cached content when offline
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});

// 3. Push Event: Handle incoming push notifications
self.addEventListener('push', event => {
  console.log('User Service Worker: Push Received.');
  const data = event.data.json();
  const title = data.title || 'Portal Notification';
  const options = {
    body: data.body,
    icon: '/img/icons/user-192.png',
    badge: '/img/icons/user-badge.png'
  };

  event.waitUntil(self.registration.showNotification(title, options));
});
