# AJ Dental & Facial Aesthetics — Website

Live site: **https://ajdental.vercel.app** · single self-contained `index.html` (all fonts, photos and illustrative images embedded; zero external runtime assets).

## Highlights

- **AJ-first branding** with the locked Ivory Primary logo (ivory tooth + navy face silhouette).
- **Direct booking.** Every booking action opens WhatsApp (`wa.me/917997911390`) with a pre-written, context-specific message — per service, per doctor, aesthetics, hair. Call actions use `tel:+917997911390` everywhere applicable. No forms.
- **10 unique named Google reviews** (verbatim quotes, keyword highlights): Deepika Cheemala, Tarun, Adhilaxmi Kondru, Venkat Korumilli, Balaram Potnuru, Surya Vardhan Dadala, Boddapati Vijayalaxmi, Yamdamuri Babykumari, Chandu Reddy K, Sindhu Yandamuri.
- **6 core dental services** as photo cards, led by our two specialities — **Orthodontics** (braces & aligners, Dr. B. Joe Praveen) and **Oral Medicine & Radiology** (Dr. M. Ankitha) — followed by Dental Implants, Crowns/Bridges & Dentures, Root Canal Treatment and Extractions & Impactions. Each has contextual WhatsApp + call icon links and a details dialog.
- **Doctors presented together** — Dr. B. Joe Praveen (MDS · Orthodontist · Assistant Professor · Reg No: A16267) and Dr. M. Ankitha (MDS · Oral Physician & Radiologist · Asst. Professor · Reg No: A23045) — with portrait hero switcher and bio dialogs.
- **Telugu warmth** (embedded Noto Sans Telugu subset): hero line "మీ చిరునవ్వు, మా బాధ్యత", welcome ribbon, and Telugu eyebrows.
- **Case:** proper case throughout, including mid-sentence designations (“meeting a Dentist”, “our Orthodontist”, “a particular Doctor’s availability”). No `text-transform` anywhere in the CSS, so headings, eyebrows, kickers, chips and nav labels render exactly as authored. Google review quotes stay verbatim.
- **Polished UX:** researched type scale (body 17px desktop / 16.5px mobile), ≥48px tap targets, no overflow at 320–1440px or 200% zoom, scroll-reveal and micro-motion that honour `prefers-reduced-motion` (footer toggle), drag-to-scroll reviews, photo lightbox, sticky mobile Call/Book dock.
- **Google Analytics 4** (`G-LHL2H84Z37`) with custom events `whatsapp_click`, `call_click`, `directions_click`, `social_click`; the tag runs on real hostnames only.
- **Socials:** Instagram, Facebook and YouTube — cards, footer links and schema `sameAs`.

## Fixed facts (client-confirmed)

- Phone/WhatsApp: **7997911390 only** · Hours: **Mon–Sat 9 AM–8 PM, Sunday by appointment**
- Address: **Road No. 3, Ayodhya Nagar, Kakinada, AP 533001**
- AJ-first branding; "Jubeda Dental" appears only in one FAQ (returning patients) plus invisible schema `alternateName` — the footer line was removed 2026-10-15 after client feedback
- No prices anywhere, including no implant fee
- Service imagery is AI-generated (3D jaw illustrations) and labelled "Illustrative" — not AJ patients or premises
- Clinic photographs are **client-supplied originals** of the Ayodhya Nagar premises (received 24 Oct 2026); source files and consent status are recorded in `source/assets/photo-manifest.json`

## Testing (`evidence/` folder)

- Playwright/Chromium suite (`test_preview.py`): 8 check groups pass — content guards, per-service contextual WhatsApp links, dialogs/carousel, gallery, mobile dock, 320–1440px + 200%-zoom no-overflow, reduced-motion, zero JS errors, zero external runtime requests.
- axe-core (WCAG 2.0/2.1 A+AA + best-practice rules): **0 violations** on desktop and mobile. Not a formal certification.
- Screenshots: `evidence/v*-*.jpg`, `preview-desktop*.jpg`, `preview-mobile*.jpg`.

## Files

- `index.html` — the deployable site (single self-contained file)
- `source/` — `template.html`, `styles.css`, `app.js`, `content.json`, `care-topics.json`, `assets/`
- `source/assemble_preview.py` — rebuilds the single HTML (`python3 assemble_preview.py`), stdlib only
- `source/test_preview.py` — Playwright QA suite
- `og-image.jpg` — share card (ivory logo on brand navy)

## Notes

- Hosting: Vercel Hobby is non-commercial only — a production clinic site needs a paid/suitable plan or another host.
- Google Analytics setup: acknowledge User Data Collection in GA4 Admin; mark `whatsapp_click`, `call_click`, `directions_click` as key events after the first real traffic appears.
- Get a print-ready vector (SVG/AI) of the locked ivory logo for outdoor signage.
