# data/examples/ — Content Reference Library

Reference material content agents read before generating anything:

- **Craft docs** (e.g., a storytelling best-practices playbook) — hook types, narrative structure (hook → stakes → build → payoff → CTA), pacing, format-selection rules for the brand's platform. Write one during/after onboarding; the story-spine structure is platform-agnostic and worth adopting for any brand.
- **`posts/`** — the confirmed-template library: one build sheet per series, copied from `templates/<pillar>/<slug>/` (the canonical copy). Content agents read these to know exactly which `{{...}}` slots to fill per post. Never edit the copies here directly — edit the canonical file under `templates/` and re-copy.
