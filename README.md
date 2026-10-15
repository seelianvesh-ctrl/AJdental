# AJ Dental & Facial Aesthetics — Website Preview 03

**Status: design preview for client review. Not deployed. No GitHub changes made.**
Open `AJ_Dental_Preview.html` (identical to `index.html`) in any browser — it is a single
self-contained file (1.8 MB) with all fonts, photos and illustrative images embedded.
A local preview server (`python3 preview_server.py`, port 3000) serves the same file.

## What changed in Preview 03 (logo lock, 14 Oct 2026)

- **Logo locked: Ivory Primary (#1)** — ivory tooth + navy face silhouette, replacing the bright
  yellow (yellow reads as stained teeth). New assets `assets/aj-mark-ivory.webp` (shown in a navy
  chip on light surfaces) and `assets/aj-favicon.png` (ivory on navy tile). The reversed
  navy-on-cream version was created for light backgrounds (`/home/user/aj-logo-ivory-options.png`).
  Colour-option explorations: `/home/user/aj-logo-colour-options.png`.
- **Whitening & smile-design images generated** — all 10 services now have dedicated,
  text-matched illustrative visuals; the Preview 02 interims are gone.

## What changed in Preview 02 (per client brief, 14 Oct 2026)

1. **Studied `rojadental.vercel.app`** — adopted its flow patterns only: dual WhatsApp + Call
   CTAs in the hero, local-language warmth, filterable treatment cards each with its own
   WhatsApp enquiry, a big WhatsApp booking band, FAQ, and address/hours/directions block.
   None of its claims (painless/same-day/pricing) were copied — AJ facts only.
2. **10 unique named Google reviews** (target reached): Deepika Cheemala, Tarun,
   Adhilaxmi Kondru, Venkat Korumilli, Balaram Potnuru, Surya Vardhan Dadala, Boddapati Vijayalaxmi,
   Yamdamuri Babykumari, Chandu Reddy K, Sindhu Yandamuri — from the live profile plus the
   client's three Google screenshots, deduplicated (11 unique candidates found; the briefest,
   Kommanapalli Ashmi, was omitted). Drag/scroll carousel; tap a card for the full text.
3. **Direct booking.** Every "Book Appointment" opens WhatsApp directly
   (`wa.me/917997911390`) with a pre-written, context-specific message — per service,
   per doctor, aesthetics, hair. Call buttons use `tel:+917997911390` everywhere applicable.
4. **"Request a visit" → "Book Appointment"** throughout; sticky mobile Call/Book dock and a
   floating WhatsApp-green Book pill on desktop.
5. **Typography rebuilt** on researched readability guidance (Material Design type scale;
   WCAG 1.4.4 resize): body 17px desktop / 16.5px mobile, line-height ≈1.7–1.85, labels
   ≥12px, tap targets ≥48px. Verified no overlap/horizontal scroll at 320–1440px and at
   200% zoom (720 CSS px @2×).
6. **Telugu, elegantly:** embedded Noto Sans Telugu subset (68 KB) — hero line
   "మీ చిరునవ్వు, మా బాధ్యత", a scrolling welcome ribbon, and Telugu eyebrows in the
   services, journey, reviews, visit and Instagram sections. Small bottom footnote only for
   the rating snapshot / AI-illustration notes — no disclaimer banners.
7. **Engagement:** scroll-progress bar, subtle hero parallax, scroll-reveal, animated
   treatment tabs, an interactive 4-step "Your first visit" journey, hover-lift cards,
   drag-to-scroll reviews with progress bar, photo lightbox. All motion honours
   `prefers-reduced-motion` and can be toggled in the footer.
8. **Realistic AI-generated service imagery** for all 10 services, each matched to its text
   and labelled "Illustrative" on the image (they are not AJ patients/premises).
9. **Instagram** (@aj_dental_facial_aesthetics) has a dedicated band above the footer and a
   footer link; it is also in the page's structured data (`sameAs`).

## Fixed facts (client-confirmed)

- Phone/WhatsApp: **7997911390 only** · Hours: **Mon–Sat 9 AM–8 PM, Sunday by appointment**
- Address: **Road No. 3, Ayodhya Nagar, Kakinada, AP 533001**
- AJ-first branding; "Jubeda Dental" appears only in one FAQ (returning patients) plus invisible schema alternateName — the footer line was removed 2026-10-15 after client feedback
- No prices anywhere, including no implant fee

## QA (evidence/ folder)

- Playwright/Chromium suite `test_preview.py`: 9 check groups pass — content guards,
  per-service WhatsApp deep links, journey/tabs/dialogs/carousel, gallery, mobile dock,
  320–1440px + 200%-zoom no-overflow, reduced-motion, zero JS errors, zero external requests.
- axe-core (WCAG 2.0/2.1 A+AA): **0 violations** on desktop, mobile and dialog states
  (`evidence/accessibility-v2.json`, `evidence/preview-qa.json`). Not a formal certification.
- Screenshots: `evidence/v2-*.jpg`, `preview-desktop*.jpg`, `preview-mobile*.jpg`.
- Preview 01 is preserved in `preview01-backup/`.

## Files

- `AJ_Dental_Preview.html` / `index.html` — the deliverable (built file, identical)
- `template.html`, `styles.css`, `app.js`, `content.json`, `care-topics.json` — sources
- `assemble_preview.py` — rebuilds the single HTML (`python3 assemble_preview.py`), stdlib only
- `assets/` — clinic/doctor WebP photos, brand mark, embedded fonts (Instrument Serif,
  Manrope, Noto Sans Telugu subset — all OFL), AI service images (JPG masters + WebP)
- `AJ_Dental_Design_Research.md` — benchmark rationale from Preview 01

## Still open before launch

- Get a print-ready vector (SVG/AI) of the locked ivory logo for outdoor signage
- Client approval of this design → then GitHub repo + hosting decision
  (Vercel Hobby is non-commercial only; use a paid/suitable host)
- Confirm doctor credentials/service availability wording; recheck Google rating snapshot
