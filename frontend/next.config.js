/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'Referrer-Policy', value: 'no-referrer' },
          { key: 'Permissions-Policy', value: 'geolocation=(), microphone=(), camera=()' },
          { key: 'Cache-Control', value: 'no-store' },
          { key: 'Content-Security-Policy', value: "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self' http://localhost:8000 http://127.0.0.1:8000; frame-ancestors 'none'; base-uri 'self'; form-action 'self'" },
        ],
      },
    ]
  },
  experimental: {
    typedRoutes: false,
  },
}

module.exports = nextConfig
