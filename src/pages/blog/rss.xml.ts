import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import MarkdownIt from 'markdown-it';
import sanitizeHtml from 'sanitize-html';
import type { APIContext } from 'astro';

const md = new MarkdownIt({ html: false, linkify: true, typographer: true });

// Resolve from project cwd so it works both in dev (astro dev) and build.
const BLOG_DIR = join(process.cwd(), 'src/content/blog');

/**
 * Best-effort MDX → HTML for RSS:
 *   - strip frontmatter,
 *   - strip MDX imports / JSX components (e.g. <FeatureMatrix /> in docs),
 *   - run markdown-it for the rest,
 *   - sanitize for feed-reader safety.
 *
 * RSS readers do not run our component tree; the alternative would be to spin
 * up the Astro container API per item, which is heavier and not needed for a
 * doc-blog with mostly prose posts.
 */
function postBodyToHtml(slug: string): string {
  const raw = readFileSync(join(BLOG_DIR, `${slug}.mdx`), 'utf8');
  const withoutFrontmatter = raw.replace(/^---[\s\S]*?---\n/, '');
  const withoutMdx = withoutFrontmatter
    .replace(/^import\s.+?;\s*$/gm, '')
    .replace(/<[A-Z][A-Za-z0-9]*(\s[^>]*)?\/>/g, '')
    .replace(/<[A-Z][A-Za-z0-9]*(\s[^>]*)?>[\s\S]*?<\/[A-Z][A-Za-z0-9]*>/g, '');
  const html = md.render(withoutMdx);
  return sanitizeHtml(html, {
    allowedTags: sanitizeHtml.defaults.allowedTags.concat(['img', 'pre', 'code']),
    allowedAttributes: {
      ...sanitizeHtml.defaults.allowedAttributes,
      a: ['href', 'name', 'target', 'rel'],
      img: ['src', 'alt', 'title'],
      code: ['class'],
      pre: ['class'],
    },
  });
}

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
      categories: [p.data.category, ...p.data.tags],
      content: postBodyToHtml(p.id),
    })),
  });
}
