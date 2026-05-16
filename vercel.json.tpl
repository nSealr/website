{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "astro",
  "buildCommand": "pnpm run build",
  "installCommand": "pnpm install --frozen-lockfile",
  "outputDirectory": "dist",
  "redirects": [
    { "source": "/system",  "destination": "/docs/system/product-shape/",   "permanent": false },
    { "source": "/system/", "destination": "/docs/system/product-shape/",   "permanent": false },
    { "source": "/security",  "destination": "/docs/security/trust-boundaries/", "permanent": false },
    { "source": "/security/", "destination": "/docs/security/trust-boundaries/", "permanent": false }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Content-Security-Policy",
          "value": "default-src 'self'; img-src 'self' data:; font-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval' 'unsafe-eval'; worker-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'none'" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), interest-cohort=()" },
        { "key": "Cache-Control", "value": "no-store, must-revalidate" }
      ]
    },
    {
      "source": "/_astro/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    },
    {
      "source": "/fonts/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    },
    {
      "source": "/favicon.svg",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=604800" }]
    },
    {
      "source": "/favicon.png",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=604800" }]
    },
    {
      "source": "/favicon-180.png",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=604800" }]
    },
    {
      "source": "/og-default.png",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=604800" }]
    },
    {
      "source": "/og/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=604800" }]
    },
    {
      "source": "/pagefind/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=3600" }]
    }
  ]
}
