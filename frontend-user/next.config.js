/** @type {import('next').NextConfig} */

const withPWA = require('next-pwa')({
  dest: 'public',
  // ... other PWA options
});

const nextConfig = {
  reactStrictMode: true,

  // Note the different API prefix '/api/portal'
  async rewrites() {
    return [
      {
        source: '/api/portal/:path*',
        destination: 'http://localhost:8000/api/portal/:path*', // URL of your FastAPI backend
      },
    ];
  },
};

module.exports = withPWA(nextConfig);
