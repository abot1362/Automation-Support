/** @type {import('next').NextConfig} */

const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
  // You can add more PWA options here
});

const nextConfig = {
  reactStrictMode: true,

  // This rewrites API calls in development to avoid CORS issues.
  // In production, Nginx or your hosting provider will handle this.
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*', // URL of your FastAPI backend
      },
    ];
  },
};

module.exports = withPWA(nextConfig);
