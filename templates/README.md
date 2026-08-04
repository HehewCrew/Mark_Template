# templates/ — Brand Assets & Content Templates

- `logo/` — the locked brand logo files (vector + PNG) once designed, plus `logo/fonts/` for the brand's TTF/OTF files (used by mockup/dashboard tooling for font embedding) and optionally `logo/generator/` if the logo is produced programmatically.
- `<pillar-slug>/<series-slug>/` — confirmed content templates grouped by content pillar (same pillar slugs as `social/`): a Canva build sheet (`<slug>-template.md`) + HTML visual reference (`<slug>-final.html`), produced by the `template-generator` skill. Each confirmed build sheet is mirrored to `data/examples/posts/` (flat) for content agents — the copy here is canonical.
- If the brand needs a recurring generated graphic (diagrams, charts, boards — anything produced repeatedly to a locked spec), its generator script lives here too (e.g., `templates/<asset>/generator/`), with the spec locked in the `designer` skill.
