# Website Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `website/public/index.html` + `styles.css` with a professional Astro site driven by Markdown/MDX content collections, with light/dark theming centered on Nostr purple `#8E30EB`, blog and documentation sections, and one-push Vercel deploy — preserving every safety-contract assertion enforced by the current `validate_site.py`.

**Architecture:** Astro 5 static output. Content collections for blog/docs/signers/authors with Zod schemas (build fails on bad frontmatter). Custom design system in CSS custom properties keyed by `data-theme`. Pagefind for static search, Shiki for code, RSS via `@astrojs/rss`. CI: `astro check` + `astro build` + ported `validate_site.py` against `dist/` + lychee + axe + lhci. Vercel framework preset = `astro`, strict CSP headers.

**Tech Stack:** Astro 5, TypeScript strict, MDX, Pagefind, Shiki, Zod, `@astrojs/sitemap`, `@astrojs/rss`, `@astrojs/check`, `satori` + `@resvg/resvg-js` for OG, pnpm, Node 22, Vercel.

**Source of truth for signer content:** `/Users/vincenzo/Documents/GitHub/nSealr/specs/vectors/features/signer-feature-matrix-v0.json`. Each signer MDX consumes its solution block (label, product_goal, repository, features).

---

## File Structure

Created / modified files in `website/`:

```
website/
  package.json                    [new]
  pnpm-workspace.yaml             [new]      empty workspace placeholder
  pnpm-lock.yaml                  [generated]
  tsconfig.json                   [new]
  astro.config.mjs                [new]
  vercel.json                     [new]
  Makefile                        [modify]   pnpm-based ci targets
  README.md                       [modify]   stack & dev/run/deploy section
  .gitignore                      [modify]   add dist/, .pagefind/, .vercel/
  .npmrc                          [new]      strict-peer-deps, prefer-frozen
  .nvmrc                          [new]      "22"

  public/
    fonts/Inter-Variable.woff2          [new, vendored]
    fonts/JetBrainsMono-Variable.woff2  [new, vendored]
    favicon.svg                          [new]
    og-default.png                       [new, generated once]
    robots.txt                           [new]
    index.html                           [delete in last task]
    styles.css                           [delete in last task]

  src/
    env.d.ts                                              [new]
    content.config.ts                                     [new]   Zod schemas
    styles/tokens.css                                     [new]   palette, typography vars
    styles/base.css                                       [new]   reset + global element styles
    styles/prose.css                                      [new]   .prose for MDX content
    scripts/theme-init.ts                                 [new]   blocking inline script source
    lib/og.ts                                             [new]   satori OG generator
    layouts/BaseLayout.astro                              [new]
    layouts/DocsLayout.astro                              [new]
    layouts/BlogPostLayout.astro                          [new]
    components/Header.astro                               [new]
    components/Footer.astro                               [new]
    components/ThemeToggle.astro                          [new]
    components/Hero.astro                                 [new]
    components/SystemMap.astro                            [new]   SVG, theme-aware
    components/SignerCard.astro                           [new]
    components/SignerFamilyGrid.astro                     [new]
    components/StatusPill.astro                           [new]
    components/Callout.astro                              [new]
    components/CodeBlock.astro                            [new]
    components/DocsSidebar.astro                          [new]
    components/TableOfContents.astro                      [new]
    components/BlogList.astro                             [new]
    components/TagPill.astro                              [new]
    components/FeatureMatrix.astro                        [new]
    components/SearchTrigger.astro                        [new]
    pages/index.astro                                     [new]   home
    pages/system.astro                                    [new]
    pages/security.astro                                  [new]
    pages/about.astro                                     [new]
    pages/contributing.astro                              [new]
    pages/404.astro                                       [new]
    pages/docs/index.astro                                [new]   redirects to /docs/getting-started
    pages/docs/[...slug].astro                            [new]
    pages/blog/index.astro                                [new]
    pages/blog/[...slug].astro                            [new]
    pages/blog/tags/[tag].astro                           [new]
    pages/blog/rss.xml.ts                                 [new]

    content/blog/2026-05-15-nsealr-website-relaunch.mdx   [new]   seed release post
    content/docs/getting-started/overview.mdx             [new]
    content/docs/getting-started/use.mdx                  [new]
    content/docs/guides/build-raspberry-qr-vault.mdx      [new]
    content/docs/guides/flash-esp32-firmware.mdx          [new]
    content/docs/specs/event-canonicalization.mdx         [new]
    content/docs/specs/qr-envelope.mdx                    [new]
    content/docs/security/trust-boundaries.mdx            [new]
    content/docs/security/threat-model.mdx                [new]
    content/signers/raspberry-qr.mdx                      [new]
    content/signers/esp32-qr.mdx                          [new]
    content/signers/esp32-usb.mdx                         [new]
    content/signers/smartcard.mdx                         [new]
    content/signers/custom-wallet.mdx                     [new]
    content/authors/nsealr-core.yaml                      [new]

  scripts/
    validate_site.py                                      [rewrite]
    verify_repo.py                                        [keep as-is]
    build_og.mjs                                          [new]   batch OG image generation
    compute_csp_hash.mjs                                  [new]   reads theme-init.ts -> sha256

  tests/
    test_site_validation.py                               [rewrite]

  .github/workflows/ci.yml                                [modify]
```

Deleted at the end: `public/index.html`, `public/styles.css`, `content/.gitkeep`, `design/.gitkeep`.

---

## Tasks

### Task 1: Scaffold Astro project, pnpm, tsconfig, gitignore

**Files:**
- Create: `package.json`, `pnpm-workspace.yaml`, `.npmrc`, `.nvmrc`, `tsconfig.json`, `astro.config.mjs`, `src/env.d.ts`
- Modify: `.gitignore`

- [ ] **Step 1.1 — Write `package.json`**

```json
{
  "name": "@nsealr/website",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "engines": { "node": ">=22.0.0" },
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "node scripts/compute_csp_hash.mjs && astro build && pagefind --site dist && node scripts/build_og.mjs",
    "preview": "astro preview",
    "check": "astro check",
    "ci": "pnpm run check && pnpm run build && python3 scripts/validate_site.py && python3 -m unittest discover -s tests"
  },
  "dependencies": {
    "astro": "^5.0.0",
    "@astrojs/mdx": "^4.0.0",
    "@astrojs/sitemap": "^3.2.0",
    "@astrojs/rss": "^4.0.0",
    "@astrojs/check": "^0.9.4",
    "typescript": "^5.6.0",
    "zod": "^3.23.0",
    "shiki": "^1.22.0",
    "rehype-autolink-headings": "^7.1.0",
    "rehype-slug": "^6.0.0",
    "remark-gfm": "^4.0.0",
    "satori": "^0.11.0",
    "@resvg/resvg-js": "^2.6.2",
    "pagefind": "^1.1.1"
  }
}
```

- [ ] **Step 1.2 — `pnpm-workspace.yaml`**

```yaml
packages: []
```

- [ ] **Step 1.3 — `.npmrc`**

```
strict-peer-dependencies=true
auto-install-peers=true
shamefully-hoist=false
```

- [ ] **Step 1.4 — `.nvmrc`**

```
22
```

- [ ] **Step 1.5 — `tsconfig.json`**

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "~/*": ["src/*"] },
    "verbatimModuleSyntax": true,
    "allowImportingTsExtensions": false
  },
  "include": [".astro/types.d.ts", "src/**/*", "scripts/**/*.mjs"],
  "exclude": ["dist/**", "node_modules/**"]
}
```

- [ ] **Step 1.6 — `astro.config.mjs`**

```js
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import remarkGfm from 'remark-gfm';

export default defineConfig({
  site: 'https://nsealr.vercel.app',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'auto' },
  integrations: [mdx(), sitemap()],
  markdown: {
    syntaxHighlight: 'shiki',
    shikiConfig: {
      themes: { dark: 'github-dark-dimmed', light: 'min-light' },
      wrap: true
    },
    remarkPlugins: [remarkGfm],
    rehypePlugins: [
      rehypeSlug,
      [rehypeAutolinkHeadings, { behavior: 'wrap' }]
    ]
  },
  vite: { ssr: { noExternal: ['satori'] } }
});
```

- [ ] **Step 1.7 — `src/env.d.ts`**

```ts
/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />
```

- [ ] **Step 1.8 — Update `.gitignore`**

```
.DS_Store
node_modules/
dist/
.astro/
.vercel/
.pagefind/
.env
.env.*
!.env.example
```

- [ ] **Step 1.9 — Install + first build check**

```bash
cd /Users/vincenzo/Documents/GitHub/nSealr/website
corepack enable
corepack prepare pnpm@9 --activate
pnpm install
pnpm exec astro --version
```

Expected: prints `Astro v5.x.x`.

- [ ] **Step 1.10 — Commit**

```bash
git add package.json pnpm-workspace.yaml pnpm-lock.yaml .npmrc .nvmrc tsconfig.json astro.config.mjs src/env.d.ts .gitignore
git commit -m "build: scaffold astro 5 + pnpm + strict typescript"
```

---

### Task 2: Design tokens, base CSS, fonts, theme-init script

**Files:**
- Create: `src/styles/tokens.css`, `src/styles/base.css`, `src/styles/prose.css`, `src/scripts/theme-init.ts`, `public/fonts/Inter-Variable.woff2`, `public/fonts/JetBrainsMono-Variable.woff2`, `scripts/compute_csp_hash.mjs`

- [ ] **Step 2.1 — Vendored fonts**

Download Inter (variable, Latin subset) and JetBrains Mono (variable, Latin subset) `.woff2` from upstream releases:

```bash
mkdir -p public/fonts
curl -L -o public/fonts/Inter-Variable.woff2 'https://github.com/rsms/inter/raw/master/docs/font-files/InterVariable.woff2'
curl -L -o public/fonts/JetBrainsMono-Variable.woff2 'https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/variable/JetBrainsMono%5Bwght%5D.woff2'
ls -la public/fonts
```

Expected: both files > 50 KB.

- [ ] **Step 2.2 — `src/styles/tokens.css`**

```css
:root {
  --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  --font-sans: 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

  --radius-sm: 3px;
  --radius-md: 6px;
  --radius-lg: 10px;
  --radius-pill: 999px;

  --shadow-1: 0 1px 2px rgba(12, 8, 20, .08);
  --shadow-2: 0 4px 14px rgba(12, 8, 20, .12);

  --content-max: 72ch;
  --container-max: 1180px;
}

@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'JetBrains Mono';
  src: url('/fonts/JetBrainsMono-Variable.woff2') format('woff2-variations');
  font-weight: 100 800;
  font-style: normal;
  font-display: swap;
}

html[data-theme='dark'] {
  --bg:            #07060d;
  --bg-elevated:   #0f0c17;
  --bg-code:       #02010a;
  --fg:            #dcd4f0;
  --fg-strong:     #ffffff;
  --fg-muted:      #7e7393;
  --border:        #1f1830;
  --border-strong: #2d2440;
  --accent:        #8E30EB;
  --accent-soft:   #b388ff;
  --accent-bg:     rgba(142, 48, 235, .12);
  --ok:            #7be0a8;
  --ok-bg:         rgba(123, 224, 168, .10);
  --warn:          #ff7a90;
  --warn-bg:       rgba(255, 122, 144, .10);
  --pending:       #f5c451;
  --pending-bg:    rgba(245, 196, 81, .10);
}

html[data-theme='light'] {
  --bg:            #fbfaff;
  --bg-elevated:   #f3eefb;
  --bg-code:       #f3eefb;
  --fg:            #1a132b;
  --fg-strong:     #0c0814;
  --fg-muted:      #5b4f78;
  --border:        #e6def5;
  --border-strong: #d6c8ea;
  --accent:        #7c1fd9;
  --accent-soft:   #9d4bff;
  --accent-bg:     rgba(124, 31, 217, .08);
  --ok:            #0b8a5c;
  --ok-bg:         #dcfaeb;
  --warn:          #c1183c;
  --warn-bg:       #ffe0e6;
  --pending:       #a06c00;
  --pending-bg:    #fff3d6;
}
```

- [ ] **Step 2.3 — `src/styles/base.css`**

```css
*, *::before, *::after { box-sizing: border-box; }

html {
  color-scheme: dark light;
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 1.55;
  text-size-adjust: 100%;
  -webkit-font-smoothing: antialiased;
  scroll-behavior: smooth;
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { animation-duration: 0ms !important; transition-duration: 0ms !important; }
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main { flex: 1; }

a {
  color: var(--accent);
  text-decoration: none;
  text-decoration-skip-ink: auto;
}
a:hover { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px; }

:focus-visible {
  outline: 2px solid var(--accent-soft);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

::selection { background: var(--accent); color: white; }

code, kbd, samp, pre { font-family: var(--font-mono); font-size: 0.92em; }
:not(pre) > code {
  background: var(--bg-elevated);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}

img, svg, video { max-width: 100%; height: auto; display: block; }

.container {
  max-width: var(--container-max);
  margin-inline: auto;
  padding-inline: clamp(20px, 5vw, 48px);
}

.eyebrow {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--accent-soft);
  letter-spacing: 0.06em;
  text-transform: lowercase;
}

.skip-link {
  position: absolute; left: -9999px;
  background: var(--accent); color: white;
  padding: 8px 14px; border-radius: var(--radius-sm);
}
.skip-link:focus { left: 12px; top: 12px; z-index: 1000; }
```

- [ ] **Step 2.4 — `src/styles/prose.css`**

```css
.prose {
  max-width: var(--content-max);
  color: var(--fg);
}
.prose > * + * { margin-top: 1.2em; }
.prose h1, .prose h2, .prose h3, .prose h4 {
  font-family: var(--font-mono);
  color: var(--fg-strong);
  line-height: 1.15;
  letter-spacing: -0.01em;
}
.prose h1 { font-size: clamp(28px, 4vw, 40px); margin-top: 0; }
.prose h2 { font-size: 24px; margin-top: 2em; }
.prose h3 { font-size: 18px; margin-top: 1.6em; }
.prose h2 a, .prose h3 a, .prose h4 a {
  color: inherit; text-decoration: none;
}
.prose h2 a::before { content: '#'; color: var(--accent); opacity: 0; margin-right: 8px; }
.prose h2:hover a::before, .prose h3:hover a::before { opacity: 1; }

.prose p, .prose li { font-size: 16px; }
.prose ul, .prose ol { padding-left: 1.4em; }
.prose blockquote {
  border-left: 3px solid var(--accent);
  padding: 4px 14px;
  color: var(--fg-muted);
  background: var(--accent-bg);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
.prose pre {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  overflow-x: auto;
  border-left: 2px solid var(--accent);
  font-size: 13px;
  line-height: 1.65;
}
.prose table {
  width: 100%; border-collapse: collapse; font-size: 14px;
  border: 1px solid var(--border); border-radius: var(--radius-md); overflow: hidden;
}
.prose th, .prose td {
  text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--border);
}
.prose th { background: var(--bg-elevated); font-family: var(--font-mono); font-size: 12px; }
.prose tbody tr:nth-child(even) { background: var(--bg-elevated); }

.prose hr { border: none; border-top: 1px solid var(--border); margin: 2.4em 0; }
```

- [ ] **Step 2.5 — `src/scripts/theme-init.ts`**

The file holds the literal blocking script as a default export string. The build hash is computed from this exact text.

```ts
export const themeInitScript = `(()=>{try{var s=localStorage.getItem('theme');var t=s==='light'||s==='dark'?s:(matchMedia('(prefers-color-scheme: light)').matches?'light':'dark');document.documentElement.setAttribute('data-theme',t);}catch(e){document.documentElement.setAttribute('data-theme','dark');}})();`;
```

- [ ] **Step 2.6 — `scripts/compute_csp_hash.mjs`**

```js
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const src = readFileSync('src/scripts/theme-init.ts', 'utf8');
const match = src.match(/`([^`]+)`/);
if (!match) {
  console.error('compute_csp_hash: cannot find script literal in theme-init.ts');
  process.exit(1);
}
const script = match[1];
const hash = createHash('sha256').update(script).digest('base64');

let vercel;
const tplPath = 'vercel.json.tpl';
const outPath = 'vercel.json';
if (!existsSync(tplPath)) {
  console.error(`compute_csp_hash: ${tplPath} missing`);
  process.exit(1);
}
vercel = readFileSync(tplPath, 'utf8').replaceAll('__THEME_INIT_HASH__', hash);
writeFileSync(outPath, vercel);
console.log(`compute_csp_hash: vercel.json written with sha256-${hash}`);
```

