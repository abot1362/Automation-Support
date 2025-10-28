// user_portal_public/app.js

document.addEventListener('DOMContentLoaded', () => {
    // --- PWA Service Worker Registration ---
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js')
            .then(registration => {
                console.log('User Service Worker registered successfully.');
                // You can add the push notification subscription logic here as well
            })
            .catch(error => {
                console.error('User Service Worker registration failed:', error);
            });
    }
    // ------------------------------------

    // ... your existing navigation and page loading logic ...
});
