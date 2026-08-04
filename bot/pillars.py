"""Series → content-pillar mapping.

Used only to *guess* which pillar folder a queue package archives into when it
is marked posted. The bot always shows every pillar and lets the guess be
confirmed or overridden, so a wrong guess costs one tap and an empty map costs
nothing — you just pick from the full list every time.

## Filling this in

`PILLAR_SLUGS` must match the content pillars defined in
`context/Marketing_Strategy.md` §1.1, because those same slugs are the folder
names under `social/` and `templates/`. The set below is a generic starter —
replace it with this brand's pillars during `/brand-onboarding`.

`_SERIES_BY_PILLAR` ships empty on purpose: series names are brand-specific and
are only known once the content rotation is defined. Add them as the rotation
settles — series names in the planner tend to drift slightly from the strategy
doc's canonical list, so listing every alias you actually use is what makes the
guess land.
"""

from __future__ import annotations

PILLAR_SLUGS = ("educational", "storytelling", "behind-the-scenes", "community", "products")

PILLAR_LABELS = {
    "educational": "Educational",
    "storytelling": "Storytelling",
    "behind-the-scenes": "Behind-the-Scenes",
    "community": "Community",
    "products": "Products",
}

# Lowercase series names (and their aliases) per pillar, e.g.
#     "educational": ["how it works", "myth busting"],
_SERIES_BY_PILLAR: dict[str, list[str]] = {slug: [] for slug in PILLAR_SLUGS}


def guess_pillar(series_name: str) -> tuple[str | None, bool]:
    """Returns (pillar, exact). exact=True only when the normalized series
    name matches a known series name exactly — safe to act on with a single
    confirm button. False means a fuzzy substring match (still just a
    guess — the planner's series text sometimes carries extra annotation,
    e.g. a swap note — needs the full pillar picker to confirm)."""
    norm = series_name.strip().lower().rstrip("?")
    for pillar, names in _SERIES_BY_PILLAR.items():
        if norm in names:
            return pillar, True
    for pillar, names in _SERIES_BY_PILLAR.items():
        for n in names:
            if n in norm or norm in n:
                return pillar, False
    return None, False