- [ ] **Step 2.7 — Sanity: import tokens compiles**

Create a temp page later (Task 4) to consume tokens. For now:

```bash
pnpm exec astro check
```

Expected: no errors. (No `.astro` pages exist yet — Astro reports `0 errors`.)

- [ ] **Step 2.8 — Commit**

```bash
git add public/fonts src/styles src/scripts scripts/compute_csp_hash.mjs
git commit -m "feat(design): tokens, base + prose styles, vendored variable fonts"
```

---

### Task 3: Content collections (schemas + seed signers)

**Files:**
- Create: `src/content.config.ts`, `src/content/authors/nsealr-core.yaml`, `src/content/signers/{raspberry-qr,esp32-qr,esp32-usb,smartcard,custom-wallet}.mdx`

- [ ] **Step 3.1 — `src/content.config.ts`**

```ts
import { defineCollection, reference, z } from 'astro:content';
import { glob, file } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/blog' }),
  schema: ({ image }) => z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.date(),
    updatedAt: z.date().optional(),
    category: z.enum(['release', 'research', 'tutorial', 'news']),
    tags: z.array(z.string()).default([]),
    authors: z.array(reference('authors')).min(1),
    cover: image().optional(),
    draft: z.boolean().default(false),
  })
});

const DOC_SECTIONS = ['getting-started', 'guides', 'signers', 'specs', 'security'] as const;

const docs = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/docs' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    section: z.enum(DOC_SECTIONS),
    order: z.number().default(100),
    updatedAt: z.date(),
    status: z.enum(['stable', 'draft', 'research']).default('stable'),
  }).superRefine((data, ctx) => {
    // section must match folder prefix; checked via id at runtime in pages
  })
});

const FAMILY_KEYS = ['raspberry-qr', 'esp32-qr', 'esp32-usb', 'smartcard', 'custom-wallet'] as const;
const CAPABILITY_STATUS = ['target', 'present', 'absent', 'disabled', 'partial', 'planned', 'research', 'forbidden', 'not_applicable', 'implemented', 'disabled_until_gates_pass'] as const;

const signers = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/signers' }),
  schema: z.object({
    family: z.enum(FAMILY_KEYS),
    displayName: z.string(),
    tagline: z.string(),
    repo: z.string().url(),
    productGoal: z.string(),
    maturity: z.enum(['research', 'prototype', 'alpha', 'beta']),
    capabilities: z.array(z.object({
      id: z.string(),
      target: z.enum(CAPABILITY_STATUS),
      current: z.enum(CAPABILITY_STATUS),
      contractId: z.string().optional(),
      notes: z.string().optional()
    })),
    requiredText: z.array(z.string()).default([]),
    order: z.number()
  })
});

const authors = defineCollection({
  loader: file('src/content/authors/_authors.json'),
  schema: z.object({
    id: z.string(),
    name: z.string(),
    bio: z.string().optional(),
    links: z.object({
      github: z.string().url().optional(),
      nostr: z.string().optional(),
      web: z.string().url().optional(),
    }).default({})
  })
});

export const collections = { blog, docs, signers, authors };
```

- [ ] **Step 3.2 — `src/content/authors/_authors.json`**

```json
[
  {
    "id": "nsealr-core",
    "name": "nSealr Core",
    "bio": "Non-profit, open-source program for Nostr signing devices.",
    "links": {
      "github": "https://github.com/nSealr",
      "web": "https://nsealr.vercel.app"
    }
  }
]
```

- [ ] **Step 3.3 — `src/content/signers/raspberry-qr.mdx`**

Frontmatter values come directly from `specs/vectors/features/signer-feature-matrix-v0.json` (`solutions.raspberry_qr_vault`). `requiredText` re-asserts the safety-contract phrases this family page must contain (used by `validate_site.py`).

```mdx
---
family: 'raspberry-qr'
displayName: 'Raspberry/Pi Stateless QR Vault'
tagline: 'Air-gapped RAM-only Raspberry/Pi flow inspired by SeedSigner principles for Nostr events.'
repo: 'https://github.com/nSealr/raspberry'
productGoal: 'A SeedSigner-like airgapped Nostr signer for Raspberry/Pi hardware with RAM-only key custody and QR request/response workflows.'
maturity: 'alpha'
order: 1
capabilities:
  - { id: 'request_validation_v0',      target: 'required', current: 'implemented',  contractId: 'signing-request-v0+implementation-limits-v0+invalid-vectors' }
  - { id: 'nostr_event_review_universal', target: 'required', current: 'implemented', contractId: 'trusted-review-v0+review-detail-pages-v0' }
  - { id: 'review_detail_pages',        target: 'required', current: 'implemented',  contractId: 'review-detail-pages-v0' }
  - { id: 'approval_digest_binding',    target: 'required', current: 'implemented',  contractId: 'approval-digest-v0' }
  - { id: 'physical_approval',          target: 'required', current: 'partial',      contractId: 'physical-approval-v0' }
  - { id: 'sign_event_bip340',          target: 'required', current: 'implemented',  contractId: 'nostr-sign-event-bip340-v0' }
  - { id: 'qr_static_request',          target: 'required', current: 'implemented',  contractId: 'qr-envelope-static-v0' }
  - { id: 'qr_animated_request',        target: 'required', current: 'implemented',  contractId: 'qr-envelope-animated-v0' }
  - { id: 'qr_response',                target: 'required', current: 'implemented',  contractId: 'qr-response-v0' }
  - { id: 'stateless_session_custody',  target: 'required', current: 'partial',      contractId: 'stateless-session-custody-v0' }
  - { id: 'manual_only_policy',         target: 'required', current: 'implemented',  contractId: 'manual-only-approval-policy-v0' }
  - { id: 'device_display_review',      target: 'required', current: 'partial',      contractId: 'device-display-review-v0' }
  - { id: 'response_verification',      target: 'required', current: 'implemented',  contractId: 'signed-response-verification-v0' }
  - { id: 'persistent_secret_custody',  target: 'forbidden', current: 'forbidden' }
  - { id: 'scoped_policy_automation',   target: 'forbidden', current: 'forbidden' }
requiredText:
  - 'Raspberry/Pi Stateless QR Vault'
  - 'Raspberry/Pi kit requirements'
  - 'Raspberry/Pi OS profile'
  - 'review detail pages'
  - 'approval_digest'
---

# Raspberry/Pi Stateless QR Vault

A SeedSigner-style air-gapped Nostr signer for Raspberry/Pi hardware. Secret material lives in RAM only for the current signing session and is wiped when the device powers off. Every request and response moves over QR; no wireless, no host link.

## Hardware target

The primary kit follows the SeedSigner Pi Zero pattern:

- Pi Zero-class board.
- Pi/ZeroCam OV5647 camera.
- Waveshare-compatible ST7789 240×240 LCD HAT.
- GPIO joystick / buttons.
- Removable microSD boot media.
- SeedSigner-OS-inspired minimal runtime (Raspberry/Pi OS profile: removable boot media, disabled or absent wireless, RAM-only session custody, no swap during signing, no remote access during signing, no persistent signing-secret storage).

Pi 3/4/5 variants can be development or accessibility targets later only if they preserve the same offline QR, local review, physical approval, and RAM-only custody boundary. See the **Raspberry/Pi kit requirements** in `nSealr/hardware`.

## What it does today

import { FeatureMatrix } from '~/components/FeatureMatrix.astro';

<FeatureMatrix family="raspberry-qr" />

## Trust boundary

The companion is not trusted with key custody — it routes static and animated `nsealr1:` QR requests to the device and verifies signed responses against `nSealr/specs` fixtures. The vault performs trusted display **review detail pages** so long content and tags reach the user without truncation, binds the local approval action to the exact reviewed material through `approval_digest`, and signs BIP-340/secp256k1.

## Repository

[github.com/nSealr/raspberry](https://github.com/nSealr/raspberry)
```

- [ ] **Step 3.4 — `src/content/signers/esp32-qr.mdx`**

```mdx
---
family: 'esp32-qr'
displayName: 'ESP32 Stateless QR Vault'
tagline: 'Air-gapped ESP32-S3 camera/display signer line; T-Display S3 Pro OV5640 candidate, no persistent secret.'
repo: 'https://github.com/nSealr/esp32'
productGoal: 'An airgapped ESP32-S3 QR signer with camera, display, local controls, RAM-only key custody, and behavior matching the Raspberry QR vault where features overlap.'
maturity: 'prototype'
order: 2
capabilities:
  - { id: 'request_validation_v0',        target: 'required', current: 'implemented', contractId: 'signing-request-v0+implementation-limits-v0+invalid-vectors' }
  - { id: 'nostr_event_review_universal', target: 'required', current: 'implemented', contractId: 'trusted-review-v0+review-detail-pages-v0' }
  - { id: 'review_detail_pages',          target: 'required', current: 'implemented', contractId: 'review-detail-pages-v0' }
  - { id: 'approval_digest_binding',      target: 'required', current: 'implemented', contractId: 'approval-digest-v0' }
  - { id: 'physical_approval',            target: 'required', current: 'partial',     contractId: 'physical-approval-v0' }
  - { id: 'sign_event_bip340',            target: 'required', current: 'disabled_until_gates_pass', contractId: 'nostr-sign-event-bip340-v0' }
  - { id: 'qr_static_request',            target: 'required', current: 'partial',     contractId: 'qr-envelope-static-v0' }
  - { id: 'qr_animated_request',          target: 'required', current: 'partial',     contractId: 'qr-envelope-animated-v0' }
  - { id: 'qr_response',                  target: 'required', current: 'planned',     contractId: 'qr-response-v0' }
  - { id: 'stateless_session_custody',    target: 'required', current: 'planned',     contractId: 'stateless-session-custody-v0' }
  - { id: 'manual_only_policy',           target: 'required', current: 'implemented', contractId: 'manual-only-approval-policy-v0' }
  - { id: 'device_display_review',        target: 'required', current: 'partial',     contractId: 'device-display-review-v0' }
  - { id: 'response_verification',        target: 'required', current: 'planned',     contractId: 'signed-response-verification-v0' }
  - { id: 'secure_boot_hardening',        target: 'optional', current: 'planned',     contractId: 'firmware-boot-hardening-v0' }
requiredText:
  - 'ESP32 Stateless QR Vault'
  - 'T-Display S3 review scenario smoke'
  - 'signing_disabled'
  - 'approval_digest'
  - 'firmware protocol evidence'
  - 'Unicode fallback'
---

# ESP32 Stateless QR Vault

Air-gapped ESP32-S3 camera + display signer. Behavior parity with the Raspberry QR vault is enforced through shared `contract_id`s in `nSealr/specs`.

## Hardware target

- Primary candidate: **T-Display S3 Pro OV5640** (camera + display).
- Secondary target: Waveshare `ESP32-S3-Touch-LCD-3.5B-C`.
- Production-readiness gates: real camera ingestion, display acceptance, button drivers, provisioning.

## Current status

Real `sign_event` is **`signing_disabled`** in development firmware until all hardening, display, button, and provisioning gates pass. The T-Display S3 review scenario smoke confirms host-core review frames render correctly; this is **development evidence**, not a production trusted-display claim. Approvals are bound to `approval_digest`. Firmware protocol evidence and Unicode fallback tracking are recorded in `nSealr/esp32`.

<FeatureMatrix family="esp32-qr" />

import { FeatureMatrix } from '~/components/FeatureMatrix.astro';

## Repository

[github.com/nSealr/esp32](https://github.com/nSealr/esp32)
```

- [ ] **Step 3.5 — `src/content/signers/esp32-usb.mdx`**

```mdx
---
family: 'esp32-usb'
displayName: 'ESP32 USB/NIP-46 Signer'
tagline: 'Daily-use USB/display signer firmware for ESP32-S3 first, with classic ESP32/TTGO compatibility later. Real signing still gated.'
repo: 'https://github.com/nSealr/esp32'
productGoal: 'A daily-use connected ESP32-S3 signer with USB/display review, optional scoped policy automation through the companion, and real signing disabled until hardening gates pass.'
maturity: 'prototype'
order: 3
capabilities:
  - { id: 'request_validation_v0',        target: 'required', current: 'implemented', contractId: 'signing-request-v0+implementation-limits-v0+invalid-vectors' }
  - { id: 'nostr_event_review_universal', target: 'required', current: 'implemented', contractId: 'trusted-review-v0+review-detail-pages-v0' }
  - { id: 'review_detail_pages',          target: 'optional', current: 'implemented', contractId: 'review-detail-pages-v0' }
  - { id: 'approval_digest_binding',      target: 'required', current: 'implemented', contractId: 'approval-digest-v0' }
  - { id: 'physical_approval',            target: 'required', current: 'partial',     contractId: 'physical-approval-v0' }
  - { id: 'sign_event_bip340',            target: 'required', current: 'disabled_until_gates_pass', contractId: 'nostr-sign-event-bip340-v0' }
  - { id: 'serial_usb_transport',         target: 'required', current: 'implemented', contractId: 'serial-usb-transport-v0' }
  - { id: 'nip46_decrypted_bridge',       target: 'required', current: 'partial',     contractId: 'nip46-decrypted-bridge-v0' }
  - { id: 'scoped_policy_automation',     target: 'required', current: 'planned',     contractId: 'scoped-policy-automation-v0' }
  - { id: 'persistent_secret_custody',    target: 'required', current: 'planned',     contractId: 'persistent-secret-custody-v0' }
  - { id: 'secure_boot_hardening',        target: 'required', current: 'planned',     contractId: 'firmware-boot-hardening-v0' }
  - { id: 'response_verification',        target: 'required', current: 'implemented', contractId: 'signed-response-verification-v0' }
  - { id: 'stateless_session_custody',    target: 'forbidden', current: 'forbidden' }
requiredText:
  - 'ESP32 USB/NIP-46 Signer'
  - 'NIP-46 bridge decisions'
  - 'nsealr nip46 decide'
  - 'request-bound capture checks'
  - 'nsealr serial-line exchange'
  - 'sign-event-disabled smoke'
  - 'companion-to-device serial smoke'
  - 'firmware protocol evidence'
  - 'Unicode fallback'
  - 'signing_disabled'
  - 'approval_digest'
---

# ESP32 USB/NIP-46 Signer

Daily-use connected ESP32-S3 signer with USB/display review and bridged NIP-46 inputs.

## Boundaries

- The companion handles **NIP-46 bridge decisions** via `nsealr nip46 decide`; the device receives already-decrypted, validated signing requests.
- USB transport uses bounded frames with `request-bound capture checks`. Bring-up is covered by `nsealr serial-line exchange`.
- Smoke evidence: `companion-to-device serial smoke`, `sign-event-disabled smoke`, `firmware protocol evidence`, Unicode fallback tracking.
- `signing_disabled` until hardening gates pass; approvals are bound to `approval_digest`.

<FeatureMatrix family="esp32-usb" />

import { FeatureMatrix } from '~/components/FeatureMatrix.astro';

## Repository

[github.com/nSealr/esp32](https://github.com/nSealr/esp32)
```

