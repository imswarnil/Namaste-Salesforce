// sync-page-meta.mjs — apply .github/content/page-meta.json to a live
// Ghost site through the Admin API. Run by .github/workflows/content-sync.yml
// with the same GHOST_ADMIN_API_URL / GHOST_ADMIN_API_KEY secrets the theme
// deploy uses. Prints every page's PREVIOUS values before changing it, so
// the run log is the undo record. DRY_RUN=1 prints without writing.
import { readFileSync } from 'node:fs';
import { createHmac } from 'node:crypto';

const url = (process.env.GHOST_ADMIN_API_URL || '').replace(/\/$/, '');
const key = process.env.GHOST_ADMIN_API_KEY || '';
const dry = process.env.DRY_RUN === '1';
if (!url || !key.includes(':')) { console.error('Missing GHOST_ADMIN_API_URL / GHOST_ADMIN_API_KEY'); process.exit(1); }

const [id, secret] = key.split(':');
const b64 = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
function token() {
  const now = Math.floor(Date.now() / 1000);
  const h = b64({ alg: 'HS256', typ: 'JWT', kid: id });
  const p = b64({ iat: now, exp: now + 300, aud: '/admin/' });
  const s = createHmac('sha256', Buffer.from(secret, 'hex')).update(`${h}.${p}`).digest('base64url');
  return `${h}.${p}.${s}`;
}
async function api(method, path, body) {
  const res = await fetch(`${url}/ghost/api/admin${path}`, {
    method,
    headers: { Authorization: `Ghost ${token()}`, 'Content-Type': 'application/json', 'Accept-Version': 'v5.0' },
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`${method} ${path} → ${res.status} ${JSON.stringify(json.errors?.[0]?.message || json)}`);
  return json;
}

const spec = JSON.parse(readFileSync(new URL('./page-meta.json', import.meta.url)));
const { pages } = await api('GET', '/pages/?limit=all&filter=status:[published,draft]&fields=id,slug,status,updated_at,custom_excerpt,meta_title,meta_description');
const bySlug = Object.fromEntries(pages.map((p) => [p.slug, p]));
let changed = 0, missing = [];

for (const [slug, next] of Object.entries(spec.pages)) {
  const page = bySlug[slug];
  if (!page) { missing.push(slug); continue; }
  const before = Object.fromEntries(Object.keys(next).map((k) => [k, page[k]]));
  console.log(`\n# ${slug}\nBEFORE ${JSON.stringify(before)}`);
  if (Object.keys(next).every((k) => page[k] === next[k])) { console.log('unchanged'); continue; }
  if (!dry) await api('PUT', `/pages/${page.id}/`, { pages: [{ updated_at: page.updated_at, ...next }] });
  console.log(dry ? 'would update' : 'updated'); changed++;
}

for (const slug of spec.draft || []) {
  const page = bySlug[slug];
  if (!page) { missing.push(slug); continue; }
  console.log(`\n# ${slug}\nBEFORE status=${page.status}`);
  if (page.status === 'draft') { console.log('already draft'); continue; }
  if (!dry) await api('PUT', `/pages/${page.id}/`, { pages: [{ updated_at: page.updated_at, status: 'draft' }] });
  console.log(dry ? 'would unpublish' : 'unpublished → draft'); changed++;
}

console.log(`\n${dry ? 'DRY RUN — ' : ''}${changed} page(s) changed.${missing.length ? ' Not on this site: ' + missing.join(', ') : ''}`);
