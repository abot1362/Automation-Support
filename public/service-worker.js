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
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache)));
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET' || event.request.url.startsWith('http://') ) {
    return;
  }
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});

self.addEventListener('push', event => {
  const data = event.data.json();
  const title = data.title || 'Platform Alert';
  const options = { body: data.body, icon: '/img/icons/admin-192.png' };
  event.waitUntil(self.registration.showNotification(title, options));
});```

#### **۶. فایل `public/index.html`**
*   **مسیر:** `/public/index.html`

```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unified Management Platform</title>
    <!-- PWA -->
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#336699"/>
    <!-- Styles & Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <script defer src="https://unpkg.com/lucide@latest/dist/lucide.js"></script>
    <style> /* ... (Styles from previous answers) ... */ </style>
</head>
<body>
    <aside> <!-- ... (Full sidebar HTML from previous answers) ... --> </aside>
    <main id="main-content"> <!-- ... (All page sections from previous answers) ... --> </main>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();

            // PWA Service Worker Registration
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(() => console.log('Admin Service Worker Registered'));
            }

            // Your full SPA navigation and loader logic goes here
            // (Full JS code from previous answers)
        });
    </script>
</body>
</html>