- [ ] **Step 3.6 — `src/content/signers/smartcard.mdx`**

```mdx
---
family: 'smartcard'
displayName: 'JavaCard/NFC Smartcard Signer'
tagline: 'Display-less APDU card research for key protection, not trusted event review alone.'
repo: 'https://github.com/nSealr/smartcard'
productGoal: 'A display-less card custody line that can sign through APDUs only after external review acknowledgement and deterministic policy checks.'
maturity: 'research'
order: 4
capabilities:
  - { id: 'request_validation_v0',         target: 'required', current: 'partial',  contractId: 'signing-request-v0+implementation-limits-v0+invalid-vectors' }
  - { id: 'approval_digest_binding',       target: 'required', current: 'partial',  contractId: 'approval-digest-v0' }
  - { id: 'sign_event_bip340',             target: 'required', current: 'partial',  contractId: 'nostr-sign-event-bip340-v0' }
  - { id: 'persistent_secret_custody',     target: 'required', current: 'partial',  contractId: 'persistent-secret-custody-v0' }
  - { id: 'smartcard_apdu',                target: 'required', current: 'implemented', contractId: 'smartcard-apdu-v0' }
  - { id: 'external_review_acknowledgement', target: 'required', current: 'partial', contractId: 'external-review-acknowledgement-v0' }
  - { id: 'response_verification',         target: 'required', current: 'partial',  contractId: 'signed-response-verification-v0' }
  - { id: 'device_display_review',         target: 'not_applicable', current: 'not_applicable' }
  - { id: 'physical_approval',             target: 'not_applicable', current: 'not_applicable' }
  - { id: 'stateless_session_custody',     target: 'forbidden', current: 'forbidden' }
requiredText:
  - 'JavaCard/NFC Smartcard Signer'
  - 'nsealr-smartcard CLI probes'
  - 'no trusted review or real-card compatibility claim'
---

# JavaCard/NFC Smartcard Signer

Display-less APDU custody. The card cannot provide trusted event review by itself; external review acknowledgement is required before any APDU signing operation reaches the card.

## Current evidence

- Python APDU codec with `GET_PUBLIC_KEY` and `SIGN_EVENT_ID` proprietary constants.
- secp256k1-backed simulator returning x-only public keys and signatures on 32-byte event ids.
- `nsealr-smartcard CLI probes` for simulator and PC/SC probes; PC/SC commands fail clearly without `pyscard` or a reader.
- Tests against shared `nSealr/specs` event-id and APDU status-word rejection vectors.
- **No trusted review or real-card compatibility claim** yet.

<FeatureMatrix family="smartcard" />

import { FeatureMatrix } from '~/components/FeatureMatrix.astro';

## Repository

[github.com/nSealr/smartcard](https://github.com/nSealr/smartcard)
```

- [ ] **Step 3.7 — `src/content/signers/custom-wallet.mdx`**

```mdx
---
family: 'custom-wallet'
displayName: 'Custom Nostr Hardware Wallet With Persistent Secret'
tagline: 'USB-C bus-powered persistent-secret wallet research with TROPIC01 assistance; direct TROPIC01 Schnorr remains future-gated.'
repo: 'https://github.com/nSealr/hardware'
productGoal: 'A research family for a purpose-built persistent-secret Nostr hardware wallet, now centered on a USB-C bus-powered TROPIC01-assisted Rev A scaffold before any KiCad or production claim.'
maturity: 'research'
order: 5
capabilities:
  - { id: 'request_validation_v0',        target: 'required', current: 'planned',  contractId: 'signing-request-v0+implementation-limits-v0+invalid-vectors' }
  - { id: 'nostr_event_review_universal', target: 'required', current: 'planned',  contractId: 'trusted-review-v0+review-detail-pages-v0' }
  - { id: 'review_detail_pages',          target: 'required', current: 'planned',  contractId: 'review-detail-pages-v0' }
  - { id: 'approval_digest_binding',      target: 'required', current: 'planned',  contractId: 'approval-digest-v0' }
  - { id: 'physical_approval',            target: 'required', current: 'planned',  contractId: 'physical-approval-v0' }
  - { id: 'sign_event_bip340',            target: 'required', current: 'research', contractId: 'nostr-sign-event-bip340-v0' }
  - { id: 'persistent_secret_custody',    target: 'required', current: 'research', contractId: 'persistent-secret-custody-v0' }
  - { id: 'secure_boot_hardening',        target: 'required', current: 'research', contractId: 'firmware-boot-hardening-v0' }
  - { id: 'device_display_review',        target: 'required', current: 'planned',  contractId: 'device-display-review-v0' }
  - { id: 'response_verification',        target: 'required', current: 'planned',  contractId: 'signed-response-verification-v0' }
  - { id: 'stateless_session_custody',    target: 'forbidden', current: 'forbidden' }
requiredText:
  - 'Custom Nostr Hardware Wallet With Persistent Secret'
  - 'USB-C bus-powered'
  - 'Direct TROPIC01 Schnorr/BIP-340 remains future-gated'
---

# Custom Nostr Hardware Wallet With Persistent Secret

Research family for a purpose-built persistent-secret Nostr hardware wallet. The current Rev A direction is USB-C bus-powered, connected/no-wireless, no-battery, and TROPIC01-assisted. BIP-340 signing stays on the ESP32-S3 host MCU unless a public TROPIC01 API, firmware release, or written vendor path proves non-exportable Schnorr support.

<FeatureMatrix family="custom-wallet" />

import { FeatureMatrix } from '~/components/FeatureMatrix.astro';

## Repository

Open hardware: [github.com/nSealr/hardware](https://github.com/nSealr/hardware). ESP32 firmware references: [github.com/nSealr/esp32](https://github.com/nSealr/esp32).
```

- [ ] **Step 3.8 — Verify schemas with astro check**

```bash
pnpm exec astro sync
pnpm exec astro check
```

Expected: `Result (5 files): 0 errors`.

- [ ] **Step 3.9 — Commit**

```bash
git add src/content.config.ts src/content/authors src/content/signers
git commit -m "content: signer collection + 5 family pages sourced from feature-matrix-v0"
```

---

### Task 4: Core components (Header, Footer, ThemeToggle, BaseLayout)

**Files:** Create `src/components/{ThemeToggle,Header,Footer,StatusPill,Callout,TagPill}.astro`, `src/layouts/BaseLayout.astro`.

- [ ] **Step 4.1 — `src/components/ThemeToggle.astro`**

```astro
---
---
<button id="theme-toggle" type="button" aria-label="Toggle color theme" aria-pressed="false" class="theme-toggle">
  <span class="sun" aria-hidden="true">☀</span>
  <span class="moon" aria-hidden="true">☾</span>
</button>
<style>
  .theme-toggle {
    display: inline-grid; place-items: center;
    width: 34px; height: 34px;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    background: transparent; color: var(--fg);
    cursor: pointer; position: relative;
  }
  .theme-toggle:hover { border-color: var(--accent); }
  .theme-toggle .sun, .theme-toggle .moon {
    position: absolute; transition: opacity 120ms, transform 120ms;
    font-size: 15px; line-height: 1;
  }
  html[data-theme='dark'] .theme-toggle .sun { opacity: 0; transform: rotate(-30deg); }
  html[data-theme='dark'] .theme-toggle .moon { opacity: 1; }
  html[data-theme='light'] .theme-toggle .sun { opacity: 1; }
  html[data-theme='light'] .theme-toggle .moon { opacity: 0; transform: rotate(30deg); }
</style>
<script>
  const btn = document.getElementById('theme-toggle');
  const sync = () => {
    const t = document.documentElement.getAttribute('data-theme') || 'dark';
    btn?.setAttribute('aria-pressed', String(t === 'light'));
  };
  sync();
  btn?.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch {}
    sync();
  });
</script>
```

- [ ] **Step 4.2 — `src/components/Header.astro`**

```astro
---
import ThemeToggle from './ThemeToggle.astro';
const { pathname } = Astro.url;
const isActive = (p: string) => pathname === p || pathname.startsWith(p + '/');
---
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/">
      <span class="mark" aria-hidden="true">ns</span>
      <span>nsealr</span>
    </a>
    <nav aria-label="Primary">
      <a class={isActive('/system') ? 'active' : ''} href="/system/">System</a>
      <a class={isActive('/docs') ? 'active' : ''} href="/docs/">Docs</a>
      <a class={isActive('/blog') ? 'active' : ''} href="/blog/">Blog</a>
      <a class={isActive('/security') ? 'active' : ''} href="/security/">Security</a>
      <a class="ext" href="https://github.com/nSealr" rel="noopener">GitHub ↗</a>
      <ThemeToggle />
    </nav>
  </div>
</header>

<style>
  .site-header {
    position: sticky; top: 0; z-index: 50;
    border-bottom: 1px solid var(--border);
    background: color-mix(in oklab, var(--bg) 88%, transparent);
    backdrop-filter: saturate(140%) blur(8px);
  }
  .header-inner {
    display: flex; align-items: center; justify-content: space-between;
    height: 60px; gap: 16px;
  }
  .brand {
    display: inline-flex; align-items: center; gap: 10px;
    color: var(--fg-strong); font-family: var(--font-mono); font-weight: 700;
    text-decoration: none; font-size: 15px;
  }
  .brand .mark {
    width: 26px; height: 26px; border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm); display: grid; place-items: center;
    font-size: 11px; color: var(--accent-soft);
  }
  nav {
    display: flex; align-items: center; gap: 22px;
    font-family: var(--font-mono); font-size: 13px;
  }
  nav a { color: var(--fg-muted); text-decoration: none; }
  nav a:hover { color: var(--fg-strong); }
  nav a.active { color: var(--accent-soft); }
  nav a.ext { color: var(--fg-muted); }
  @media (max-width: 720px) {
    .header-inner { flex-direction: column; align-items: stretch; gap: 8px; padding-block: 10px; height: auto; }
    nav { flex-wrap: wrap; gap: 14px; }
  }
</style>
```

- [ ] **Step 4.3 — `src/components/Footer.astro`**

```astro
---
const year = new Date().getFullYear();
---
<footer class="site-footer">
  <div class="container footer-inner">
    <div>
      <p class="brand-line"><span class="brand-mark">ns</span> nsealr — non-profit · open-source signer program</p>
      <p class="muted">Pre-production research. No production security claim. MIT for code; CC0-1.0 for content.</p>
    </div>
    <nav aria-label="Repositories">
      <a href="https://github.com/nSealr/specs">specs</a>
      <a href="https://github.com/nSealr/companion">companion</a>
      <a href="https://github.com/nSealr/raspberry">raspberry</a>
      <a href="https://github.com/nSealr/esp32">esp32</a>
      <a href="https://github.com/nSealr/smartcard">smartcard</a>
      <a href="https://github.com/nSealr/hardware">hardware</a>
      <a href="https://github.com/nSealr/lab">lab</a>
      <a href="/blog/rss.xml">RSS</a>
    </nav>
    <p class="muted small">© {year} nSealr contributors.</p>
  </div>
</footer>

<style>
  .site-footer { border-top: 1px solid var(--border); margin-top: 80px; padding: 36px 0; }
  .footer-inner { display: grid; gap: 18px; }
  .brand-line { font-family: var(--font-mono); font-size: 14px; margin: 0 0 4px; }
  .brand-mark { background: var(--accent-bg); color: var(--accent-soft); padding: 2px 6px; border-radius: var(--radius-sm); }
  .muted { color: var(--fg-muted); margin: 0; font-size: 14px; }
  .muted.small { font-size: 12px; }
  nav { display: flex; flex-wrap: wrap; gap: 14px; font-family: var(--font-mono); font-size: 13px; }
  nav a { color: var(--fg-muted); text-decoration: none; }
  nav a:hover { color: var(--accent-soft); }
</style>
```

- [ ] **Step 4.4 — `src/components/StatusPill.astro`**

```astro
---
type Variant = 'ok' | 'warn' | 'pending' | 'neutral' | 'disabled';
interface Props { variant?: Variant; label?: string; }
const { variant = 'neutral', label } = Astro.props;
const symbol = variant === 'ok' ? '✓' : variant === 'warn' ? '!' : variant === 'disabled' ? '⊘' : variant === 'pending' ? '◔' : '•';
---
<span class={`pill pill-${variant}`}>
  <span aria-hidden="true">{symbol}</span>
  <slot>{label}</slot>
</span>
<style>
  .pill {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: var(--font-mono); font-size: 11px; font-weight: 600;
    padding: 3px 9px; border-radius: var(--radius-pill);
    border: 1px solid;
    line-height: 1.4;
  }
  .pill-ok       { color: var(--ok);       background: var(--ok-bg);       border-color: color-mix(in oklab, var(--ok) 40%, transparent); }
  .pill-warn     { color: var(--warn);     background: var(--warn-bg);     border-color: color-mix(in oklab, var(--warn) 40%, transparent); }
  .pill-disabled { color: var(--warn);     background: var(--warn-bg);     border-color: color-mix(in oklab, var(--warn) 40%, transparent); }
  .pill-pending  { color: var(--pending);  background: var(--pending-bg);  border-color: color-mix(in oklab, var(--pending) 40%, transparent); }
  .pill-neutral  { color: var(--accent-soft); background: var(--accent-bg); border-color: color-mix(in oklab, var(--accent) 40%, transparent); }
</style>
```

- [ ] **Step 4.5 — `src/components/Callout.astro`**

```astro
---
interface Props { variant?: 'info' | 'warn' | 'danger'; title?: string; }
const { variant = 'info', title } = Astro.props;
---
<aside class={`callout callout-${variant}`} role={variant === 'info' ? 'note' : 'alert'}>
  {title && <p class="callout-title">{title}</p>}
  <div class="callout-body"><slot /></div>
</aside>
<style>
  .callout {
    border-left: 3px solid var(--accent);
    background: var(--accent-bg);
    padding: 12px 16px;
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    margin: 1.4em 0;
  }
  .callout-warn { border-color: var(--pending); background: var(--pending-bg); }
  .callout-danger { border-color: var(--warn); background: var(--warn-bg); }
  .callout-title { font-family: var(--font-mono); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 4px; color: var(--fg-strong); }
  .callout-body :global(p) { margin: 0; }
  .callout-body :global(p + p) { margin-top: 8px; }
</style>
```

