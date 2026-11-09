import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const source = JSON.parse(await readFile('public/connect/source.json', 'utf8'));
assert.match(source.commit, /^[a-f0-9]{40}$/);
for (const [name, hash] of Object.entries(source.web)) {
  const data = await readFile(`public/connect/${name}`);
  assert.equal(createHash('sha256').update(data).digest('hex'), hash, `Repackage changed asset: ${name}`);
}
for (const [name, entry] of Object.entries(source.downloads)) {
  const data = await readFile(`public/downloads/${name}`);
  assert.equal(data.length, entry.bytes, `Download size changed: ${name}`);
  assert.equal(createHash('sha256').update(data).digest('hex'), entry.sha256, `Download hash changed: ${name}`);
}
console.log(`Companion assets verified: ${source.commit}`);
