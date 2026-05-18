# nSealr Website Redesign — Design Spec

- Date: 2026-05-15
- Owner: vincenzo
- Status: Draft, pending user review
- Supersedes: `docs/site-brief.md` (still authoritative for editorial trust claims),
  `docs/architecture.md` (extended by this spec, not replaced), `docs/information-architecture.md`
  (extended below)

## 1. Goal

Replace the current single-file static site (`public/index.html` + `public/styles.css`)
with a professional, documentation-grade public website that:

1. Stores all editorial content as Markdown / MDX (no copy living in HTML).
2. Adds a real documentation section and a real blog section.
3. Supports a user-controllable light / dark theme with Nostr purple
   (`#8E30EB`) as the predominant color.
4. Deploys to Vercel with one `git push`.
5. Preserves every safety-contract assertion currently enforced by
   `scripts/validate_site.py` and `tests/test_site_validation.py` (no
   regression in trust claims).

The site stays a **non-profit, open-source, pre-production research program**.
No new marketing claims are introduced.

## 2. Non-Goals

- No application backend, auth, CMS, comments system, analytics SDKs.
- No i18n in this iteration. Content is English-only (per user decision
  2026-05-15). The architecture leaves room for future locales but does not
  ship them.
- No newsletter signup, no contact forms, no telemetry.
- No replacement of canonical specs / lab content. The website links to
  `nSealr/specs`, `nSealr/lab`, `nSealr/companion`, etc., it does not
  duplicate them.

## 3. Stack

- **Astro 5** (static `output: 'static'`), TypeScript strict.
- **MDX** via `@astrojs/mdx` for content with inline components.
- **Content collections** (`astro:content`) with Zod schemas for
  `blog`, `docs`, `signers`, `authors`. Build fails on invalid frontmatter.
- **Shiki** for syntax highlighting (dual-theme: `github-dark-dimmed` for
  dark mode, `min-light` for light mode).
- **Pagefind** for static client-side search, built post-`astro build`.
- **`@astrojs/sitemap`**, **`@astrojs/rss`** for sitemap and `/blog/rss.xml`.
- **remark / rehype** plugins: `remark-gfm`, `rehype-autolink-headings`,
  `rehype-slug`, a small custom `remark-callout` for `:::info` / `:::warn`
  / `:::danger`.
- **pnpm** as the package manager. Node 22 LTS.
- **Vercel** as the deploy target; framework preset `astro`.

Astro was already the documented candidate in `docs/architecture.md` and
`README.md`. This spec confirms that choice and rules out Starlight and
Next.js for the reasons recorded in `docs/superpowers/specs/`-internal
discussion (Starlight's preset look fights the chosen visual direction;
Next.js adds runtime/JS overhead unjustified by a static doc/blog site).

## 4. Information Architecture

Top-level routes:

- `/` — home (custom, hero + system map + family grid + status + repo
  strip)
- `/system/` — product shape, five signer families explained
- `/security/` — threat model overview + links into `/docs/security/...`
- `/docs/` — documentation hub (lists sections, redirect default to
  `/docs/getting-started/`)
  - `/docs/getting-started/`
  - `/docs/guides/<slug>/` — build / flash / use guides
  - `/docs/signers/<family>/` — one page per family (raspberry-qr,
    esp32-qr, esp32-usb, smartcard, custom-wallet)
  - `/docs/specs/<slug>/` — reference (request/response, BIP-340 vectors,
    transports, canonicalization)
  - `/docs/security/<slug>/` — threat-model deep dives
- `/blog/` — blog index, category and tag filters (static, no JS)
  - `/blog/<slug>/`
  - `/blog/tags/<tag>/`
  - `/blog/rss.xml`
- `/about/`
- `/contributing/`
- `/404.html`

This extends `docs/information-architecture.md`: the existing top-nav
items (Overview / Use / Build / Security / Developers / Roadmap) map to
home + `/system` + `/docs/guides` + `/security` + `/docs/specs` +
`/docs/signers` respectively. The redesign exposes fewer top-level nav
entries (`System · Docs · Blog · Security`) to reduce surface, with the
remaining sections reachable from inside the docs sidebar.

## 5. Content Model

All content lives under `src/content/`. Schemas live in
`src/content/config.ts`.

### 5.1 `blog`

Path: `src/content/blog/*.mdx`

```ts
{
  title: z.string(),
  description: z.string(),
  publishedAt: z.date(),
  updatedAt: z.date().optional(),
  category: z.enum(['release', 'research', 'tutorial', 'news']),
  tags: z.array(z.string()).default([]),
  authors: z.array(reference('authors')).min(1),
  cover: image().optional(),
  draft: z.boolean().default(false),
}
```

Drafts are excluded from production builds (`import.meta.env.PROD`).

### 5.2 `docs`