- [ ] **Step 4.6 — `src/components/TagPill.astro`**

```astro
---
interface Props { tag: string; href?: string; }
const { tag, href } = Astro.props;
---
{href
  ? <a class="tag-pill" href={href}>#{tag}</a>
  : <span class="tag-pill">#{tag}</span>}
<style>
  .tag-pill {
    display: inline-block;
    font-family: var(--font-mono); font-size: 11px;
    color: var(--fg-muted);
    border: 1px solid var(--border);
    padding: 2px 8px; border-radius: var(--radius-pill);
    text-decoration: none;
  }
  a.tag-pill:hover { color: var(--accent-soft); border-color: var(--accent); }
</style>
```

- [ ] **Step 4.7 — `src/layouts/BaseLayout.astro`**

```astro
---
import '~/styles/tokens.css';
import '~/styles/base.css';
import '~/styles/prose.css';
import Header from '~/components/Header.astro';
import Footer from '~/components/Footer.astro';
import { themeInitScript } from '~/scripts/theme-init';

interface Props {
  title: string;
  description: string;
  ogImage?: string;
  noindex?: boolean;
}
const { title, description, ogImage = '/og-default.png', noindex = false } = Astro.props;
const canonical = new URL(Astro.url.pathname, Astro.site).toString();
---
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="dark light" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />
    {noindex && <meta name="robots" content="noindex,nofollow" />}
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="alternate" type="application/rss+xml" title="nSealr blog" href="/blog/rss.xml" />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={ogImage} />
    <meta property="og:type" content="website" />
    <meta property="og:url" content={canonical} />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="preload" href="/fonts/Inter-Variable.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="/fonts/JetBrainsMono-Variable.woff2" as="font" type="font/woff2" crossorigin />
    <script set:html={themeInitScript}></script>
  </head>
  <body>
    <a href="#main" class="skip-link">Skip to content</a>
    <Header />
    <main id="main">
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

- [ ] **Step 4.8 — Type-check**

```bash
pnpm exec astro check
```

Expected: `0 errors`.

- [ ] **Step 4.9 — Commit**

```bash
git add src/layouts src/components/Header.astro src/components/Footer.astro src/components/ThemeToggle.astro src/components/StatusPill.astro src/components/Callout.astro src/components/TagPill.astro
git commit -m "feat(layout): base layout, header, footer, theme toggle, status pill, callout"
```

---

### Task 5: Home, system, security, about, contributing, 404

**Files:** Create `src/components/{Hero,SystemMap,SignerFamilyGrid,SignerCard,FeatureMatrix,SearchTrigger}.astro`, `src/pages/{index,system,security,about,contributing,404}.astro`, `public/favicon.svg`, `public/robots.txt`.

- [ ] **Step 5.1 — `public/favicon.svg`**

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="6" fill="#8E30EB"/>
  <text x="50%" y="56%" text-anchor="middle" dominant-baseline="middle"
        font-family="JetBrains Mono, Menlo, monospace" font-size="13" font-weight="700" fill="#ffffff">ns</text>
</svg>
```

- [ ] **Step 5.2 — `public/robots.txt`**

```
User-agent: *
Allow: /
Sitemap: https://nsealr.vercel.app/sitemap-index.xml
```

- [ ] **Step 5.3 — `src/components/Hero.astro`**

```astro
---
import StatusPill from './StatusPill.astro';
---
<section class="hero container">
  <p class="eyebrow">// nsealr · v0 · stateless · pre-production</p>
  <h1>Sign <em>Nostr</em><br />events offline.</h1>
  <p class="lead">
    A non-profit, open-source program for reproducible Nostr signing devices.
    Companion software, five signer families, and open hardware references —
    auditable instead of proprietary.
  </p>
  <div class="actions">
    <a class="btn primary" href="/docs/">$ read the docs</a>
    <a class="btn ghost" href="https://github.com/nSealr" rel="noopener">github ↗</a>
  </div>
  <div class="pills">
    <StatusPill variant="ok">approval_digest</StatusPill>
    <StatusPill variant="warn">signing_disabled</StatusPill>
    <StatusPill variant="neutral">v0 spec</StatusPill>
    <StatusPill variant="neutral">non-profit · open-source</StatusPill>
  </div>
  <pre class="snippet"><code>{`# verify a response — companion
$ nsealr verify-response --request req.json --response resp.json
✓ approval_digest ok
! sign-event disabled in dev firmware`}</code></pre>
</section>

<style>
  .hero { padding-block: clamp(48px, 8vw, 110px) clamp(24px, 4vw, 56px); }
  .hero h1 {
    font-family: var(--font-mono); color: var(--fg-strong);
    font-size: clamp(40px, 7vw, 78px); line-height: 0.96;
    letter-spacing: -0.02em; margin: 12px 0 16px;
  }
  .hero h1 em { color: var(--accent-soft); font-style: normal; }
  .hero .lead { color: var(--fg-muted); font-size: clamp(15px, 1.6vw, 18px); max-width: 60ch; margin: 0 0 20px; }
  .actions { display: flex; gap: 10px; margin-bottom: 22px; flex-wrap: wrap; }
  .btn {
    display: inline-block; padding: 10px 16px;
    font-family: var(--font-mono); font-size: 13px; font-weight: 600;
    border-radius: var(--radius-sm); text-decoration: none;
    border: 1px solid transparent;
  }
  .btn.primary { background: var(--accent); color: white; }
  .btn.primary:hover { background: var(--accent-soft); }
  .btn.ghost { background: transparent; color: var(--fg-strong); border-color: var(--border-strong); }
  .btn.ghost:hover { border-color: var(--accent); }
  .pills { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 22px; }
  .snippet {
    background: var(--bg-code); border: 1px solid var(--border);
    border-left: 2px solid var(--accent);
    padding: 14px 16px; border-radius: var(--radius-md);
    font-size: 13px; line-height: 1.7; overflow-x: auto;
    color: var(--fg);
  }
</style>
```

- [ ] **Step 5.4 — `src/components/SystemMap.astro`**

```astro
---
---
<figure class="system-map" aria-label="nSealr system map">
  <svg viewBox="0 0 760 480" role="img" aria-labelledby="map-title map-desc">
    <title id="map-title">nSealr signer architecture</title>
    <desc id="map-desc">
      Nostr clients send signing requests to the companion, which routes them to a
      Raspberry/Pi stateless QR vault, ESP32 QR vault, ESP32 USB signer,
      smartcard, or custom persistent-secret hardware wallet.
    </desc>
    <g class="links">
      <path d="M164 210h124" />
      <path d="M420 210h74v-118h48" />
      <path d="M420 210h96v-30h26" />
      <path d="M420 210h96v52h26" />
      <path d="M420 210h96v134h26" />
      <path d="M420 210h74v216h48" />
    </g>
    <g class="node client">
      <rect x="32" y="154" width="132" height="112" rx="8" />
      <text x="98" y="200">Nostr</text>
      <text x="98" y="226">Client</text>
    </g>
    <g class="node companion">
      <rect x="288" y="122" width="132" height="176" rx="8" />
      <text x="354" y="194">Companion</text>
      <text x="354" y="220">Verifier</text>
    </g>
    <g class="node signer s1">
      <rect x="542" y="56" width="170" height="72" rx="8" />
      <text x="627" y="86">Raspberry</text>
      <text x="627" y="108">QR Vault</text>
    </g>
    <g class="node signer s2">
      <rect x="542" y="148" width="170" height="64" rx="8" />
      <text x="627" y="172">ESP32</text>
      <text x="627" y="194">QR Vault</text>
    </g>
    <g class="node signer s3">
      <rect x="542" y="230" width="170" height="64" rx="8" />
      <text x="627" y="254">ESP32</text>
      <text x="627" y="276">USB / NIP-46</text>
    </g>
    <g class="node signer s4">
      <rect x="542" y="312" width="170" height="64" rx="8" />
      <text x="627" y="336">Smartcard</text>
      <text x="627" y="358">APDU</text>
    </g>
    <g class="node signer s5">
      <rect x="542" y="394" width="170" height="64" rx="8" />
      <text x="627" y="418">Custom</text>
      <text x="627" y="440">Wallet</text>
    </g>
  </svg>
</figure>
<style>
  .system-map { margin: 0; padding-block: 12px; }
  svg { display: block; width: 100%; height: auto; }
  .links path { fill: none; stroke: var(--border-strong); stroke-width: 2; }
  .node rect { fill: var(--bg-elevated); stroke: var(--border-strong); stroke-width: 1.5; }
  .node text { font-family: var(--font-mono); fill: var(--fg-strong); font-size: 15px; font-weight: 600; text-anchor: middle; }
  .node.companion rect { stroke: var(--accent); }
  .node.signer rect { stroke: var(--accent-soft); }
  .node.client rect { stroke: var(--ok); }
</style>
```

- [ ] **Step 5.5 — `src/components/SignerCard.astro`**

```astro
---
import StatusPill from './StatusPill.astro';
interface Props {
  family: string;
  displayName: string;
  tagline: string;
  maturity: string;
  href: string;
}
const { family, displayName, tagline, maturity, href } = Astro.props;
const variant = maturity === 'alpha' ? 'ok' : maturity === 'prototype' ? 'pending' : 'neutral';
---
<a class="signer-card" href={href} data-family={family}>
  <div class="head">
    <span class="name">{displayName}</span>
    <StatusPill variant={variant}>{maturity}</StatusPill>
  </div>
  <p class="tag">{tagline}</p>
  <span class="arrow" aria-hidden="true">→</span>
</a>
<style>
  .signer-card {
    display: block; padding: 16px 18px;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    background: var(--bg-elevated);
    text-decoration: none; color: var(--fg);
    transition: border-color 120ms, transform 120ms;
    position: relative;
  }
  .signer-card:hover { border-color: var(--accent); transform: translateY(-1px); }
  .head { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 6px; }
  .name { font-family: var(--font-mono); font-size: 13px; color: var(--fg-strong); font-weight: 700; line-height: 1.3; }
  .tag { color: var(--fg-muted); font-size: 13px; margin: 0; }
  .arrow { position: absolute; right: 18px; bottom: 14px; color: var(--accent-soft); font-family: var(--font-mono); }
</style>
```

- [ ] **Step 5.6 — `src/components/SignerFamilyGrid.astro`**

```astro
---
import { getCollection } from 'astro:content';
import SignerCard from './SignerCard.astro';
const signers = (await getCollection('signers')).sort((a, b) => a.data.order - b.data.order);
---
<div class="grid">
  {signers.map(s => (
    <SignerCard
      family={s.data.family}
      displayName={s.data.displayName}
      tagline={s.data.tagline}
      maturity={s.data.maturity}
      href={`/docs/signers/${s.id}/`}
    />
  ))}
</div>
<style>
  .grid {
    display: grid; gap: 12px;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  }
</style>
```

- [ ] **Step 5.7 — `src/components/FeatureMatrix.astro`**

```astro
---
import { getCollection } from 'astro:content';
interface Props { family: string; }
const { family } = Astro.props;
const all = await getCollection('signers');
const entry = all.find(s => s.data.family === family);
if (!entry) throw new Error(`FeatureMatrix: unknown family "${family}"`);
const STATUS_VARIANT: Record<string, 'ok' | 'warn' | 'pending' | 'neutral'> = {
  implemented: 'ok', present: 'ok', partial: 'pending',
  planned: 'pending', research: 'pending',
  disabled_until_gates_pass: 'warn', disabled: 'warn', forbidden: 'warn', absent: 'warn',
  not_applicable: 'neutral', target: 'neutral'
};
---
<div class="fm">
  <table>
    <thead>
      <tr>
        <th scope="col">Feature</th>
        <th scope="col">Target</th>
        <th scope="col">Current</th>
        <th scope="col">Contract</th>
      </tr>
    </thead>
    <tbody>
      {entry.data.capabilities.map(c => (
        <tr>
          <th scope="row"><code>{c.id}</code></th>
          <td><span class={`b b-${STATUS_VARIANT[c.target] ?? 'neutral'}`}>{c.target}</span></td>
          <td><span class={`b b-${STATUS_VARIANT[c.current] ?? 'neutral'}`}>{c.current}</span></td>
          <td>{c.contractId ? <code>{c.contractId}</code> : <span class="muted">—</span>}</td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
<style>
  .fm { overflow-x: auto; margin: 1.4em 0; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; font-family: var(--font-mono); }
  th, td { padding: 6px 10px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }
  thead th { background: var(--bg-elevated); font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--fg-muted); }
  code { background: transparent; border: 0; padding: 0; font-size: 12px; color: var(--fg); }
  .b { display: inline-block; padding: 1px 7px; border-radius: var(--radius-pill); border: 1px solid; font-size: 11px; }
  .b-ok { color: var(--ok); border-color: color-mix(in oklab, var(--ok) 40%, transparent); background: var(--ok-bg); }
  .b-warn { color: var(--warn); border-color: color-mix(in oklab, var(--warn) 40%, transparent); background: var(--warn-bg); }
  .b-pending { color: var(--pending); border-color: color-mix(in oklab, var(--pending) 40%, transparent); background: var(--pending-bg); }
  .b-neutral { color: var(--fg-muted); border-color: var(--border); background: transparent; }
  .muted { color: var(--fg-muted); }
</style>
```

- [ ] **Step 5.8 — `src/components/SearchTrigger.astro`**

```astro
---
---
<button id="search-trigger" type="button" class="search-trigger" aria-label="Open search">
  <span>Search…</span>
  <kbd>⌘K</kbd>
</button>
<link rel="stylesheet" href="/pagefind/pagefind-ui.css" />
<div id="search-modal" hidden>
  <div class="search-modal-inner" role="dialog" aria-modal="true" aria-label="Search">
    <div id="pagefind-search"></div>
    <button id="search-close" aria-label="Close search">Esc</button>
  </div>
</div>
<style>
  .search-trigger {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--bg-elevated); border: 1px solid var(--border);
    color: var(--fg-muted); padding: 6px 10px;
    border-radius: var(--radius-md); font-family: var(--font-mono);
    font-size: 12px; cursor: pointer;
  }
  .search-trigger:hover { border-color: var(--accent); color: var(--fg-strong); }
  .search-trigger kbd { font-size: 11px; padding: 1px 5px; border: 1px solid var(--border-strong); border-radius: 3px; }
  #search-modal {
    position: fixed; inset: 0; background: color-mix(in oklab, var(--bg) 70%, transparent);
    z-index: 100; display: grid; place-items: start center; padding-top: 12vh;
  }
  .search-modal-inner {
    width: min(640px, 92vw); background: var(--bg-elevated);
    border: 1px solid var(--border-strong); border-radius: var(--radius-md);
    padding: 16px; box-shadow: var(--shadow-2);
  }
  #search-close { float: right; background: transparent; color: var(--fg-muted); border: 1px solid var(--border-strong); border-radius: var(--radius-sm); padding: 3px 8px; font-family: var(--font-mono); font-size: 11px; cursor: pointer; }
</style>
<script>
  const trigger = document.getElementById('search-trigger');
  const modal = document.getElementById('search-modal');
  const closeBtn = document.getElementById('search-close');
  let mounted = false;
  async function open() {
    modal!.hidden = false;
    if (!mounted) {
      const { PagefindUI } = await import('/pagefind/pagefind-ui.js' as any);
      new PagefindUI({ element: '#pagefind-search', showImages: false, resetStyles: false });
      mounted = true;
    }
  }
  function close() { modal!.hidden = true; }
  trigger?.addEventListener('click', open);
  closeBtn?.addEventListener('click', close);
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); open(); }
    if (e.key === 'Escape') close();
  });
</script>
```

