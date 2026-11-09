import {writeFileSync} from 'node:fs';
import {renderOgPng} from '../src/lib/og.mjs';
writeFileSync('dist/og-default.png', await renderOgPng({title:'Your Nostr key.\nOffline.',eyebrow:'// nsealr'}));