Path: `src/content/docs/<section>/*.mdx`, where `section ∈ {
getting-started, guides, signers, specs, security }`.

```ts
{
  title: z.string(),
  description: z.string(),
  section: z.enum(['getting-started', 'guides', 'signers', 'specs', 'security']),
  order: z.number().default(100),
  updatedAt: z.date(),
  status: z.enum(['stable', 'draft', 'research']).default('stable'),
}
```

`section` must match the parent folder; a Zod refinement enforces it.

### 5.3 `signers`

Path: `src/content/signers/*.mdx` — one MDX file per family. Drives both
`/docs/signers/<slug>` and the family grid on `/` and `/system`.

```ts
{
  family: z.enum([
    'raspberry-qr',
    'esp32-qr',
    'esp32-usb',
    'smartcard',
    'custom-wallet',
  ]),
  displayName: z.string(),     // 'Raspberry/Pi Stateless QR Vault', etc.
  tagline: z.string(),
  maturity: z.enum(['research', 'prototype', 'alpha', 'beta']),
  capabilities: z.array(z.object({
    id: z.string(),            // e.g. 'approval_digest', 'signing_disabled'
    status: z.enum(['target', 'present', 'absent', 'disabled']),
    contractId: z.string().optional(),
  })),
  repo: z.string().url(),
  order: z.number(),
}
```

Capabilities mirror `nSealr/specs vectors/features/signer-feature-matrix-v0.json`.
A future task can wire a build step that cross-validates `capabilities`
against the upstream JSON; this spec only requires the schema, not the
cross-check.

### 5.4 `authors`

Path: `src/content/authors/*.yaml`

```ts
{
  name: z.string(),
  bio: z.string().optional(),
  links: z.object({
    github: z.string().url().optional(),
    nostr: z.string().optional(),  // npub
    web: z.string().url().optional(),
  }).default({}),
}
```

## 6. Design System

### 6.1 Typography

- **JetBrains Mono** (variable, self-hosted from `public/fonts/`,
  Latin subset) — headings, code, UI.
- **Inter** (variable, self-hosted, Latin subset) — long-form prose in
  blog posts and doc bodies.
- Sizes: `12, 13, 14, 16, 18, 22, 28, 36, 48, 64`. Display headlines on
  `/` use `clamp(36px, 6vw, 64px)`.
- `font-feature-settings: 'ss01', 'cv11'` on Inter; default ligatures on
  JetBrains Mono.
- Self-hosting (not Google Fonts CDN) because the strict CSP forbids
  third-party font origins.

### 6.2 Palette

Confirmed with user 2026-05-15.

| Token            | Dark value | Light value | Use                            |
|------------------|------------|-------------|--------------------------------|
| `--bg`           | `#07060d`  | `#fbfaff`   | page background                |
| `--bg-elevated`  | `#0f0c17`  | `#f3eefb`   | cards, codeblocks              |
| `--fg`           | `#dcd4f0`  | `#1a132b`   | body text                      |
| `--fg-strong`    | `#ffffff`  | `#0c0814`   | headlines                      |
| `--fg-muted`     | `#7e7393`  | `#5b4f78`   | secondary text                 |
| `--border`       | `#1f1830`  | `#e6def5`   | dividers                       |
| `--accent`       | `#8E30EB`  | `#7c1fd9`   | primary, links, focus ring     |
| `--accent-soft`  | `#b388ff`  | `#9d4bff`   | hover, light accents on dark   |
| `--ok`           | `#7be0a8`  | `#0b8a5c`   | verified pill, success         |
| `--warn`         | `#ff7a90`  | `#c1183c`   | warn / disabled pill           |
| `--pending`      | `#f5c451`  | `#a06c00`   | pending pill                   |

Status colors (`--ok`, `--warn`, `--pending`) keep their semantic meaning
across both themes; only luminance is tuned for contrast.

All tokens defined in `src/styles/tokens.css`; components consume tokens
only (no hardcoded hex outside `tokens.css`).

### 6.3 Theming

- `<html data-theme="dark|light">` is the single switch.
- Blocking inline script in `<head>` (~400 bytes, CSP-hashed) reads
  `localStorage.theme` else `prefers-color-scheme`, sets the attribute
  before first paint → no FOUC.
- `ThemeToggle` component (sun/moon) writes `localStorage.theme` and
  toggles the attribute. `aria-pressed` reflects current state.
- `<meta name="color-scheme" content="dark light">` so native UI
  (scrollbars, form controls) follows the theme.

### 6.4 Prose

In `src/styles/prose.css`, scoped under `.prose`:

- `max-width: 72ch`
- Headings get anchor links via `rehype-autolink-headings` (visible on
  hover / focus, contrast-AA underline)