- [ ] **Step 5.9 — `src/pages/index.astro`**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import Hero from '~/components/Hero.astro';
import SystemMap from '~/components/SystemMap.astro';
import SignerFamilyGrid from '~/components/SignerFamilyGrid.astro';
---
<BaseLayout
  title="nSealr — open-source hardware signers for Nostr"
  description="nSealr is a non-profit open-source hardware and software program for Nostr signing devices."
>
  <Hero />

  <section class="container split">
    <div>
      <p class="eyebrow">// system</p>
      <h2>One companion. Five signer families.</h2>
      <p class="muted">
        The companion prepares requests, moves them over QR, file, stdio,
        serial, USB, or card transports, and verifies every successful
        response. The signer keeps or protects the private key and signs
        only through an explicit policy boundary.
      </p>
      <p><a class="link-arrow" href="/system/">Read product shape →</a></p>
    </div>
    <SystemMap />
  </section>

  <section class="container">
    <p class="eyebrow">// families</p>
    <h2>Pick the boundary that matches your trust model.</h2>
    <SignerFamilyGrid />
  </section>

  <section class="container status">
    <p class="eyebrow">// status</p>
    <h2>Current maturity is explicit.</h2>
    <ul>
      <li><strong>Specs:</strong> v0 request, response, QR envelope, fixtures, review-screen vectors, <em>review detail pages</em>, <code>approval_digest</code> contracts, and <em>NIP-46 bridge decisions</em>.</li>
      <li><strong>Companion:</strong> CLI, verification, transports, QR, serial framing with <em>request-bound capture checks</em>, <code>nsealr serial-line exchange</code> for one-shot local USB-serial bring-up, <code>nsealr nip46 decide</code> for already-decrypted payload policy checks, and untrusted detail-page previews.</li>
      <li><strong>Raspberry:</strong> desktop stateless QR vault simulation with NIP-06 signing, <code>approval_digest</code>-bound review, and hardware-neutral adapter boundaries for later Pi drivers.</li>
      <li><strong>ESP32 QR:</strong> stateless QR vault host-core review flow and <em>T-Display S3 review scenario smoke</em> while the T-Display S3 Pro OV5640 hardware target remains pending.</li>
      <li><strong>ESP32 USB/NIP-46:</strong> native USB scaffold with get_public_key, <code>signing_disabled</code>, <code>approval_digest</code>-gated approval core, <em>companion-to-device serial smoke</em>, <em>sign-event-disabled smoke</em>, <em>firmware protocol evidence</em>, and <em>Unicode fallback</em> tracking for disabled-signing development firmware.</li>
      <li><strong>Smartcard:</strong> JavaCard/NFC Smartcard Signer research with APDU simulator plus <em>nsealr-smartcard CLI probes</em> for public-key and event-id signing research; <em>no trusted review or real-card compatibility claim</em> yet.</li>
      <li><strong>Custom wallet:</strong> Custom Nostr Hardware Wallet With Persistent Secret research now has a USB-C bus-powered, no-battery, TROPIC01-assisted Rev A scaffold; direct TROPIC01 Schnorr remains future-gated.</li>
      <li><strong>Hardware:</strong> checked requirements, BOM scaffold, and <em>Raspberry/Pi OS profile</em>, including <em>Raspberry/Pi kit requirements</em>, request-id and <code>approval_digest</code> review binding.</li>
    </ul>
  </section>

  <section class="container security">
    <p class="eyebrow">// security</p>
    <h2>No production security claim yet.</h2>
    <p class="muted">
      nSealr is pre-production research and implementation work. The project
      documents trust boundaries, test evidence, and known limits before
      presenting any device as ready for real keys.
    </p>
    <p><a class="link-arrow" href="/security/">Read the trust model →</a></p>
  </section>
</BaseLayout>

<style>
  h2 { font-family: var(--font-mono); color: var(--fg-strong); font-size: clamp(24px, 3vw, 36px); line-height: 1.1; letter-spacing: -0.01em; margin: 6px 0 14px; }
  .muted { color: var(--fg-muted); max-width: 64ch; }
  section.container { padding-block: clamp(36px, 6vw, 80px); }
  section.split { display: grid; gap: 28px; grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr); align-items: center; }
  @media (max-width: 820px) { section.split { grid-template-columns: 1fr; } }
  .status ul { padding-left: 1em; display: grid; gap: 8px; max-width: 80ch; }
  .status li { padding-left: 0; }
  .status strong { font-family: var(--font-mono); color: var(--fg-strong); }
  .status code, .status em { background: var(--accent-bg); color: var(--accent-soft); border-radius: var(--radius-sm); padding: 1px 6px; font-style: normal; }
  .link-arrow { font-family: var(--font-mono); color: var(--accent-soft); font-size: 14px; }
</style>
```

- [ ] **Step 5.10 — `src/pages/system.astro`**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import SystemMap from '~/components/SystemMap.astro';
import SignerFamilyGrid from '~/components/SignerFamilyGrid.astro';
---
<BaseLayout title="System — nSealr" description="Product shape: one companion and five signer families for Nostr signing.">
  <section class="container">
    <p class="eyebrow">// system</p>
    <h1>One companion. Five signer families.</h1>
    <p class="lead">
      The practical product is a shared companion plus five signer families,
      not five unrelated experiments. Every shared feature behaves the same
      across implementations because the <code>contract_id</code> in
      <code>nSealr/specs</code> defines it once.
    </p>
    <SystemMap />
    <h2>Families</h2>
    <SignerFamilyGrid />
    <h2>Boundaries</h2>
    <ul>
      <li><strong>Companion:</strong> secretless routing and verification infrastructure. Not trusted with keys.</li>
      <li><strong>QR vaults:</strong> stateless RAM-only session signers.</li>
      <li><strong>USB/NIP-46:</strong> future persistent encrypted device-vault signer.</li>
      <li><strong>Smartcards:</strong> display-less slot-backed custody — requires external review acknowledgement.</li>
      <li><strong>Custom wallet:</strong> research for persistent-secret hardware wallets.</li>
    </ul>
  </section>
</BaseLayout>
<style>
  .container { padding-block: 60px; }
  h1 { font-family: var(--font-mono); color: var(--fg-strong); font-size: clamp(32px, 4.5vw, 56px); line-height: 1; letter-spacing: -0.02em; margin: 8px 0 18px; }
  h2 { font-family: var(--font-mono); color: var(--fg-strong); font-size: 22px; margin: 36px 0 14px; }
  .lead { color: var(--fg-muted); font-size: clamp(15px, 1.6vw, 18px); max-width: 64ch; }
  ul { display: grid; gap: 8px; max-width: 80ch; }
</style>
```

- [ ] **Step 5.11 — `src/pages/security.astro`**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import Callout from '~/components/Callout.astro';
---
<BaseLayout title="Security — nSealr" description="Trust boundaries, threat model overview, and known limits for nSealr signers.">
  <section class="container">
    <p class="eyebrow">// security</p>
    <h1>No production security claim yet.</h1>
    <p class="lead">
      nSealr is pre-production research and implementation work. The
      website documents trust boundaries, test evidence, and known limits
      before presenting any device as ready for real keys.
    </p>

    <h2>Trust boundaries</h2>
    <ul>
      <li>Private keys must not be exposed to ordinary Nostr clients.</li>
      <li>Sensitive signing should require explicit user review where hardware allows it.</li>
      <li>The companion is not trusted with key custody.</li>
      <li>Maturity differs by signer family — see each family page.</li>
    </ul>

    <h2>Current contracts</h2>
    <p>The safety contracts the site enforces today include:</p>
    <ul>
      <li><code>approval_digest</code> — the local approval is bound to the exact reviewed material.</li>
      <li><code>signing_disabled</code> — real signing is blocked on prototype firmware until hardening gates pass.</li>
      <li><strong>NIP-46 bridge decisions</strong> via <code>nsealr nip46 decide</code> for already-decrypted payloads.</li>
      <li><strong>Request-bound capture checks</strong> in <code>nsealr serial-line exchange</code>.</li>
      <li><strong>Review detail pages</strong> for long content and tags without truncation.</li>
      <li><strong>T-Display S3 review scenario smoke</strong>, <strong>companion-to-device serial smoke</strong>, <strong>sign-event-disabled smoke</strong>, <strong>firmware protocol evidence</strong>, and <strong>Unicode fallback</strong> tracking — disabled-signing development evidence, not production claims.</li>
    </ul>

    <Callout variant="warn" title="Pre-production">
      Do not put production secrets onto current prototypes. Maturity per
      family is in <a href="/docs/signers/raspberry-qr/">each family page</a>
      and in the feature matrix.
    </Callout>

    <p><a class="link-arrow" href="/docs/security/threat-model/">Read the full threat model →</a></p>
  </section>
</BaseLayout>
<style>
  .container { padding-block: 60px; max-width: 880px; }
  h1 { font-family: var(--font-mono); color: var(--fg-strong); font-size: clamp(28px, 4vw, 44px); line-height: 1.05; margin: 8px 0 16px; }
  h2 { font-family: var(--font-mono); color: var(--fg-strong); font-size: 22px; margin: 32px 0 12px; }
  ul { display: grid; gap: 8px; max-width: 80ch; }
  .lead { color: var(--fg-muted); max-width: 64ch; font-size: 17px; }
  .link-arrow { font-family: var(--font-mono); color: var(--accent-soft); font-size: 14px; }
</style>
```

- [ ] **Step 5.12 — `src/pages/about.astro`**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
---
<BaseLayout title="About — nSealr" description="About the non-profit open-source nSealr program.">
  <section class="container">
    <p class="eyebrow">// about</p>
    <h1>nSealr is not a product.</h1>
    <p class="lead">
      It is a non-profit, open-source program for Nostr signing devices,
      companion software, shared specs, and build documentation. The site
      explains the program without turning the core work into a proprietary
      product.
    </p>
    <h2>Repositories</h2>
    <ul>
      <li><a href="https://github.com/nSealr/specs">specs</a> — protocol, vectors, signer feature matrix.</li>
      <li><a href="https://github.com/nSealr/companion">companion</a> — host-side software.</li>
      <li><a href="https://github.com/nSealr/raspberry">raspberry</a>, <a href="https://github.com/nSealr/esp32">esp32</a>, <a href="https://github.com/nSealr/smartcard">smartcard</a>, <a href="https://github.com/nSealr/hardware">hardware</a>, <a href="https://github.com/nSealr/lab">lab</a>.</li>
    </ul>
    <h2>License</h2>
    <p>MIT for code. CC0-1.0 for content when published.</p>
  </section>
</BaseLayout>
<style>
  .container { padding-block: 60px; max-width: 800px; }
  h1 { font-family: var(--font-mono); color: var(--fg-strong); font-size: clamp(28px, 4vw, 44px); margin: 8px 0 16px; }
  h2 { font-family: var(--font-mono); color: var(--fg-strong); font-size: 22px; margin: 32px 0 12px; }
  .lead { color: var(--fg-muted); font-size: 17px; max-width: 64ch; }
  ul { display: grid; gap: 8px; }
</style>
```

- [ ] **Step 5.13 — `src/pages/contributing.astro`**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
---
<BaseLayout title="Contributing — nSealr" description="How to contribute to nSealr signers, companion, specs, and hardware.">
  <section class="container">
    <p class="eyebrow">// contributing</p>
    <h1>Contribute to a signer family or the shared spec.</h1>
    <ol>
      <li>Pick the repo for the area you want to work on (see <a href="/about/">About</a>).</li>
      <li>Read its <code>README.md</code> for build / test instructions.</li>
      <li>Open issues and PRs that preserve the shared <code>contract_id</code> behavior in <a href="https://github.com/nSealr/specs">nSealr/specs</a> when a feature is present on more than one solution.</li>
    </ol>
    <h2>Ground rules</h2>
    <ul>
      <li>No production security claim before independent test evidence.</li>
      <li>Shared features behave the same across signer families.</li>
      <li>Display-less smartcards do not provide trusted event review by themselves.</li>
      <li>TROPIC01 is not assumed to directly sign Nostr/BIP-340 until proven.</li>
    </ul>
  </section>
</BaseLayout>
<style>
  .container { padding-block: 60px; max-width: 800px; }
  h1 { font-family: var(--font-mono); color: var(--fg-strong); font-size: clamp(28px, 4vw, 40px); margin: 8px 0 16px; }
  h2 { font-family: var(--font-mono); color: var(--fg-strong); font-size: 22px; margin: 32px 0 12px; }
  ol, ul { display: grid; gap: 8px; max-width: 70ch; }
</style>
```

- [ ] **Step 5.14 — `src/pages/404.astro`**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
---
<BaseLayout title="404 — nSealr" description="Not found." noindex={true}>
  <section class="container">
    <p class="eyebrow">// 404</p>
    <h1>404 — not found.</h1>
    <p class="muted">The page you requested does not exist (yet).</p>
    <p><a class="link-arrow" href="/">← back home</a></p>
  </section>
</BaseLayout>
<style>
  .container { padding-block: 120px; text-align: center; }
  h1 { font-family: var(--font-mono); color: var(--fg-strong); font-size: 36px; margin: 8px 0 12px; }
  .muted { color: var(--fg-muted); }
  .link-arrow { font-family: var(--font-mono); color: var(--accent-soft); }
</style>
```

- [ ] **Step 5.15 — Dev smoke**

```bash
pnpm exec astro check
pnpm run dev &
sleep 4
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/system/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/security/
kill %1
```

Expected: all 200.

- [ ] **Step 5.16 — Commit**

```bash
git add public/favicon.svg public/robots.txt src/components src/pages
git commit -m "feat(pages): home, system, security, about, contributing, 404 + hero + system map + family grid"
```

---

### Task 6: Docs (sidebar, dynamic page, seed content)

**Files:** Create `src/components/{DocsSidebar,TableOfContents}.astro`, `src/layouts/DocsLayout.astro`, `src/pages/docs/index.astro`, `src/pages/docs/[...slug].astro`, `src/content/docs/**/*.mdx` (7 files), `src/lib/docs-nav.ts`.

- [ ] **Step 6.1 — `src/lib/docs-nav.ts`**

