# Mockup Page Guide — verified mechanics

How to build the self-contained mockup/reference HTML pages (template mockups, dashboards, decks).

## 1. Write the HTML with placeholders first

Author the page with the Write tool using `__HEADLINE_B64__` and `__BODY_B64__` font placeholders — never paste base64 through chat context. Skeleton:

```html
<title>{{BRAND_NAME}} — <name> mockups</title>
<style>
@font-face { font-family: '<HeadlineFont>'; src: url(data:font/ttf;base64,__HEADLINE_B64__) format('truetype'); }
@font-face { font-family: '<BodyFont>';     src: url(data:font/ttf;base64,__BODY_B64__) format('truetype'); }
/* locked palette only — hexes from context/Style_Guide.md §2.1 */
:root { --primary:#______; --secondary:#______; --bg:#______; --text:#______; }
.stage { display:flex; gap:24px; justify-content:center; flex-wrap:wrap; padding:24px; }
.slide { background:var(--bg); border-radius:8px; box-shadow:0 4px 16px rgba(0,0,0,.25);
         box-sizing:border-box; overflow:hidden; position:relative; }
/* 30%-scale frames: carousel 1080×1350 → 324×405; square → 324×324; vertical 1080×1920 → 324×576 */
.s-carousel { width:324px; height:405px; }
.s-square   { width:324px; height:324px; }
.s-vertical { width:324px; height:576px; }
.headline { font-family:'<HeadlineFont>', serif; color:var(--text); }
.body-txt { font-family:'<BodyFont>', sans-serif; color:var(--text); line-height:1.7; }
</style>
<div class="stage" dir="<rtl|ltr per the brand's language>">
  <!-- Direction A: <one-line rationale> -->
  <div class="slide s-carousel"> ... cover ... </div>
  <div class="slide s-carousel"> ... body slide ... </div>
  <!-- Directions B and C follow -->
</div>
```

Notes:
- No `<!DOCTYPE>`/`<html>`/`<head>`/`<body>` wrapper if publishing via Artifact (it wraps for you); harmless either way for local browser viewing.
- Set `dir="rtl"` on the container for RTL scripts — browsers shape Arabic/Hebrew natively; nothing else needed.
- Since px values in the frames are 30% scale, keep a comment mapping scale→real px (e.g., headline 29px here ≙ 96px on the 1080 canvas) so the build sheet numbers stay honest.
- Logo: paste the brand `<svg>...</svg>` from `templates/logo/` inline once it exists (vector-outlined SVGs have no font dependency).
- Sample copy: real illustrative text in the brand's language with glossary-standard terms — never lorem ipsum.

## 2. Inject the fonts (verified command pattern)

PowerShell (Windows):

```powershell
$fonts = "templates\logo\fonts"
$head = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$fonts\<HeadlineFont>.ttf"))
$body = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$fonts\<BodyFont>.ttf"))
$html = [IO.File]::ReadAllText("<template-with-placeholders>.html", [Text.Encoding]::UTF8)
$html = $html.Replace("__HEADLINE_B64__", $head).Replace("__BODY_B64__", $body)
[IO.File]::WriteAllText("templates\<pillar-slug>\<slug>\<slug>-mockups.html", $html, (New-Object Text.UTF8Encoding $false))
```

Bash equivalent:

```bash
python - <<'EOF'
import base64, pathlib
head = base64.b64encode(pathlib.Path('templates/logo/fonts/<HeadlineFont>.ttf').read_bytes()).decode()
body = base64.b64encode(pathlib.Path('templates/logo/fonts/<BodyFont>.ttf').read_bytes()).decode()
p = pathlib.Path('template-with-placeholders.html')
out = p.read_text(encoding='utf-8').replace('__HEADLINE_B64__', head).replace('__BODY_B64__', body)
pathlib.Path('templates/<pillar-slug>/<slug>/<slug>-mockups.html').write_text(out, encoding='utf-8')
EOF
```

Write the placeholder template into the scratchpad; only the injected final lands in `templates/<pillar-slug>/<slug>/`.

## 3. Present

- **Artifact tool available:** publish the injected file (fully self-contained — data-URI fonts pass the no-external-hosts CSP). Load the `artifact-design` skill first, per the Artifact tool's requirement. The brand's locked design system takes precedence over generic design guidance.
- **No Artifact tool:** tell the user to open the file in a browser.

Then AskUserQuestion for the A/B/C pick.

## Gotchas (learned the hard way)

- Write the final file as UTF-8 **without BOM** (`New-Object Text.UTF8Encoding $false`) — PowerShell 5.1's default encoding is UTF-16, which browsers may misread and which doubles the file size.
- Don't pass non-ASCII text through PowerShell command arguments — author all content in files via the Write tool (UTF-8 safe) and let PowerShell only do byte-level base64/replace work.
- Two TTFs typically add ~200–300 KB base64 — fine for a local file or Artifact; don't inline them more than once per page.
