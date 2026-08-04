# {{BRAND_NAME}} Content Planner — Episode Schedule & Done-Log

> Living planner: which episode runs on which day, grounded in the reference material (`data/references/`), and which episodes are already produced (redundancy guard).
> Rotation authority: `../context/Marketing_Strategy.md` §1.3. This file schedules *episodes into* that rotation — it never changes the rotation itself.
> Consumed and updated by the `content-creator` skill. An episode isn't "done" until its box is checked and the export package is linked.
> Last updated: {{DATE}}

---

## Week anchor

**Week 1 of the rotation starts Monday {{START_DATE}}** (first production cycle in this workspace — for an existing brand this is when the workspace takes over the schedule, not a launch date). Parity from then on: weeks alternate 1 → 2 → 1 → 2 continuously (if the rotation is bi-weekly). *(Adjust this anchor line if the start shifts, and the whole schedule shifts with it.)*

---

## Cycle 1 — Week 1 ({{WEEK_1_START}} → {{WEEK_1_END}})

| Day | Date | Series | Episode topic | Source grounding | Done |
|---|---|---|---|---|---|
| Mon | | {{SERIES}} | {{TOPIC}} | {{SOURCE + pages/link}} | [ ] |
| Tue | | | | | [ ] |
| Wed | | | | | [ ] |
| Thu | | | | | [ ] |
| Fri | | | | | [ ] |
| Sat | | | | | [ ] |
| Sun | | | | | [ ] |

## Cycle 1 — Week 2 (if bi-weekly)

| Day | Date | Series | Episode topic | Source grounding | Done |
|---|---|---|---|---|---|
| Mon | | | | | [ ] |
| … | | | | | [ ] |

---

## Episode log (all-time, prevents redundancy)

Move episodes here when checked done, with the export package link:

*(none yet — for an existing brand, seed this log during onboarding with recently published topics so the redundancy guard knows what's already been done)*

**Redundancy rule:** before generating any episode, search this file for the topic AND the source — same topic or same primary source twice = pick the next planned episode instead. Same source is acceptable only with a genuinely different angle.

---

## Appendix — Source → Series map (for planning future cycles)

<!-- Once reference material exists in data/references/, map each source to the series it can feed (with page ranges / sections), so planning future cycles is a lookup, not research. Baydaq's example mapped each chess book's table of contents to specific series. -->

*(build this during onboarding / when reference material is added)*

---

## Open / To Be Defined

- [ ] Set the week anchor once the actual start date is locked (launch date for a new brand; takeover date for an existing one)
- [ ] Add reference material to `data/references/` and build the Appendix source→series map
- [ ] Plan Cycle 1 episodes
- [ ] Native-speaker/expert review pass over the first cycle's content before publishing begins (if applicable)

---

*Works alongside `../context/Marketing_Strategy.md` (rotation), `data/examples/` (craft references), and the `content-creator` skill (execution). Check episodes off here — an unchecked episode is not done.*
