/* ════════════════════════════════════════════════════════════════════════════
   migrate-col-tags.mjs — add the `-col` collection tags to published posts.
   ----------------------------------------------------------------------------
       node scripts/migrate-col-tags.mjs            # dry run — changes nothing
       node scripts/migrate-col-tags.mjs --apply    # writes

       GHOST_URL=https://www.namastesalesforce.com \
       GHOST_ADMIN_API_KEY=<id:secret> node scripts/migrate-col-tags.mjs

   ── WHY THIS IS ADDITIVE, AND WHY THAT IS THE WHOLE DESIGN ──────────────────
   It ADDS `#blog-col` beside `#blog`. It removes nothing, ever.

   Collection membership is decided by routes.yaml's filter, and routes.yaml
   is NOT in the theme zip — it is uploaded separately in Ghost Admin. So the
   two halves of this migration cannot be made atomic, and there is a window
   where one is done and the other is not. Additive means that window is safe
   in BOTH directions: a post carrying old and new tags matches the old filter
   and the new one, so whichever routes.yaml is live, every post stays routed.

   Remove a tag instead and the window is a 404 on published content.

   ⚠ URLS DO NOT CHANGE. The permalinks use {slug} and {primary_tag}, and
   {primary_tag} resolves to the post's PUBLIC tag — "Data Model Basics", not
   "#training-content". Internal tags decide which collection claims a post,
   never where it lands. Verified against the live URL model before writing
   this.

   ── THE ORDER, WHICH IS NOT OPTIONAL ────────────────────────────────────────
     1. run this with --apply
     2. confirm every count below is 0 remaining
     3. THEN upload routes.yaml in Admin → Settings → Labs → Routes
     4. spot-check one URL per collection
     5. later, once settled, drop the old tags and the old branches in post.hbs

   Doing 3 before 1 unroutes every post in every collection.
   ═══════════════════════════════════════════════════════════════════════ */

import GhostAdminAPI from '@tryghost/admin-api';

const URL = process.env.GHOST_URL;
const KEY = process.env.GHOST_ADMIN_API_KEY;
const APPLY = process.argv.includes('--apply');

if (!URL || !KEY) {
    console.error('Set GHOST_URL and GHOST_ADMIN_API_KEY. See the header of this file.');
    process.exit(2);
}

/* old internal tag → the -col tag it gains. Nothing is renamed or removed. */
const MAP = {
    'hash-training-section': 'training-sections-col',
    'hash-training-module':  'training-sections-col',  // canonical name, unused live
    'hash-training-content': 'training-lessons-col',
    'hash-training-lesson':  'training-lessons-col',
    'hash-course':           'courses-col',
    'hash-lesson':           'lessons-col',
    'hash-blog':             'blog-col',
    'hash-docs-section':     'folders-col',
    'hash-docs-page':        'docs-col',
    'hash-resource':         'resource-col',
};

const api = new GhostAdminAPI({ url: URL, key: KEY, version: 'v5.0' });

const posts = await api.posts.browse({ limit: 'all', include: 'tags' });
console.log(`${posts.length} posts on ${URL}\n`);

const planned = [];
for (const post of posts) {
    const slugs = new Set(post.tags.map(t => t.slug));
    const want = new Set();
    for (const [from, to] of Object.entries(MAP)) {
        if (slugs.has(from) && !slugs.has(`hash-${to}`)) want.add(to);
    }
    if (want.size) planned.push({ post, want: [...want] });
}

if (!planned.length) {
    console.log('✓ nothing to do — every post already carries its -col tag.');
    process.exit(0);
}

for (const { post, want } of planned) {
    console.log(`  ${post.url.replace(URL, '') || '/'}\n      + ${want.map(w => '#' + w).join(', ')}`);
}
console.log(`\n${planned.length} posts would gain tags.`);

if (!APPLY) {
    console.log('\nDRY RUN — nothing written. Re-run with --apply.');
    process.exit(0);
}

let ok = 0, failed = 0;
for (const { post, want } of planned) {
    try {
        /* Send the existing tags plus the new ones. Ghost REPLACES the tag
           list on edit, so omitting the current ones would strip them —
           which is the one way this script could destroy something. */
        const tags = [...post.tags.map(t => ({ name: t.name })),
                      ...want.map(w => ({ name: '#' + w }))];
        await api.posts.edit({ id: post.id, updated_at: post.updated_at, tags });
        ok++;
    } catch (e) {
        failed++;
        console.error(`  ✗ ${post.slug}: ${e.message}`);
    }
}
console.log(`\n✓ ${ok} updated${failed ? `, ✗ ${failed} failed` : ''}.`);
console.log('Now re-run the dry run to confirm 0 remaining, THEN upload routes.yaml.');
