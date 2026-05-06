# Technical Plan

## Default Direction

Use Astro when implementation starts unless requirements change.

Reasons:

- static-first output;
- good Markdown/MDX support;
- straightforward GitHub Pages deployment;
- enough flexibility for docs, comparison pages, and future interactive demos;
- avoids overbuilding a full application before the content is stable.

## Deployment Candidates

- GitHub Pages for the first public launch.
- Cloudflare Pages if preview deployments, redirects, or edge headers become
  useful.

## Content Sources

- `lab` remains the source-backed research graph.
- `website` publishes curated public explanations and build docs.
- `specs` remains the canonical machine/test-vector repo.

The website should link to source repositories rather than duplicating long
technical documents.

## Required Checks Before Public Launch

- no private notes or unverified claims in public pages;
- all repo links point to public repositories;
- security claims match `lab` threat models;
- hardware maturity labels are explicit;
- generated site has no broken internal links.

## Future Automation

- Build and deploy on push to `main`.
- Link checker for internal/external URLs.
- Markdown linting.
- Spell check for public pages.
- Optional sync script that imports selected roadmap status from `lab`.