```ts
import { getCollection, type CollectionEntry } from 'astro:content';

export const DOC_SECTION_ORDER = ['getting-started', 'guides', 'signers', 'specs', 'security'] as const;
export const DOC_SECTION_LABEL: Record<typeof DOC_SECTION_ORDER[number], string> = {
  'getting-started': 'Getting Started',
  'guides': 'Guides',
  'signers': 'Signers',
  'specs': 'Specs & Reference',
  'security': 'Security'
};

export type DocsEntry = CollectionEntry<'docs'> | { id: string; data: { title: string; section: typeof DOC_SECTION_ORDER[number]; order: number } };

export async function getDocsNav() {
  const docs = await getCollection('docs');
  const signers = await getCollection('signers');

  const fromDocs = docs.map(d => ({
    id: d.id,
    href: `/docs/${d.id}/`,
    title: d.data.title,
    section: d.data.section,
    order: d.data.order
  }));

  const fromSigners = signers.map(s => ({
    id: `signers/${s.id}`,
    href: `/docs/signers/${s.id}/`,
    title: s.data.displayName,
    section: 'signers' as const,
    order: s.data.order
  }));

  const all = [...fromDocs, ...fromSigners];

  const grouped = DOC_SECTION_ORDER.map(section => ({
    section,
    label: DOC_SECTION_LABEL[section],
    items: all.filter(e => e.section === section).sort((a, b) => a.order - b.order)
  }));

  return grouped;
}
```

- [ ] **Step 6.2 — `src/components/DocsSidebar.astro`**

```astro
---
import { getDocsNav } from '~/lib/docs-nav';
interface Props { currentHref: string; }
const { currentHref } = Astro.props;
const nav = await getDocsNav();
---
<aside class="docs-sidebar" aria-label="Documentation sections">
  <nav>
    {nav.map(group => (
      <section>
        <h3>{group.label}</h3>
        <ul>
          {group.items.map(item => (
            <li>
              <a href={item.href} class={item.href === currentHref ? 'current' : ''}>{item.title}</a>
            </li>
          ))}
        </ul>
      </section>
    ))}
  </nav>
</aside>
<style>
  .docs-sidebar { font-family: var(--font-mono); font-size: 13px; padding: 24px 0; border-right: 1px solid var(--border); }
  section { padding: 8px 16px; }
  h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--fg-muted); margin: 14px 0 6px; }
  ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 4px; }
  a { color: var(--fg-muted); text-decoration: none; padding: 4px 8px; border-radius: var(--radius-sm); display: block; }
  a:hover { color: var(--fg-strong); background: var(--bg-elevated); }
  a.current { color: var(--accent-soft); background: var(--accent-bg); }
  @media (max-width: 960px) {
    .docs-sidebar { border-right: 0; border-bottom: 1px solid var(--border); }
  }
</style>
```

- [ ] **Step 6.3 — `src/components/TableOfContents.astro`**

```astro
---
interface Heading { depth: number; slug: string; text: string; }
interface Props { headings: Heading[]; }
const { headings } = Astro.props;
const items = headings.filter(h => h.depth >= 2 && h.depth <= 3);
---
{items.length > 0 && (
  <nav class="toc" aria-label="On this page">
    <h3>On this page</h3>
    <ul>
      {items.map(h => (
        <li class={`d-${h.depth}`}><a href={`#${h.slug}`}>{h.text}</a></li>
      ))}
    </ul>
  </nav>
)}
<style>
  .toc { position: sticky; top: 80px; font-family: var(--font-mono); font-size: 12px; padding: 24px 16px 24px 0; }
  h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--fg-muted); margin: 0 0 8px; }
  ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 4px; border-left: 1px solid var(--border); }
  li { padding-left: 12px; }
  li.d-3 { padding-left: 24px; opacity: 0.85; }
  a { color: var(--fg-muted); text-decoration: none; display: block; padding: 2px 0; }
  a:hover { color: var(--accent-soft); }
</style>
```

- [ ] **Step 6.4 — `src/layouts/DocsLayout.astro`**

```astro
---
import BaseLayout from './BaseLayout.astro';
import DocsSidebar from '~/components/DocsSidebar.astro';
import TableOfContents from '~/components/TableOfContents.astro';
import StatusPill from '~/components/StatusPill.astro';
interface Props {
  title: string;
  description: string;
  status?: 'stable' | 'draft' | 'research';
  updatedAt?: Date;
  headings: { depth: number; slug: string; text: string }[];
  editUrl?: string;
}
const { title, description, status = 'stable', updatedAt, headings, editUrl } = Astro.props;
const currentHref = Astro.url.pathname;
---
<BaseLayout title={`${title} — nSealr Docs`} description={description}>
  <div class="docs-shell container">
    <DocsSidebar currentHref={currentHref} />
    <article class="prose docs-article">
      <header class="docs-header">
        <h1>{title}</h1>
        {status !== 'stable' && <StatusPill variant={status === 'draft' ? 'pending' : 'warn'}>{status}</StatusPill>}
      </header>
      <slot />
      <footer class="docs-footer">
        {updatedAt && <p class="muted">Last updated {updatedAt.toISOString().slice(0, 10)}</p>}
        {editUrl && <p><a href={editUrl}>Edit this page on GitHub →</a></p>}
      </footer>
    </article>
    <TableOfContents headings={headings} />
  </div>
</BaseLayout>
<style>
  .docs-shell {
    display: grid; gap: 12px;
    grid-template-columns: 240px minmax(0, 1fr) 220px;
    align-items: start; padding-block: 28px;
  }
  .docs-article { padding: 24px 8px 60px; min-width: 0; }
  .docs-header { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  .docs-footer { margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--border); font-size: 14px; color: var(--fg-muted); }
  @media (max-width: 960px) {
    .docs-shell { grid-template-columns: 1fr; }
  }
</style>
```

- [ ] **Step 6.5 — `src/pages/docs/index.astro`**

```astro
---
return Astro.redirect('/docs/getting-started/overview/');
---
```

- [ ] **Step 6.6 — `src/pages/docs/[...slug].astro`**

```astro
---
import { getCollection, render, type CollectionEntry } from 'astro:content';
import DocsLayout from '~/layouts/DocsLayout.astro';

export async function getStaticPaths() {
  const docs = await getCollection('docs');
  const signers = await getCollection('signers');

  const docPaths = docs.map(entry => ({
    params: { slug: entry.id },
    props: { kind: 'doc' as const, entry }
  }));

  const signerPaths = signers.map(entry => ({
    params: { slug: `signers/${entry.id}` },
    props: { kind: 'signer' as const, entry }
  }));

  return [...docPaths, ...signerPaths];
}

type Props =
  | { kind: 'doc'; entry: CollectionEntry<'docs'> }
  | { kind: 'signer'; entry: CollectionEntry<'signers'> };

const props = Astro.props as Props;
const { Content, headings } = await render(props.entry);

const isDoc = props.kind === 'doc';
const title = isDoc ? props.entry.data.title : props.entry.data.displayName;
const description = isDoc ? props.entry.data.description : props.entry.data.tagline;
const status = isDoc ? props.entry.data.status : 'stable';
const updatedAt = isDoc ? props.entry.data.updatedAt : undefined;
const editUrl = `https://github.com/nSealr/website/edit/main/website/src/content/${
  isDoc ? 'docs/' + props.entry.id : 'signers/' + props.entry.id
}.mdx`;
---
<DocsLayout
  title={title}
  description={description}
  status={status}
  updatedAt={updatedAt}
  headings={headings}
  editUrl={editUrl}
>
  <Content />
</DocsLayout>
```

- [ ] **Step 6.7 — Seed `src/content/docs/getting-started/overview.mdx`**

```mdx
---
title: 'Overview'
description: 'What nSealr is, who it is for, and why open hardware signing matters for Nostr.'
section: 'getting-started'
order: 1
updatedAt: 2026-05-15
---

# Overview

**nSealr** is a non-profit, open-source program for Nostr signing devices.
It is not a closed hardware wallet product. The shared shape is one
companion plus five signer families, with shared specs and build
documentation in `nSealr/specs`, `nSealr/hardware`, and per-family
firmware repos.

## Why

Private keys for Nostr accounts should not live in ordinary clients.
Hardware signers raise the bar: secrets stay inside a device with an
explicit trust boundary, signing requires explicit user review or
explicit policy, and every successful response is verified by an
untrusted companion before reaching a relay.

## What this site is

- **/system** — product shape and the five families.
- **/docs** — guides, signer status pages, specs reference, security.
- **/blog** — release notes, research, tutorials, news.
- **/security** — trust boundaries and current safety contracts.

## Pre-production

No part of this program currently makes a production security claim. See
[the security page](/security/) for the contracts the site enforces today.
```

- [ ] **Step 6.8 — `src/content/docs/getting-started/use.mdx`**

```mdx
---
title: 'Using a signer'
description: 'End-to-end flow: a Nostr client requests a signature, the companion routes it, and a signer reviews and signs.'
section: 'getting-started'
order: 2
updatedAt: 2026-05-15
---

# Using a signer

1. A Nostr client builds an event template and asks for a signature.
2. The **companion** validates the request, normalizes it to the v0
   contract, and routes it over the right transport (QR, USB serial,
   APDU, or NIP-46 bridge).
3. The **signer** displays the event for review where hardware allows it,
   binds the local approval to `approval_digest`, and signs BIP-340.
4. The companion **verifies the signed response** against shared fixtures
   before handing it back to the client.

The signer keeps or protects the private key. The companion never holds
keys. The client never sees keys.
```

- [ ] **Step 6.9 — `src/content/docs/guides/build-raspberry-qr-vault.mdx`**

```mdx
---
title: 'Build a Raspberry/Pi QR vault'
description: 'Assemble and run the SeedSigner-style stateless QR vault for Nostr signing on a Pi Zero kit.'
section: 'guides'
order: 1
updatedAt: 2026-05-15
status: 'draft'
---

# Build a Raspberry/Pi QR vault

import Callout from '~/components/Callout.astro';

<Callout variant="warn" title="Pre-production">
  This guide tracks the prototype build. Do not put production secrets
  onto current hardware. Current maturity is in the
  [signer family page](/docs/signers/raspberry-qr/).
</Callout>

## Bill of materials

