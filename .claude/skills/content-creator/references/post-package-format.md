# Post Export Package — Output Skeleton

Format for `social/queue/<YYYY-MM-DD>-<series-slug>.md`. Everything the user needs to produce the post in the production tool without reopening the sources or the chat.

```markdown
# <Series Name> — <episode topic> (<YYYY-MM-DD>)

> Status: APPROVED by user on <date> — ready for production.
> Template: `data/examples/posts/<series-slug>-template.md` (visual ref: `templates/<pillar-slug>/<series-slug>/<series-slug>-final.html`)
> After publishing: this file moves to `social/<pillar-slug>/<series-slug>/` (content-creator Step 8).
> Source: <source>, <pages/link> (paraphrased — no verbatim text). Fact-checks: <links/notes or "n/a">

## Fill sheet
Open the saved brand template for this series in the production tool and replace each slot:

| Slide | Slot | Final text (copy-paste) |
|---|---|---|
| 1 | `{{HOOK}}` | <approved hook> |
| 2 | `{{BODY_1}}` | <approved body> |
| … | … | … |
| N | `{{CTA}}` | <approved CTA> |

Slide count: <N> (per user approval)

## Generated assets (when the template has image slots)
| Slot | File (same folder) | Produced from |
|---|---|---|
| `{{IMG_1}}` | `<date>-<slug>-asset-1.png` | <the data/spec used> |

## Caption (copy-paste)
<approved caption — keyword-rich, glossary terms with the pairing rule, ends with engagement prompt>

## Alt text
<one-line descriptive alt text with natural keywords>

## Pre-publish checklist (run before posting)
- [ ] Correct series for the day per rotation
- [ ] Terms match the glossary; pairing rule on first mention
- [ ] Only locked palette colors & locked typography
- [ ] Caption ends with engagement prompt
- [ ] No unconfirmed product claims
- [ ] Alt text added
(full list: `sop/SOP.md` §2)

## Gist (for the record)
<2–4 sentences: what this post teaches/tells, and the source it paraphrases>
```

Rules for the generating agent:
- Only APPROVED text goes in — this file is written after the Step 5 review gate, never before.
- The slot names must match the series template exactly; if the template lacks a slot the content needs, flag it to the user instead of inventing one (the template may need a revision via template-generator).
- Keep the file self-sufficient: the user should produce the post from this file + the production tool alone.
