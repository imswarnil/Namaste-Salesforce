# Prompt — a DOCUMENTATION ARTICLE

> Paste `00-house-style.md` above this, then your brief.

You are producing a **help-centre article** at `/docs/{section}/{slug}/`. Docs
answer *how do I do this on this website* — accounts, billing, progress,
publishing, troubleshooting. They are not Salesforce tutorials; that is what
courses and training are for.

Rendered by `partials/post-documentation.hbs` — sticky docs sidebar, article,
right rail with the contents.

---

## Docs voice is different

Courses teach and blog posts argue. **Docs answer a question and stop.** The
reader is mildly annoyed already — something did not work, or they cannot find a
setting. So:

- **Answer in the first sentence.** No preamble, no "This article explains…".
- **Shortest correct path only.** One way to do the thing. Alternatives go at the
  end, if at all.
- **No personality.** No first person, no jokes, no opinions.
- **Literal UI strings**, in the case the interface uses, wrapped in `<code>` when
  they are exact labels.
- **Say what happens after.** A step without its confirmation is half a step.

## Where it lands and what the theme builds around you

| Region | Comes from |
| --- | --- |
| Docs sidebar, current article highlighted, its section opened | generated from the section registry |
| Mobile docs menu bar | theme |
| Breadcrumb: Home › Docs › {section} › {title} | theme |
| `<h1>` | Title |
| Lede | **Excerpt** |
| Reading time · author · "Updated {date}" | automatic (`updated_at`) |
| Header image | Feature image + alt |
| The article | **your body** |
| Prev / Next **within the section** | siblings, by publish date |
| First article of a section → "Section overview" card | theme |
| Last article of a section → "next section" card | theme |
| Right rail: on-this-page | your `<h2>`/`<h3>`s |
| Comments | Ghost |

---

## The ten sections — and only these ten

A docs section is registered in **three** places: `partials/docs/sections.hbs`,
`partials/docs/next-section-for.hbs`, and `routes.yaml`. Content alone cannot
create one. Use an existing slug:

| Section tag | Slug | Covers |
| --- | --- | --- |
| Getting Started | `getting-started` | account creation, first steps, orientation |
| Account & Profile | `account-profile` | email, display name, preferences |
| Courses & Lessons | `courses-lessons` | how courses work, previews, gating |
| Roadmaps | `roadmaps` | the guided training path and following it |
| Membership & Billing | `membership-billing` | plans, payments, invoices, cancelling |
| Certificates & Progress | `certificates-progress` | completion tracking, certificates |
| Become an Author | `become-an-author` | what we publish, the review process |
| Community & Support | `community-support` | where to ask, guidelines |
| Troubleshooting | `troubleshooting` | errors, sign-in problems, things not loading |
| Design System | `design-system` | the Developer Console system this site is built from |

**If your article does not fit one of these,** do not invent a section. Either
place it in the closest fit, or flag it:

> ⚠ This needs a new docs section (`{name}`), which is a theme change:
> add a `docs/section-item` line to `partials/docs/sections.hbs`, mirror the
> order in `partials/docs/next-section-for.hbs`, and add a
> `/docs/{slug}/` route with `data: tag.{slug}` and `template: docs-section`
> to `routes.yaml`.

---

## Fields

| Field | Rule |
| --- | --- |
| **Title** | The question, as a task. "Change your email address", "Cancel or change your plan", "Sign-in link not working". Imperative or the symptom — never "Email Management" and never a question mark. |
| **Slug** | `{section}-NN-{title-words}` — `account-profile-01-change-your-email-address`. Matches existing content and keeps the admin list sorted; publish date is what actually orders it. |
| **Excerpt** | The lede. One sentence, 15–30 words, that already contains the answer's shape. *"Change it from your account page — the new address has to be confirmed before it becomes your sign-in."* |
| **Feature image** | Usually none. Add one only if a screenshot genuinely disambiguates, and give it real alt text. |
| **Publish date** | **Article order within the section.** Ascending, spaced. |
| **Updated** | Rendered on the page as "Updated {date}". Re-save when the product changes — a stale docs date is worse than none. |
| **Visibility** | `public`. Always. Someone locked out of their account cannot sign in to read how to sign in. |