- Code blocks: Shiki dual-theme, copy button (lazy-loaded ~1 KB)
- Tables: zebra rows, sticky header at `position: sticky; top: 0`
- Callouts: `:::info`, `:::warn`, `:::danger` → `<Callout variant>` with
  left border `--accent` / `--pending` / `--warn`

### 6.5 Motion & a11y

- `prefers-reduced-motion: reduce` disables all transitions / scroll
  effects.
- `:focus-visible` ring: 2px `--accent-soft`, 2px offset.
- Contrast: every `--fg` over `--bg` pair ≥ 7:1 (AAA on body text);
  status pills ≥ 4.5:1 (AA).
- All SVG diagrams keep the `<title>` + `<desc>` pattern from the
  current `SystemMap`.

## 7. Components

In `src/components/`:

- `BaseLayout.astro`, `DocsLayout.astro`, `BlogPostLayout.astro`
- `Header.astro` (brand mark, primary nav, `ThemeToggle`)
- `Footer.astro`
- `Hero.astro` (home)
- `SystemMap.astro` (the existing SVG, ported, dual-theme-aware: uses
  `currentColor` and CSS vars instead of hex)
- `SignerCard.astro`, `SignerFamilyGrid.astro`
- `StatusPill.astro` (variants: `ok`, `warn`, `pending`, `neutral`)
- `Callout.astro` (variants: `info`, `warn`, `danger`)
- `CodeBlock.astro` (wraps Shiki output, adds copy button)
- `DocsSidebar.astro`, `TableOfContents.astro`
- `BlogList.astro`, `TagPill.astro`
- `FeatureMatrix.astro` — MDX-usable component that renders a signer's
  `capabilities` as a table
- `ThemeToggle.astro` (sun/moon button)
- `SearchTrigger.astro` — `⌘K` opens Pagefind UI dialog (modal, focus
  trap, keyboard close)

## 8. Search

Pagefind runs after `astro build`, indexing `dist/` HTML. UI is the
Pagefind default web component, themed via CSS vars to match the
palette. Triggered by `⌘K` / `Ctrl+K` or clicking the search icon in
the header. ~50 KB of JS loaded lazily on first open.

## 9. Validation, testing & CI

### 9.1 Build-time

- `astro check` (TypeScript + content collection schema check).
- `astro build` fails on:
  - missing required frontmatter,
  - unknown `family` / `section` enum value,
  - broken `reference('authors')`,
  - markdown link to a missing internal slug (custom remark plugin).

### 9.2 Required-text validator

`scripts/validate_site.py` is rewritten to scan **the built `dist/`
tree** (not a single hand-written HTML file). The current `REQUIRED_TEXT`
list is partitioned by route:

- `HOME_REQUIRED_TEXT` — must appear on `dist/index.html`. Contains the
  brand and positioning strings (`nSealr`, `open-source`, `non-profit`,
  `Companion`, `Raspberry`, `ESP32`, `Smartcard`, `Hardware`, and the
  five family display names), plus `"No production security claim"`.
- `SIGNERS_REQUIRED_TEXT` — must appear collectively across
  `dist/docs/signers/*.html` (per-family contract phrases like
  `nsealr serial-line exchange`, `T-Display S3 review scenario smoke`,
  `nsealr-smartcard CLI probes`, `Raspberry/Pi OS profile`, etc., each
  asserted against the page for its family).
- `SAFETY_REQUIRED_TEXT` — must appear on `dist/security/index.html`
  and/or in `dist/docs/security/*.html` (`approval_digest`,
  `signing_disabled`, `NIP-46 bridge decisions`, `nsealr nip46 decide`,
  `request-bound capture checks`, `sign-event-disabled smoke`,
  `review detail pages`, `firmware protocol evidence`, `Unicode fallback`).
- `GLOBAL_FORBIDDEN_CLAIMS` — must NOT appear anywhere in `dist/`.

The validator uses the `signers` collection frontmatter as the source
of truth for which family page must contain which contract phrases, so
the assertion list stays in sync with the content. The
`FORBIDDEN_REPOSITORY_LINK_RE` (no legacy GitHub link ending in `/vault`) stays
global.

Adapted assertions in `tests/test_site_validation.py` call the same
functions and assert against the built tree. `make ci` first does
`pnpm run build`, then runs the Python validator.

### 9.3 Other gates

- `lychee` link check on `dist/` (allowlist for `https://github.com/nSealr/*`).
- `html-validate` on `dist/**/*.html`.
- `@axe-core/cli` on home + one docs page + one blog post.
- `lhci` (Lighthouse CI): perf ≥ 95, a11y ≥ 100, best-practices ≥ 95,
  SEO ≥ 100, on home + one docs page.

### 9.4 CI

`.github/workflows/ci.yml`:

