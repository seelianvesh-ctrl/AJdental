# AJ Dental & Facial Aesthetics — Website

Design **Preview 03** for AJ Dental & Facial Aesthetics, Ayodhya Nagar, Kakinada.
Status: **design preview — not yet approved for public launch** (the page carries a
`noindex` tag and a small "Design preview 03 · Not live" footer label on purpose).

## View the site
Open `index.html` in any browser. It is a single self-contained file (fonts, photos and
illustrations embedded); no server or build step is needed to view it.

## Confirmed clinic facts used on the site
- Phone / WhatsApp: **+91 79979 11390** (only number shown)
- Hours: **Monday–Saturday, 10 AM–8 PM · Sunday closed**
- Address: **Road No. 3, Ayodhya Nagar, Kakinada, Andhra Pradesh 533001**
- Every "Book Appointment" opens WhatsApp with a pre-written, service-specific message.
  Call buttons dial the number above. No prices are published anywhere.

## Editing
Editable sources are in `source/`:
- `template.html`, `styles.css`, `app.js` — page, design, behaviour
- `content.json`, `care-topics.json` — clinic data, reviews, services
- `assets/` — photos, fonts (all OFL-licensed), logo (ivory-on-navy, locked design), AI service illustrations

Rebuild the single file after editing:
```
cd source
python3 assemble_preview.py
```
It regenerates `AJ_Dental_Preview.html` / `index.html` inside `source/` — copy the new
`index.html` to the repo root afterwards.

## Before public launch
- [ ] Client approves the design
- [ ] Remove `noindex,nofollow` meta and the "Design preview · Not live" footer label
- [ ] Get a print-ready vector (SVG/AI) of the ivory logo for signage
- [ ] Recheck the Google rating snapshot (5.0 · 62 reviews, checked 14 Oct 2026)
- [ ] Hosting: GitHub Pages works well for this static site (Settings → Pages →
      deploy from `main`, root). A custom domain can be attached later.
