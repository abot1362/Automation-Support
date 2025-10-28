// public/service-worker.js
const CACHE_NAME = 'admin-portal-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/login.html',
  'https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css',
  'https://unpkg.com/lucide@latest/dist/lucide.js'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('Admin Service Worker: Caching app shell');
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('activate', event => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET' || event.request.url.startsWith('http://') ) {
    return;
  }
  
  if (event.request.url.includes('/api/')) {
    event.respondWith(
        fetch(event.request).catch(() => {
            return new Response(JSON.stringify({ error: "Offline. Could not fetch API data." }), {
                headers: { 'Content-Type': 'application/json' }
            });
        })
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});

self.addEventListener('push', event => {
  const data = event.data.json();
  const title = data.title || 'Platform Alert';
  const options = {
    body: data.body,
    icon: '/img/icons/admin-192.png'
  };
  event.waitUntil(self.registration.showNotification(title, options));
});
