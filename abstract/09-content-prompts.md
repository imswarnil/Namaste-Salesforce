# 09 · The content prompts

`prompt/` — the briefs handed to a writer or an AI to produce content that
matches the templates that render it. They are versioned with the theme
because a template change can invalidate one.

| File | Produces |
| --- | --- |
| `00-house-style.md` | the voice — read first, it governs the rest |
| `01-course.md` | a `#course` post |
| `02-course-lesson.md` | a `#lesson` post |
| `03-training-section.md` | a `#training-section` post |
| `04-training-lesson.md` | a `#training-content` post |
| `05-blog-post.md` | a `#blog` post |
| `06-resource.md` | a `#resource` post |
| `07-documentation.md` | a `documentation` post |
| `SITE-CONTEXT.md` | the single briefing to hand any AI working on this site |

## Why they matter to the THEME

Each prompt encodes the tag contract from `01-content-model.md` — which tags to
set, which internal tags carry metadata, what the slug must equal. **A prompt
that drifts from the templates produces content the templates cannot render.**

Concretely: if a course post is written without its slug matching its course
tag, the URL model in `01` breaks and Ghost 301s to the wrong course. The
prompt is where that rule gets enforced at authoring time.

## Keep in sync when you change

- a tag convention → every prompt that mentions it
- an internal-tag metadata field (`#learn-*`, `#prereq-*`, `#cert-*`) → the
  prompt for that content type
- an art-direction tag (`#hero-*`, `#posthead-*`) → the same
- `SITE-CONTEXT.md` → whenever the font stack, the design system, or the
  architecture changes. It has gone stale twice: once claiming Sentient was the
  editorial serif, once claiming mono was not shipped.

## `dummy-content/import.json`

ONE Ghost-importable bundle (Settings → Labs → Import) with 2–3 posts for every
collection and section, plus every tag the templates branch on. It encodes the
model rules from `routes.yaml` — a course post's slug equals its course tag, a
section post's slug equals its section tag, a lesson's primary tag is its
parent's tag.

**It is the only content fixture.** Extend it by editing the bundle; there are
no other content files. It is also the fastest way to get a local Ghost into a
state where every template can actually be looked at.
