# nSealr Website

Public website and documentation hub for nSealr.

Non-profit, open-source program for Nostr signing devices. The site
explains the program without turning the core work into a proprietary
product.

## Stack

- **Astro 5** (static output) + TypeScript strict.
- **Markdown / MDX content collections** — `blog`, `docs`, `signers`,
  `authors` — validated by Zod schemas at build time. Bad frontmatter
  fails the build.
- **JetBrains Mono + Inter** (variable, self-hosted from
  `public/fonts/`).
- **Light / dark theme** with Nostr purple `#8E30EB` as the primary
  accent. Toggle persists in `localStorage`, respects
  `prefers-color-scheme` on first load, no FOUC.
- **Pagefind** for static client-side search.
- **Shiki** for syntax highlighting (dual-theme: `github-dark-dimmed`
  + `min-light`).
- **Vercel** preset with strict CSP, immutable cache for `/_astro/*`
  and `/fonts/*`. The CSP `script-src` hash is computed from
  `src/scripts/theme-init.ts` by `scripts/compute_csp_hash.mjs` at
  every build, so `vercel.json` stays in sync.

## Develop

```sh
make setup        # pnpm install --frozen-lockfile
make dev          # → http://localhost:4321
```

## Build & validate

```sh
make build        # → dist/ (astro build + pagefind + og images)
make ci           # check + build + validate_site.py + unittest + lint
```

`scripts/validate_site.py` scans the built `dist/` tree:

- `HOME_REQUIRED_TEXT` — required brand + safety-contract strings on
  `dist/index.html`.
- Each signer family page (`dist/docs/signers/<family>/index.html`)
  contains its declared `requiredText` from the MDX frontmatter.
- `dist/security/index.html` contains the safety-contract phrases.
- No forbidden production claims appear anywhere.
- No `/vault` repo link appears anywhere.

## Deploy (Vercel)

The project is Vercel-preset-aware. Connect the repo, framework =
`astro`. Production = push to `main`; preview deploys per PR. Initial
URL is `nsealr.vercel.app`; attach a custom domain when ready without
code changes.

## Authoring

- **Blog post**: add `src/content/blog/<date>-<slug>.mdx`.
- **Doc page**: add `src/content/docs/<section>/<slug>.mdx` with
  `section` in `getting-started | guides | signers | specs | security`.
- **Signer family update**: edit
  `src/content/signers/<family>.mdx`. The `capabilities` array mirrors
  `nSealr/specs vectors/features/signer-feature-matrix-v0.json` — the
  same `contract_id` must keep the same behavior across families.

## Layout

```
website/
  astro.config.mjs · vercel.json(.tpl) · package.json · Makefile
  public/         # fonts, favicon, robots, og-default.png
  src/
    content/      # MDX + JSON content (blog, docs, signers, authors)
    components/   # Astro UI primitives
    layouts/      # BaseLayout, DocsLayout, BlogPostLayout
    pages/        # routes
    styles/       # tokens.css, base.css, prose.css
    scripts/      # theme-init.ts (inline blocking script source)
    lib/          # docs-nav.ts, og.mjs
  scripts/
    validate_site.py        # required-text / forbidden-claims validator
    verify_repo.py          # repo lint
    build_og.mjs            # satori OG image generation
    compute_csp_hash.mjs    # writes vercel.json from vercel.json.tpl
    og-fonts/               # TTF fonts used only by satori
  tests/
    test_site_validation.py
```

## Related repositories

`nSealr/specs`, `nSealr/companion`, `nSealr/raspberry`,
`nSealr/esp32`, `nSealr/smartcard`, `nSealr/hardware`, `nSealr/lab`.

## License

MIT for code. CC0-1.0 for content when published.