```
jobs.build:
  - checkout
  - setup pnpm + node 22
  - pnpm install --frozen-lockfile
  - pnpm exec astro check
  - pnpm run build
  - python scripts/validate_site.py
  - python -m unittest discover -s tests
  - pnpm exec lychee --no-progress dist
  - pnpm exec html-validate dist
  - pnpm exec axe http://localhost:4321 --exit (against `astro preview`)
  - pnpm exec lhci autorun
```

`make ci` becomes a thin wrapper around `pnpm run ci`.

## 10. Deploy (Vercel)

- Framework preset: `astro` (auto-detected; explicit in `vercel.json` for
  determinism).
- `vercel.json`:
  ```json
  {
    "$schema": "https://openapi.vercel.sh/vercel.json",
    "buildCommand": "pnpm run build",
    "outputDirectory": "dist",
    "installCommand": "pnpm install --frozen-lockfile",
    "framework": "astro",
    "headers": [
      {
        "source": "/(.*)",
        "headers": [
          { "key": "Content-Security-Policy",
            "value": "default-src 'self'; img-src 'self' data:; font-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'sha256-<THEME_INIT_HASH>'; frame-ancestors 'none'; base-uri 'self'; form-action 'none'" },
          { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
          { "key": "X-Content-Type-Options", "value": "nosniff" },
          { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
          { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), interest-cohort=()" }
        ]
      },
      {
        "source": "/_astro/(.*)",
        "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
      }
    ],
    "redirects": [
      { "source": "/docs", "destination": "/docs/getting-started", "permanent": false }
    ]
  }
  ```
- Production = push to `main`. Preview deploys on every PR.
- OG images: 1 static default (`public/og-default.png`); for blog posts,
  rendered to PNG at build time with `satori` + `@resvg/resvg-js`
  (pure Node, no edge / serverless runtime needed — site stays 100%
  static).
- Initial domain: `nsealr.vercel.app`. Custom domain attaches later
  without code changes.

## 11. Migration plan (no code in this spec, just sequence)

1. Add Astro scaffold in-place under `website/` (keep `docs/`, `scripts/`,
   `tests/`, `Makefile`, `LICENSE`, `README.md`).
2. Port `public/index.html` copy: the home is a custom page, so the copy
   lives directly in `src/pages/index.astro` and the `<SignerFamilyGrid>`
   it renders. Per-family text from the current `index.html` moves into
   5 `src/content/signers/*.mdx` files. Remove `public/index.html` +
   `public/styles.css` only after the validator passes against `dist/`.
3. Port the SVG system map into `src/components/SystemMap.astro` with
   theme-aware tokens.
4. Author seed docs: 1 getting-started, 1 guide, 5 signer status pages,
   1 spec ref, 1 security page. Author seed blog: 1 release-note post.
5. Rewrite `scripts/validate_site.py` and update `tests/`.
6. Wire CI, lhci, axe, lychee.
7. Add `vercel.json`, connect Vercel project (manual step, user-led).
8. Cut over: delete `public/index.html`.

## 12. Out of scope (explicit)

- CMS / admin UI for editing content (Markdown in repo is the workflow).
- Auth / user accounts.
- Comments on blog posts.
- Analytics.
- Localization beyond English.
- Replacing `nSealr/specs` content; the site only references it.
- A pre-publication public-launch readiness checklist (lives in
  `docs/roadmap.md` M16, untouched).

## 13. Risks & mitigations

- **Validator drift**: porting `validate_site.py` to scan `dist/` could
  miss required text if a page is renamed. Mitigation: the per-family
  required strings live in `signers` collection frontmatter; the
  validator can also be generated from that source of truth in a
  follow-up.
- **CSP hash for theme script**: the inline blocking script's SHA-256
  must be regenerated if the snippet changes. Mitigation: store the
  snippet in a single `src/scripts/theme-init.ts` file, compute hash at
  build time, write `vercel.json` from a template (`vercel.json.tpl`)
  during `pnpm run build`.
- **Font self-hosting size**: variable Inter + JetBrains Mono can be
  >300KB total. Mitigation: subset to Latin, use `font-display: swap`,
  preload only the two weights used above the fold.
- **OG image generation at build**: `satori` adds build time. Mitigation:
  cache rendered OGs keyed by post slug + `updatedAt`.

## 14. Success criteria

- `pnpm run build` produces a `dist/` that passes:
  - `validate_site.py` (all required text present, no forbidden claims,
    no legacy GitHub links ending in `/vault`, all five signer family names
    present, all current safety-contract strings present).
  - `tests/test_site_validation.py`.
  - `lychee`, `html-validate`, `axe`, `lhci` budgets.
- A `git push` to a Vercel-connected `main` produces a production
  deploy with the security headers from §10 verifiable via
  `curl -I`.
- Adding a new blog post is a single `.mdx` file commit; adding a new
  guide is a single `.mdx` under `src/content/docs/guides/`.
- The light/dark toggle works without FOUC and persists across reloads.
- No production security claim appears anywhere in `dist/`.
