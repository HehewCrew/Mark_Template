# Build Sheet — Output Skeleton

Use this structure for `templates/<pillar-slug>/<slug>/<slug>-template.md` (pillar slugs per `context/Marketing_Strategy.md` §1.1). Keep the repo doc conventions: header blockquote with cross-refs, `Last updated:` date, ends with an Open / To Be Defined checklist.

```markdown
# <Series/Product Name> — Template Build Sheet

> Recreate-once spec for the <name> template. Visual reference: `<slug>-final.html` (open in browser).
> Design system: `../../../context/Style_Guide.md` (locked palette + fonts). Content structure: the craft doc in `../../../data/examples/`.
> Last updated: <YYYY-MM-DD>

## Canvas
- Size: <W×H> px
- Background: <locked background color> (or per chosen direction)
- Text direction: <LTR/RTL per the brand's language>

## Slide 1 — Cover
| # | Element | Position / size | Font & size | Color | Content |
|---|---|---|---|---|---|
| 1 | Series wordmark | top-center, y≈90px | <headline font> 64px | <primary hex> | <fixed series name> |
| 2 | Hook headline | center, max-width 880px | <headline font> 96px | <text hex> | `{{HOOK}}` (short — first-frame rule per the craft doc) |
| 3 | Logo | bottom-center, width≈160px | — | brand SVG (`templates/logo/`) | fixed |

## Slide 2..N — Body
<same table format — one per distinct layout; identical layouts can share one table with a note "repeat for slides 3–7">

## Last slide — CTA
<engagement prompt slot `{{CTA}}` — never a hard sell; see guardrails in the skill>

## Placeholder slots (fill per episode)
| Slot | Rule |
|---|---|
| `{{HOOK}}` | short, hook type per the series' row in the craft doc's hook library |
| `{{TERM}}` | glossary-standard term with the pairing rule on first mention |
| `{{BODY_n}}` | one idea per slide |
| `{{CTA}}` | question/challenge/invitation |
| `{{HOLDING_RESPONSE}}` | only slot allowed to reference price/specs until locked in `Products.md` |

## Build it in the production tool (one time)
1. Create design → Custom size <W×H> px.
2. Confirm the brand kit is active (locked colors + fonts). If a font is missing, upload the files from `templates/logo/fonts/`.
3. Recreate each slide from the tables above, checking against `<slug>-final.html` side-by-side.
4. Fill every `{{...}}` region with the literal placeholder text so future duplicates show what to replace.
5. Save as a brand template (or a named design to duplicate).

## Batch production
For each new episode: duplicate the template → replace the `{{...}}` slots → run the pre-publish checklist (`../../../sop/SOP.md` §2) → export per the format's spec.

## Open / To Be Defined
- [ ] <anything the user deferred>
```

Notes for the generating agent:
- Every row's font/size/color must match the chosen mockup direction exactly — the build sheet and `<slug>-final.html` are two views of one spec; they must not drift.
- Positions are guidance for a human rebuilding in the tool: prefer "top-center, y≈90px" over raw coordinates alone.
- Don't spec elements the production tool can't reproduce simply — if a direction used one, translate it to an achievable equivalent and note the substitution.
