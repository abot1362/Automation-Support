// public/service-worker.js

const CACHE_NAME = 'admin-portal-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  'https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css',
  'https://unpkg.com/lucide@latest/dist/lucide.js'
];

// 1. Install Event: Cache the core assets
self.addEventListener('install', event => {
  console.log('Admin Service Worker: Install');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Admin Service Worker: Caching app shell');
        return cache.addAll(urlsToCache);
      })
  );
});

// 2. Fetch Event: Serve cached content when offline
self.addEventListener('fetch', event => {
  // We only handle GET requests
  if (event.request.method !== 'GET') {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }

        // Not in cache - fetch from network
        return fetch(event.request);
      }
    )
  );
});

// 3. Push Event: Handle incoming push notifications
self.addEventListener('push', event => {
  console.log('Admin Service Worker: Push Received.');
  const data = event.data.json();
  const title = data.title || 'Platform Notification';
  const options = {
    body: data.body,
    icon: '/img/icons/admin-192.png',
    badge: '/img/icons/admin-badge.png' // A smaller icon for the notification bar
  };

  event.waitUntil(self.registration.showNotification(title, options));
});