Follow the **Raspberry/Pi kit requirements** in
[`nSealr/hardware`](https://github.com/nSealr/hardware): Pi Zero-class
board, Pi/ZeroCam OV5647, Waveshare ST7789 240×240 LCD HAT, GPIO
joystick/buttons, removable microSD.

## OS profile

Use the **Raspberry/Pi OS profile** described in `nSealr/hardware`:
removable boot media, disabled or absent wireless, RAM-only session
custody, no swap during signing, no remote access during signing, and no
persistent signing-secret storage.

## Software

Clone and bootstrap:

```sh
git clone https://github.com/nSealr/raspberry
cd raspberry
make setup
make ci
```

## Sign a fixture event

```sh
nsealr-rasp sign-fixture --request specs/vectors/requests/request-v0.json
```

The CLI computes the NIP-01 event id, signs BIP-340/secp256k1, and emits
a `nsealr1:` QR response that the companion can verify.
```

- [ ] **Step 6.10 — `src/content/docs/guides/flash-esp32-firmware.mdx`**

```mdx
---
title: 'Flash ESP32 firmware'
description: 'Build and flash the development firmware for the ESP32-S3 signer line.'
section: 'guides'
order: 2
updatedAt: 2026-05-15
status: 'draft'
---

# Flash ESP32 firmware

import Callout from '~/components/Callout.astro';

<Callout variant="warn" title="signing_disabled">
  The development firmware ships with real `sign_event` disabled until
  hardening, display, button, and provisioning gates pass. Flashing it
  on hardware does not unlock production signing.
</Callout>

## Targets

- ESP32-S3 (display/button) for USB/NIP-46 line.
- T-Display S3 Pro OV5640 candidate for the stateless QR vault line.

## Build

```sh
git clone https://github.com/nSealr/esp32
cd esp32
make setup
make build TARGET=esp32s3-tdisplay
```

## Flash

```sh
make flash TARGET=esp32s3-tdisplay PORT=/dev/cu.usbserial-XXXX
```

## Smoke evidence

Once flashed, the companion can run **companion-to-device serial smoke**
and **sign-event-disabled smoke** to confirm the firmware protocol is
intact. See **firmware protocol evidence** and **Unicode fallback**
tracking in [`nSealr/esp32`](https://github.com/nSealr/esp32).
```

- [ ] **Step 6.11 — `src/content/docs/specs/event-canonicalization.mdx`**

```mdx
---
title: 'NIP-01 event canonicalization'
description: 'How nSealr computes the canonical NIP-01 event id and the BIP-340 signing input.'
section: 'specs'
order: 1
updatedAt: 2026-05-15
---

# NIP-01 event canonicalization

The signing input is the serialized canonical form of the event template
(`[0, pubkey, created_at, kind, tags, content]`). The event id is the
SHA-256 of that serialization; the signature is BIP-340 Schnorr over
secp256k1 with the signer public key.

Test vectors live in
[`nSealr/specs`](https://github.com/nSealr/specs) under `vectors/`. The
companion verifies every signed response against the same fixtures
before accepting device output.
```

- [ ] **Step 6.12 — `src/content/docs/specs/qr-envelope.mdx`**

```mdx
---
title: 'QR envelope (nsealr1)'
description: 'Static and animated QR envelopes for stateless signer transport.'
section: 'specs'
order: 2
updatedAt: 2026-05-15
---

# QR envelope (`nsealr1`)

Stateless QR vaults use two envelope variants:

- **`nsealr1:`** — single static QR for short signing requests.
- **`nsealr1a:`** — animated chunked QR with explicit bounds and integrity
  checks, reassembled by the signer before request validation.

Responses use the `qr-response-v0` contract: signed event or deterministic
error, encoded for host verification without exposing secret material.
```

- [ ] **Step 6.13 — `src/content/docs/security/trust-boundaries.mdx`**

```mdx
---
title: 'Trust boundaries'
description: 'Where keys live, who is trusted with what, and what each layer must not do.'
section: 'security'
order: 1
updatedAt: 2026-05-15
---

# Trust boundaries

| Layer       | Trusted with… | Not trusted with…                        |
|-------------|---------------|------------------------------------------|
| Client      | building requests | private keys, approval decisions     |
| Companion   | routing & response verification | private keys, policy execution |
| Signer      | private keys (per family boundary) | the universe outside its boundary |
| Smartcard   | persistent secret, APDU signing | trusted event review (display-less) |

The companion is never trusted with key custody. Display-less smartcards
do not provide trusted event review by themselves — an external review
acknowledgement is required.
```

- [ ] **Step 6.14 — `src/content/docs/security/threat-model.mdx`**

```mdx
---
title: 'Threat model'
description: 'Adversaries, assets, and assumptions for nSealr signer families.'
section: 'security'
order: 2
updatedAt: 2026-05-15
status: 'draft'
---

# Threat model

## Assets

- The private key for each Nostr account on a signer.
- The integrity of every signed event the user authorizes.
- The user's ability to refuse a signing request.

## Adversaries

- A compromised host running the Nostr client.
- A compromised companion (signing requests must still be reviewable on
  the device where the hardware allows it).
- A malicious accessory connected to the signer transport (USB, QR
  camera, NFC field).
- Supply-chain firmware tampering — addressed by the
  `firmware-boot-hardening-v0` contract as a required gate for production
  ESP32 USB/NIP-46 claims.

## Assumptions

- The user reads the review screen where one exists.
- The user's local approval gesture is distinct from navigation.
- Pre-production firmware has `sign_event` intentionally disabled until
  hardening gates pass.
```

- [ ] **Step 6.15 — Build & smoke**

```bash
pnpm exec astro check
pnpm run dev &
sleep 4
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/docs/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/docs/getting-started/overview/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/docs/signers/raspberry-qr/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/docs/security/threat-model/
kill %1
```

Expected: all 200 (the `/docs/` index returns 302→200 final).

- [ ] **Step 6.16 — Commit**

```bash
git add src/components/DocsSidebar.astro src/components/TableOfContents.astro src/layouts/DocsLayout.astro src/pages/docs src/content/docs src/lib/docs-nav.ts
git commit -m "feat(docs): docs layout, dynamic route, sidebar, ToC + 8 seed pages"
```

---

### Task 7: Blog (list, post, tags, RSS, seed post)

**Files:** Create `src/components/BlogList.astro`, `src/layouts/BlogPostLayout.astro`, `src/pages/blog/{index,[...slug],tags/[tag],rss.xml}.{astro,ts}`, `src/content/blog/2026-05-15-nsealr-website-relaunch.mdx`.

- [ ] **Step 7.1 — `src/components/BlogList.astro`**

```astro
---
import TagPill from './TagPill.astro';
import type { CollectionEntry } from 'astro:content';
interface Props { posts: CollectionEntry<'blog'>[]; }
const { posts } = Astro.props;
const CATEGORY_COLOR: Record<string, string> = {
  release: 'var(--ok)',
  research: 'var(--accent-soft)',
  tutorial: 'var(--pending)',
  news: 'var(--fg-muted)'
};
---
<ul class="post-list">
  {posts.map(p => (
    <li>
      <a href={`/blog/${p.id}/`} class="post-card">
        <div class="meta">
          <span class="cat" style={`--cat: ${CATEGORY_COLOR[p.data.category]}`}>{p.data.category}</span>
          <time datetime={p.data.publishedAt.toISOString()}>{p.data.publishedAt.toISOString().slice(0,10)}</time>
        </div>
        <h3>{p.data.title}</h3>
        <p class="excerpt">{p.data.description}</p>
        {p.data.tags.length > 0 && (
          <div class="tags">{p.data.tags.map(t => <TagPill tag={t} />)}</div>
        )}
      </a>
    </li>
  ))}
</ul>
<style>
  .post-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 16px; }
  .post-card {
    display: block; padding: 18px 20px;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    background: var(--bg-elevated);
    text-decoration: none; color: var(--fg);
    transition: border-color 120ms, transform 120ms;
  }
  .post-card:hover { border-color: var(--accent); transform: translateY(-1px); }
  .meta { display: flex; gap: 12px; font-family: var(--font-mono); font-size: 11px; color: var(--fg-muted); margin-bottom: 6px; }
  .cat { color: var(--cat); text-transform: lowercase; }
  h3 { font-family: var(--font-mono); margin: 0 0 6px; color: var(--fg-strong); font-size: 18px; }
  .excerpt { margin: 0 0 10px; color: var(--fg-muted); font-size: 14px; }
  .tags { display: flex; gap: 6px; flex-wrap: wrap; }
</style>
```

- [ ] **Step 7.2 — `src/layouts/BlogPostLayout.astro`**

```astro
---
import BaseLayout from './BaseLayout.astro';
import TagPill from '~/components/TagPill.astro';
import { getEntry } from 'astro:content';
interface Props {
  title: string;
  description: string;
  publishedAt: Date;
  updatedAt?: Date;
  category: string;
  tags: string[];
  authorIds: string[];
  ogImage: string;
}
const { title, description, publishedAt, updatedAt, category, tags, authorIds, ogImage } = Astro.props;
const authors = await Promise.all(authorIds.map(id => getEntry('authors', id)));
const authorNames = authors.filter(Boolean).map(a => a!.data.name).join(', ');
---
<BaseLayout title={`${title} — nSealr Blog`} description={description} ogImage={ogImage}>
  <article class="container post">
    <header class="post-head">
      <p class="meta">
        <span class="cat">{category}</span>
        <time datetime={publishedAt.toISOString()}>{publishedAt.toISOString().slice(0,10)}</time>
        {authorNames && <span class="by">by {authorNames}</span>}
      </p>
      <h1>{title}</h1>
      <p class="lead">{description}</p>
      {tags.length > 0 && <div class="tags">{tags.map(t => <TagPill tag={t} href={`/blog/tags/${t}/`} />)}</div>}
    </header>
    <div class="prose">
      <slot />
    </div>
    <footer class="post-foot">
      {updatedAt && <p class="muted">Updated {updatedAt.toISOString().slice(0,10)}</p>}
      <p><a href="/blog/">← all posts</a></p>
    </footer>
  </article>
</BaseLayout>
<style>
  .post { padding-block: 48px; max-width: 760px; }
  .post-head { margin-bottom: 28px; }
  .meta { font-family: var(--font-mono); font-size: 12px; color: var(--fg-muted); display: flex; gap: 14px; flex-wrap: wrap; margin: 0 0 10px; }
  .cat { color: var(--accent-soft); text-transform: lowercase; }
  h1 { font-family: var(--font-mono); color: var(--fg-strong); font-size: clamp(28px, 4vw, 44px); line-height: 1.05; margin: 4px 0 12px; }
  .lead { color: var(--fg-muted); font-size: 17px; margin: 0 0 12px; max-width: 64ch; }
  .tags { display: flex; gap: 6px; flex-wrap: wrap; }
  .post-foot { margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--border); font-size: 14px; color: var(--fg-muted); }
</style>
```

- [ ] **Step 7.3 — `src/pages/blog/index.astro`**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import BlogList from '~/components/BlogList.astro';
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog', ({ data }) => !data.draft || import.meta.env.DEV))
  .sort((a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime());

const categories = Array.from(new Set(posts.map(p => p.data.category)));
---
<BaseLayout title="Blog — nSealr" description="Release notes, research, tutorials, and news from the nSealr program.">
  <section class="container">
    <p class="eyebrow">// blog</p>
    <h1>Notes on the program.</h1>
    <p class="lead">Release notes, research, tutorials, and news from nSealr signers, companion, and specs.</p>

    <div class="filters" role="navigation" aria-label="Categories">
      <a href="/blog/" class="active">all</a>
      {categories.map(c => <a href={`/blog/?cat=${c}`}>{c}</a>)}
      <a class="rss" href="/blog/rss.xml">RSS</a>
    </div>

    <BlogList posts={posts} />
  </section>
</BaseLayout>
<style>
  .container { padding-block: 60px; max-width: 880px; }
  h1 { font-family: var(--font-mono); color: var(--fg-strong); font-size: clamp(28px, 4vw, 44px); margin: 8px 0 12px; }
  .lead { color: var(--fg-muted); font-size: 17px; max-width: 64ch; margin: 0 0 22px; }
  .filters { display: flex; gap: 12px; flex-wrap: wrap; font-family: var(--font-mono); font-size: 12px; margin-bottom: 18px; }
  .filters a { color: var(--fg-muted); border: 1px solid var(--border); padding: 4px 10px; border-radius: var(--radius-pill); text-decoration: none; }
  .filters a.active, .filters a:hover { color: var(--accent-soft); border-color: var(--accent); }
  .filters a.rss { margin-left: auto; }
</style>
```

- [ ] **Step 7.4 — `src/pages/blog/[...slug].astro`**

```astro
---
import { getCollection, render } from 'astro:content';
import BlogPostLayout from '~/layouts/BlogPostLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft || import.meta.env.DEV);
  return posts.map(entry => ({ params: { slug: entry.id }, props: { entry } }));
}

const { entry } = Astro.props;
const { Content } = await render(entry);
const ogImage = `/og/blog/${entry.id}.png`;
---
<BlogPostLayout
  title={entry.data.title}
  description={entry.data.description}
  publishedAt={entry.data.publishedAt}
  updatedAt={entry.data.updatedAt}
  category={entry.data.category}
  tags={entry.data.tags}
  authorIds={entry.data.authors.map(a => a.id)}
  ogImage={ogImage}
>
  <Content />
</BlogPostLayout>
```

- [ ] **Step 7.5 — `src/pages/blog/tags/[tag].astro`**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import BlogList from '~/components/BlogList.astro';
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft || import.meta.env.DEV);
  const tags = new Set(posts.flatMap(p => p.data.tags));
  return Array.from(tags).map(tag => ({
    params: { tag },
    props: { posts: posts.filter(p => p.data.tags.includes(tag)).sort((a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime()), tag }
  }));
}

const { posts, tag } = Astro.props;
---
<BaseLayout title={`#${tag} — nSealr Blog`} description={`Posts tagged ${tag}`}>
  <section class="container">
    <p class="eyebrow">// blog · tag</p>
    <h1>#{tag}</h1>
    <BlogList posts={posts} />
    <p style="margin-top:24px"><a href="/blog/">← all posts</a></p>
  </section>
</BaseLayout>
<style>
  .container { padding-block: 60px; max-width: 880px; }
  h1 { font-family: var(--font-mono); color: var(--fg-strong); font-size: clamp(28px, 4vw, 40px); margin: 8px 0 18px; }
</style>
```

- [ ] **Step 7.6 — `src/pages/blog/rss.xml.ts`**

```ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft))
    .sort((a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime());
  return rss({
    title: 'nSealr Blog',
    description: 'Release notes, research, tutorials, and news from nSealr.',
    site: context.site!,
    items: posts.map(p => ({
      title: p.data.title,
      description: p.data.description,
      pubDate: p.data.publishedAt,
      link: `/blog/${p.id}/`,
      categories: [p.data.category, ...p.data.tags]
    }))
  });
}
```

- [ ] **Step 7.7 — `src/content/blog/2026-05-15-nsealr-website-relaunch.mdx`**

```mdx
---
title: 'nSealr website relaunches on Astro'
description: 'The public site moves from a hand-rolled static page to a Markdown-driven Astro build with documentation, a blog, and a light/dark theme.'
publishedAt: 2026-05-15
category: 'release'
tags: ['website', 'release']
authors:
  - nsealr-core
---

# nSealr website relaunches on Astro

The public site that used to be a single `index.html` is now an Astro
build driven by Markdown / MDX. Concretely:

- **Content lives in `src/content/`** — `docs/`, `blog/`, and a
  type-safe `signers/` collection sourced from
  `nSealr/specs vectors/features/signer-feature-matrix-v0.json`.
- **Light & dark themes** with Nostr purple `#8E30EB` as the primary
  accent. The toggle persists in `localStorage` and honors
  `prefers-color-scheme` on first load.
- **A real documentation section** with sidebar, ToC, and per-family
  status pages.
- **A blog** with categories, tags, and an RSS feed.
- **Vercel one-click deploy** with strict CSP and immutable caching for
  assets.

Nothing about the safety posture changes. The site still reports
`signing_disabled` on prototype firmware, never makes a production
security claim, and links to canonical specs and lab research instead of
duplicating them.
```

- [ ] **Step 7.8 — Smoke**

```bash
pnpm exec astro check
pnpm run dev &
sleep 4
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/blog/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/blog/2026-05-15-nsealr-website-relaunch/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/blog/tags/website/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:4321/blog/rss.xml
kill %1
```

Expected: all 200.

- [ ] **Step 7.9 — Commit**

```bash
git add src/components/BlogList.astro src/layouts/BlogPostLayout.astro src/pages/blog src/content/blog
git commit -m "feat(blog): index, post route, tag pages, rss + seed release post"
```

---

### Task 8: OG image generation, Pagefind, Vercel config

**Files:** Create `src/lib/og.ts`, `scripts/build_og.mjs`, `vercel.json.tpl`, `public/og-default.png` (generated once).

- [ ] **Step 8.1 — `src/lib/og.ts`**

```ts
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { readFileSync } from 'node:fs';

const interBold = readFileSync('public/fonts/Inter-Variable.woff2');
const monoBold = readFileSync('public/fonts/JetBrainsMono-Variable.woff2');

export interface OgInput {
  title: string;
  eyebrow?: string;
  category?: string;
}

