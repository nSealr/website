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

const tplPath = 'vercel.json.tpl';
const outPath = 'vercel.json';
if (!existsSync(tplPath)) {
  console.error(`compute_csp_hash: ${tplPath} missing`);
  process.exit(1);
}
const vercel = readFileSync(tplPath, 'utf8').replaceAll('__THEME_INIT_HASH__', hash);
writeFileSync(outPath, vercel);
console.log(`compute_csp_hash: vercel.json written with sha256-${hash}`);
