/**
 * Regenerate brand-derived PNGs in public/ from src/assets/nsealr-logo.png:
 *   - public/favicon.png          (32×32, browsers without SVG support)
 *   - public/favicon-180.png      (apple-touch-icon)
 *   - public/og-default.png       (1200×630, OG/Twitter card)
 *
 * Run manually after the brand logo changes:
 *   node scripts/build_brand_assets.mjs
 */
import sharp from 'sharp';
import { mkdirSync, existsSync } from 'node:fs';

const SRC = 'src/assets/nsealr-logo.png';
if (!existsSync(SRC)) {
  console.error(`build_brand_assets: ${SRC} missing`);
  process.exit(1);
}

mkdirSync('public', { recursive: true });

await sharp(SRC).resize(32, 32, { fit: 'cover' }).png({ compressionLevel: 9 }).toFile('public/favicon.png');
console.log('wrote public/favicon.png (32×32)');

await sharp(SRC).resize(180, 180, { fit: 'cover' }).png({ compressionLevel: 9 }).toFile('public/favicon-180.png');
console.log('wrote public/favicon-180.png (180×180)');

// OG: dark background, logo on the left, room for runtime text overlay isn't needed —
// the per-post OG is rendered separately by build_og.mjs; this is the default fallback.
const BG = { r: 7, g: 6, b: 13, alpha: 1 };
const logo = await sharp(SRC).resize(440, 440, { fit: 'contain' }).png().toBuffer();
await sharp({
  create: { width: 1200, height: 630, channels: 3, background: BG }
})
  .composite([{ input: logo, left: 80, top: 95 }])
  .png({ compressionLevel: 9 })
  .toFile('public/og-default.png');
console.log('wrote public/og-default.png (1200×630)');