## Tags — exact, and in this order

```
TAGS: <Section Name>, documentation
```

1. **The section tag**, public, **first** — one of the ten above. This is
   `primary_tag`, and it is the `/docs/{section}/` segment of the URL as well as
   what puts the article in the right sidebar group.
2. `documentation` — required. Note it is a **public** tag, not a `#` internal
   one. It must come **second**; if it lands first it becomes `primary_tag` and
   the URL breaks.

No other tags. No level, access or type tags exist for docs.

---

## Body — the answer

**150–500 words.** If it needs more, it is probably two articles.

**Required shape:**

```html
<h2>{The answer, as a heading}</h2>
<p>{One or two sentences that answer the question outright, before any steps.
   A reader who reads only this should be unblocked.}</p>

<h2>Steps</h2>
<ol>
  <li>{One action each, with the literal label: "Click <code>Account</code> in
      the top-right menu." Then what appears: "The account panel opens."}</li>
</ol>

<h2>{What to expect / If it doesn't work}</h2>
<p>{The confirmation, the timing, or the two most common failures and what to do
   about each. For a Troubleshooting article this is the bulk of the piece.}</p>
```

For a conceptual docs article ("How a course is structured", "What a roadmap
is") drop the Steps block and use two or three explanatory `<h2>`s instead — but
keep the first-sentence answer.

### Notes

- **Two `<h2>`s minimum** or the contents rail hides itself.
- No cross-links to the previous or next article — those cards are rendered, and
  the edges of a section are handled for you (first article links back to the
  section overview, last one tees up the next section).
- Linking sideways to *another* section's article is fine and encouraged; use a
  real `/docs/{section}/{slug}/` path.
- Code blocks are rare here. When you use one, still set the language.
- At most one `.ns-note`, for irreversible actions (cancelling, deleting).
- Never document a feature that does not exist. If a step depends on a setting an
  admin must enable, say which.

---

## Worked example

```
─────────────────────────────────────────
TITLE:        Change your email address
SLUG:         account-profile-01-change-your-email-address
EXCERPT:      Change it from your account panel — the new address has to be
              confirmed by email before it becomes your sign-in.
TAGS:         Account & Profile, documentation
VISIBILITY:   public
PUBLISH:      2026-08-16 09:00   (relative order: 1 of 2 in Account & Profile)
FEATURE IMAGE: none
─────────────────────────────────────────
BODY (paste into a Ghost HTML card):

<h2>Change it from your account panel</h2>
<p>Your email address is both your contact address and how you sign in, so
  changing it needs confirmation from the new address. Until you confirm, the old
  address keeps working.</p>

<h2>Steps</h2>
<ol>
  <li>Click <code>Account</code> in the top-right of any page. The account panel
    opens.</li>
  <li>Click <code>Account settings</code>.</li>
  <li>Enter the new address in the <code>Email</code> field and click
    <code>Save</code>.</li>
  <li>Open the confirmation email sent to the <em>new</em> address and click the
    link inside it.</li>
</ol>

<h2>If the confirmation email doesn't arrive</h2>
<p>Give it a few minutes, then check spam — confirmation mail is transactional and
  is occasionally filtered. If it is still missing, the address was most likely
  mistyped: repeat the steps above and the previous request is replaced. Your
  sign-in stays on the old address the whole time, so nothing is lost by trying
  again.</p>
```

---

## Self-check

Everything in `00-house-style.md`, plus:

- [ ] Section tag is **first**, `documentation` **second**
- [ ] The section is one of the ten registered slugs — or a new section has been
      flagged as a theme change
- [ ] The answer is in the first sentence, before any steps
- [ ] Steps are one action each, with the literal UI label and the resulting state
- [ ] There is a "what to expect" or "if it doesn't work" section
- [ ] Publish date set to the intended position in the section
- [ ] Visibility is `public`
- [ ] No prev/next links written by hand
- [ ] Under ~500 words; no first person, no jokes, no opinions
- [ ] Nothing documented that does not exist
