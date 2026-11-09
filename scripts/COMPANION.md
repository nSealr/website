The site serves a frozen companion build from `public/connect/`. Website builds
verify the recorded hashes and copy these local assets; they never fetch or rebuild the companion. Runtime
JavaScript, fonts and dependency notices are local. Only the hosted HTML footer
is adjusted to link to the website guide and extension downloads.

To refresh, select a reviewed, clean nSealr checkout and use Node.js/npm plus Python 3:

```sh
python3 scripts/package_companion.py /path/to/nsealr FULL_COMMIT
pnpm run ci
```

The helper checks the source against the exact commit, runs `npm ci --ignore-scripts`
and `npm run build` in that checkout, then copies an explicit asset list. This
explicit refresh may download pinned dependencies; the website build does not.
Both ZIPs use fixed metadata and sorted entries. Review the generated changes
together. `source.json` records the commit, source tree and SHA-256 hashes; each
ZIP includes its own source record and licenses.

`vercel.json.tpl` grants camera access and secure WebSocket connections only to
`/connect/`. Its CSP allows local scripts without eval or inline scripts. The
rest of the website retains its existing policy. Deployment headers need to be
checked on the deployed URL as well as in the local browser check.

Chromium downloads are loaded unpacked. Firefox downloads are unsigned and use
[Mozilla's temporary installation flow](https://extensionworkshop.com/documentation/develop/temporary-installation-in-firefox/).
Neither ZIP is a browser-store listing.