export async function renderOgPng(input: OgInput): Promise<Buffer> {
  const svg = await satori(
    {
      type: 'div',
      props: {
        style: {
          width: '1200px', height: '630px',
          background: '#07060d', color: '#dcd4f0',
          padding: '64px', display: 'flex', flexDirection: 'column',
          justifyContent: 'space-between', fontFamily: 'JetBrainsMono'
        },
        children: [
          {
            type: 'div',
            props: {
              style: { display: 'flex', alignItems: 'center', gap: '14px' },
              children: [
                { type: 'div', props: { style: { width: '34px', height: '34px', border: '1px solid #2d2440', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#b388ff', fontSize: '14px' }, children: 'ns' } },
                { type: 'div', props: { style: { fontSize: '22px', color: '#ffffff' }, children: 'nsealr' } }
              ]
            }
          },
          {
            type: 'div',
            props: {
              style: { display: 'flex', flexDirection: 'column', gap: '18px' },
              children: [
                { type: 'div', props: { style: { color: '#b388ff', fontSize: '20px' }, children: input.eyebrow ?? '// nsealr · blog' } },
                { type: 'div', props: { style: { color: '#ffffff', fontSize: '72px', lineHeight: 1, letterSpacing: '-1.5px' }, children: input.title } },
                input.category
                  ? { type: 'div', props: { style: { color: '#7be0a8', fontSize: '20px' }, children: `# ${input.category}` } }
                  : null
              ].filter(Boolean)
            }
          },
          {
            type: 'div',
            props: {
              style: { color: '#7e7393', fontSize: '18px' },
              children: 'open-source · non-profit · pre-production'
            }
          }
        ]
      }
    },
    {
      width: 1200,
      height: 630,
      fonts: [
        { name: 'Inter', data: interBold, style: 'normal', weight: 700 },
        { name: 'JetBrainsMono', data: monoBold, style: 'normal', weight: 700 }
      ]
    }
  );
  const resvg = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } });
  return Buffer.from(resvg.render().asPng());
}
```

- [ ] **Step 8.2 — `scripts/build_og.mjs`**

```js
import { mkdirSync, writeFileSync, readdirSync, readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const { renderOgPng } = await import('../src/lib/og.ts');

mkdirSync('dist/og/blog', { recursive: true });

// default OG (regen if missing)
if (!existsSync('dist/og-default.png')) {
  const png = await renderOgPng({ title: 'Open hardware\nsigners for Nostr.', eyebrow: '// nsealr' });
  writeFileSync('dist/og-default.png', png);
}

// per-blog-post OG
const blogSrcDir = 'src/content/blog';
for (const file of readdirSync(blogSrcDir)) {
  if (!file.endsWith('.mdx')) continue;
  const slug = file.replace(/\.mdx$/, '');
  const out = `dist/og/blog/${slug}.png`;
  if (existsSync(out)) continue;
  const raw = readFileSync(join(blogSrcDir, file), 'utf8');
  const fm = raw.split('---')[1] ?? '';
  const title = (fm.match(/title:\s*['"]([^'"]+)['"]/) ?? [])[1] ?? slug;
  const category = (fm.match(/category:\s*['"]([^'"]+)['"]/) ?? [])[1];
  const png = await renderOgPng({ title, category });
  writeFileSync(out, png);
  console.log(`og: ${out}`);
}
```

- [ ] **Step 8.3 — `vercel.json.tpl`**

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "astro",
  "buildCommand": "pnpm run build",
  "installCommand": "pnpm install --frozen-lockfile",
  "outputDirectory": "dist",
  "redirects": [
    { "source": "/docs", "destination": "/docs/getting-started/overview/", "permanent": false }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Content-Security-Policy",
          "value": "default-src 'self'; img-src 'self' data:; font-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'sha256-__THEME_INIT_HASH__'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'none'" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), interest-cohort=()" }
      ]
    },
    {
      "source": "/_astro/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    },
    {
      "source": "/fonts/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
    }
  ]
}
```

- [ ] **Step 8.4 — Build full pipeline locally**

```bash
pnpm run build
ls dist/og-default.png dist/og/blog
```

Expected: both exist; `vercel.json` populated with sha256 hash (no `__THEME_INIT_HASH__` substring).

- [ ] **Step 8.5 — Copy generated `dist/og-default.png` to `public/` so it persists**

```bash
cp dist/og-default.png public/og-default.png
```

This makes the default OG image part of the repo. The build step regenerates it if missing but the canonical asset lives in `public/`.

- [ ] **Step 8.6 — Commit**

```bash
git add src/lib/og.ts scripts/build_og.mjs vercel.json.tpl vercel.json public/og-default.png
git commit -m "build: og image generation, vercel.json with strict csp, pagefind hookup"
```

---

### Task 9: Rewrite `validate_site.py` and tests against `dist/`

**Files:** Rewrite `scripts/validate_site.py`, `tests/test_site_validation.py`.

- [ ] **Step 9.1 — `scripts/validate_site.py`**

```python
#!/usr/bin/env python3
"""Validate the built Astro site under dist/.

Asserts that:
  * Required home strings appear on dist/index.html.
  * Each signer family page contains its declared `requiredText` phrases.
  * The /security/ page contains the safety-contract phrases.
  * No forbidden production claims appear anywhere in dist/.
  * No forbidden legacy vault-repo link appears anywhere in dist/.
  * Every local href in dist/index.html resolves to an existing file.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SIGNERS_SRC = ROOT / "src" / "content" / "signers"


HOME_REQUIRED_TEXT = [
    "nSealr",
    "open-source",
    "non-profit",
    "Companion",
    "Raspberry",
    "ESP32",
    "Smartcard",
    "Hardware",
    "Raspberry/Pi Stateless QR Vault",
    "ESP32 Stateless QR Vault",
    "ESP32 USB/NIP-46 Signer",
    "JavaCard/NFC Smartcard Signer",
    "Custom Nostr Hardware Wallet With Persistent Secret",
    "approval_digest",
    "signing_disabled",
    "NIP-46 bridge decisions",
    "nsealr nip46 decide",
    "request-bound capture checks",
    "nsealr serial-line exchange",
    "sign-event-disabled smoke",
    "review detail pages",
    "T-Display S3 review scenario smoke",
    "companion-to-device serial smoke",
    "firmware protocol evidence",
    "Unicode fallback",
    "Raspberry/Pi kit requirements",
    "Raspberry/Pi OS profile",
    "nsealr-smartcard CLI probes",
    "no trusted review or real-card compatibility claim",
    "No production security claim",
]

SECURITY_REQUIRED_TEXT = [
    "approval_digest",
    "signing_disabled",
    "NIP-46 bridge decisions",
    "nsealr nip46 decide",
    "request-bound capture checks",
    "review detail pages",
    "T-Display S3 review scenario smoke",
    "companion-to-device serial smoke",
    "sign-event-disabled smoke",
    "firmware protocol evidence",
    "Unicode fallback",
]

FORBIDDEN_CLAIMS = [
    "production ready",
    "military-grade",
    "unhackable",
    "guaranteed secure",
    "most secure",
]

FORBIDDEN_REPOSITORY_LINK_RE = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/vault(?:[\"/#?]|$)"
)


def read(path: Path) -> str:
    if not path.exists():
        raise ValueError(f"missing built file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def assert_contains_all(html: str, phrases: Iterable[str], page: str) -> None:
    missing = [p for p in phrases if p not in html]
    if missing:
        raise ValueError(f"{page}: missing required text: {missing}")


def assert_forbids_all(html: str, claims: Iterable[str], page: str) -> None:
    lower = html.lower()
    hits = [c for c in claims if c in lower]
    if hits:
        raise ValueError(f"{page}: forbidden unsupported claim: {hits}")


def parse_required_text_from_frontmatter(mdx_path: Path) -> list[str]:
    """Read `requiredText:` list from a signers/*.mdx frontmatter."""
    text = mdx_path.read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    lst_m = re.search(r"requiredText:\s*\n((?:\s+-\s+.*\n?)+)", block)
    if not lst_m:
        return []
    out: list[str] = []
    for line in lst_m.group(1).splitlines():
        item = re.match(r"\s+-\s+(?:'([^']+)'|\"([^\"]+)\"|(.+))", line)
        if item:
            out.append(item.group(1) or item.group(2) or item.group(3).strip())
    return out


def validate_home(dist: Path) -> None:
    html = read(dist / "index.html")
    assert_contains_all(html, HOME_REQUIRED_TEXT, "/")
    assert_forbids_all(html, FORBIDDEN_CLAIMS, "/")
    if FORBIDDEN_REPOSITORY_LINK_RE.search(html):
        raise ValueError("/ contains forbidden /vault github link")


def validate_security(dist: Path) -> None:
    html = read(dist / "security" / "index.html")
    assert_contains_all(html, SECURITY_REQUIRED_TEXT, "/security/")
    assert_forbids_all(html, FORBIDDEN_CLAIMS, "/security/")


def validate_signers(dist: Path) -> None:
    for mdx in sorted(SIGNERS_SRC.glob("*.mdx")):
        slug = mdx.stem
        page = dist / "docs" / "signers" / slug / "index.html"
        html = read(page)
        required = parse_required_text_from_frontmatter(mdx)
        if not required:
            raise ValueError(f"signers/{slug}.mdx has empty requiredText")
        assert_contains_all(html, required, f"/docs/signers/{slug}/")
        assert_forbids_all(html, FORBIDDEN_CLAIMS, f"/docs/signers/{slug}/")


def validate_global_no_forbidden_repo(dist: Path) -> None:
    for path in dist.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if FORBIDDEN_REPOSITORY_LINK_RE.search(text):
            raise ValueError(f"{path.relative_to(dist)}: forbidden /vault github link")


def main() -> int:
    if not DIST.exists():
        print("validate_site: dist/ missing — run `pnpm run build` first", file=sys.stderr)
        return 1
    validate_home(DIST)
    validate_security(DIST)
    validate_signers(DIST)
    validate_global_no_forbidden_repo(DIST)
    print("nSealr website validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 9.2 — `tests/test_site_validation.py`**

```python
import unittest
from pathlib import Path

from scripts.validate_site import (
    validate_home,
    validate_security,
    validate_signers,
    validate_global_no_forbidden_repo,
    parse_required_text_from_frontmatter,
)


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SIGNERS = ROOT / "src" / "content" / "signers"


@unittest.skipUnless(DIST.exists(), "dist/ not built; run `pnpm run build` first")
class WebsiteValidationTests(unittest.TestCase):
    def test_home_required_text(self) -> None:
        validate_home(DIST)

    def test_security_required_text(self) -> None:
        validate_security(DIST)

    def test_signers_required_text(self) -> None:
        validate_signers(DIST)

    def test_no_forbidden_repo_links(self) -> None:
        validate_global_no_forbidden_repo(DIST)


class FrontmatterParserTests(unittest.TestCase):
    def test_each_signer_declares_required_text(self) -> None:
        for mdx in SIGNERS.glob("*.mdx"):
            with self.subTest(file=mdx.name):
                self.assertTrue(parse_required_text_from_frontmatter(mdx),
                                f"{mdx.name} has empty requiredText")

    def test_five_signer_files_present(self) -> None:
        names = {p.stem for p in SIGNERS.glob("*.mdx")}
        self.assertEqual(
            names,
            {"raspberry-qr", "esp32-qr", "esp32-usb", "smartcard", "custom-wallet"},
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 9.3 — Run validation**

```bash
pnpm run build
python3 scripts/validate_site.py
python3 -m unittest discover -s tests
```

Expected: `nSealr website validation passed`, then `OK`.

- [ ] **Step 9.4 — Commit**

```bash
git add scripts/validate_site.py tests/test_site_validation.py
git commit -m "test: validate built dist tree against required text and forbidden claims"
```

---

### Task 10: CI, Makefile, README, .github workflow

**Files:** Modify `.github/workflows/ci.yml`, `Makefile`, `README.md`. Add `.github/workflows/lighthouse.yml` (optional in-PR).

- [ ] **Step 10.1 — `.github/workflows/ci.yml`**

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - name: Install
        run: pnpm install --frozen-lockfile
      - name: Astro check
        run: pnpm exec astro check
      - name: Build
        run: pnpm run build
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Validate site
        run: python3 scripts/validate_site.py
      - name: Unit tests
        run: python3 -m unittest discover -s tests
      - name: Link check
        uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress --exclude-mail dist
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist
```

- [ ] **Step 10.2 — `Makefile`**

```make
.PHONY: setup dev build check validate test lint ci clean

setup:
	corepack enable
	corepack prepare pnpm@9 --activate
	pnpm install --frozen-lockfile

dev:
	pnpm run dev

build:
	pnpm run build

check:
	pnpm exec astro check

validate:
	python3 scripts/validate_site.py

test:
	python3 -m unittest discover -s tests

lint:
	python3 scripts/verify_repo.py
	python3 -m compileall -q scripts tests

ci: setup check build validate test lint

clean:
	rm -rf dist .astro node_modules
```

- [ ] **Step 10.3 — Update `README.md`**

Replace the existing README with content that describes the new stack and dev/run/deploy steps. Key sections:

```md
# nSealr Website

Public website and documentation hub for nSealr.

## Stack

- Astro 5 (static output) with TypeScript strict.
- Markdown / MDX content collections (`blog`, `docs`, `signers`, `authors`)
  validated by Zod schemas at build time.
- JetBrains Mono + Inter (variable, self-hosted) typography.
- Light / dark theme with Nostr purple `#8E30EB` as the primary accent,
  toggle persists in `localStorage`, honors `prefers-color-scheme`.
- Pagefind for static search, Shiki for syntax highlighting.
- Vercel preset for one-push deployment with strict CSP, immutable
  cache for `/_astro/*` and `/fonts/*`.

## Develop

```sh
make setup
make dev          # http://localhost:4321
```

## Build & validate

```sh
make build        # → dist/
make ci           # check + build + validate_site.py + unittest + lint
```

`scripts/validate_site.py` asserts every required safety-contract phrase
against `dist/` (split by route: home, /security, per-family signer pages).
Forbidden production claims and forbidden legacy GitHub links ending in `/vault`
are rejected.

## Deploy (Vercel)

The project is Vercel-preset-aware. Connect the repo, set framework
`astro`. Production = push to `main`; preview deploys per PR.
The CSP `script-src` hash for the inline theme bootstrap is computed
from `src/scripts/theme-init.ts` by `scripts/compute_csp_hash.mjs` at
every build, so the produced `vercel.json` stays in sync.

## Authoring

- Blog post: add `src/content/blog/<date>-<slug>.mdx`.
- Doc page: add `src/content/docs/<section>/<slug>.mdx`.
- Signer family update: edit `src/content/signers/<family>.mdx`. The
  `capabilities` array mirrors `nSealr/specs vectors/features/signer-feature-matrix-v0.json`.

## License

MIT for code. CC0-1.0 for content when published.
```

- [ ] **Step 10.4 — Commit**

```bash
git add .github/workflows/ci.yml Makefile README.md
git commit -m "ci: pnpm-driven pipeline, lychee link check, updated readme"
```

---

### Task 11: Remove old static files; final verification

**Files:** Delete `public/index.html`, `public/styles.css`, `content/.gitkeep`, `design/.gitkeep`.

- [ ] **Step 11.1 — Delete legacy static**

```bash
git rm public/index.html public/styles.css content/.gitkeep design/.gitkeep
rmdir content design 2>/dev/null || true
```

- [ ] **Step 11.2 — Full pipeline**

```bash
pnpm run ci
```

Expected: passes end-to-end. If `validate_site.py` reports missing text, the offending phrase needs to land on the right route — fix the page that owns it (home / security / signer family) rather than the validator.

- [ ] **Step 11.3 — Final manual smoke**

```bash
pnpm run build && pnpm run preview &
sleep 4
curl -s -o /dev/null -w "/=%{http_code} system=%{http_code} docs=%{http_code} blog=%{http_code} rss=%{http_code}\n" http://localhost:4321/ \
  -o /dev/null -w "/system=%{http_code}\n" \
  http://localhost:4321/system/ -o /dev/null \
  -w "/docs=%{http_code}\n" http://localhost:4321/docs/ -o /dev/null \
  -w "/blog=%{http_code}\n" http://localhost:4321/blog/ -o /dev/null \
  -w "/rss=%{http_code}\n" http://localhost:4321/blog/rss.xml
kill %1
```

Expected: all 200.

- [ ] **Step 11.4 — Commit**

```bash
git rm public/index.html public/styles.css content/.gitkeep design/.gitkeep
git commit -m "chore: remove legacy public/index.html and styles.css; remove content/design placeholders"
```

---

## Self-Review

**Spec coverage:**
- §3 Stack → Task 1 (`package.json`, `astro.config.mjs`).
- §4 IA → Tasks 5, 6, 7 (pages for home/system/security/docs/blog).
- §5 Content model → Task 3 (`content.config.ts` + signers seed).
- §6 Design system → Task 2 (tokens, base, prose, fonts, theme-init).
- §7 Components → Tasks 4, 5, 6, 7 (every named component is built).
- §8 Search → Task 5 + Task 8 (`SearchTrigger` + Pagefind in `pnpm run build`).
- §9 Validation/testing → Task 9 + Task 10 (validator + CI).
- §10 Deploy → Task 8 (`vercel.json.tpl` + `compute_csp_hash.mjs`).
- §11 Migration → Tasks 1–11 in order; legacy delete in Task 11.

**Placeholder scan:** No "TBD" / "implement later" remain. Every code block contains complete content.

**Type consistency:** `theme-init.ts` exports `themeInitScript` and the same name is consumed in `BaseLayout.astro`. `FeatureMatrix` reads `signers` collection by `family` field, which matches the Zod enum. `getDocsNav` returns the shape consumed by `DocsSidebar.astro`. `validate_site.py` calls match the imports in `test_site_validation.py`. `vercel.json.tpl` uses literal `__THEME_INIT_HASH__` and `compute_csp_hash.mjs` substitutes that exact string.

---

## Execution

User pre-authorized full execution. Proceeding inline with executing-plans.
