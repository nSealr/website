import { mkdirSync, writeFileSync, readdirSync, readFileSync, existsSync, copyFileSync } from 'node:fs';
import { join } from 'node:path';
import { renderOgPng } from '../src/lib/og.mjs';

mkdirSync('dist/og/blog', { recursive: true });

// default OG (regen if missing in dist)
if (!existsSync('dist/og-default.png')) {
  if (existsSync('public/og-default.png')) {
    copyFileSync('public/og-default.png', 'dist/og-default.png');
  } else {
    const png = await renderOgPng({ title: 'Open hardware\nsigners for Nostr.', eyebrow: '// nsealr' });
    writeFileSync('dist/og-default.png', png);
    writeFileSync('public/og-default.png', png);
    console.log('og: wrote default at public/og-default.png');
  }
}

// per-blog-post OG
const blogSrcDir = 'src/content/blog';
if (existsSync(blogSrcDir)) {
  for (const file of readdirSync(blogSrcDir)) {
    if (!file.endsWith('.mdx')) continue;
    const slug = file.replace(/\.mdx$/, '');
    const out = `dist/og/blog/${slug}.png`;
    if (existsSync(out)) continue;
    const raw = readFileSync(join(blogSrcDir, file), 'utf8');
    const fm = raw.split('---')[1] ?? '';
    const titleMatch = fm.match(/title:\s*['"]([^'"]+)['"]/);
    const categoryMatch = fm.match(/category:\s*['"]([^'"]+)['"]/);
    const title = titleMatch ? titleMatch[1] : slug;
    const category = categoryMatch ? categoryMatch[1] : undefined;
    const png = await renderOgPng({ title, category });
    writeFileSync(out, png);
    console.log(`og: ${out}`);
  }
}
