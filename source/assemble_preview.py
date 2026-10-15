from pathlib import Path
from urllib.parse import quote
import json, base64, html, re

ROOT = Path('/home/user/aj-dental-website')
site = json.loads((ROOT / 'content.json').read_text())
WA_BASE = site['whatsapp']  # https://wa.me/917997911390

def wa(message):
    return WA_BASE + '?text=' + quote(message)

WA_GENERAL = wa('Hi AJ Dental, I would like to book an appointment. Please let me know the available slots.')
WA_AESTHETICS = wa('Hi AJ Dental, I would like to enquire about a facial aesthetics consultation. Please share the details.')
WA_HAIR = wa('Hi AJ Dental, I would like to enquire about hair care. Please share the details.')

CARE = [
 {'id':'implants','title':'Dental implants','short':'A conversation about replacing a missing tooth.','detail':'If you are considering a dental implant, ask about an assessment and the options for replacing your missing tooth. We\u2019ll discuss suitability, the treatment plan and our current availability with you at your consultation.','booking':'Dental implant enquiry','image':'assets/implants.webp','alt':'Illustrative image: a dentist explaining a dental implant model to a patient','wa':'Hi AJ Dental, I would like to enquire about dental implants for a missing tooth. Please let me know the available slots for a consultation.','questions':['What options are appropriate in my situation?','Which practitioner would assess and treat me?','What would the treatment and follow-up involve?']},
 {'id':'dentures','title':'Crowns, bridges & dentures','short':'Discuss ways to repair a damaged tooth or replace missing teeth.','detail':'A crown can protect and rebuild a damaged tooth, while a bridge or dentures can replace missing teeth. Use a consultation to ask which option may suit you, what is involved in making and fitting it, and how to care for it over time.','booking':'Crowns, bridges or dentures enquiry','image':'assets/dentures.webp','alt':'Illustrative image: ceramic bridge work being prepared on a dental model','wa':'Hi AJ Dental, I would like to book an appointment about a crown, bridge or dentures. Please let me know the available slots.','questions':['Would a crown, a bridge or dentures suit my situation?','What is involved in making and fitting them?','How would I care for them afterwards?']},
 {'id':'root-canal','title':'Root canal treatment','short':'Explore the next step when a tooth needs attention on the inside.','detail':'If you have a question about root canal treatment or a tooth that is troubling you, start with an assessment. We can discuss the concern with you and which options may be suitable.','booking':'Root canal consultation','image':'assets/rootcanal.webp','alt':'Illustrative image: root canal treatment using a dental microscope','wa':'Hi AJ Dental, I would like to book an appointment about root canal treatment. Please let me know the available slots.','questions':['Is this treatment appropriate for my tooth?','What would the visits involve?','What should I ask about recovery and follow-up?']},
 {'id':'extraction','title':'Extractions & impactions','short':'Ask about tooth removal, including impacted (wisdom) teeth.','detail':'If you have been advised to consider removing a tooth \u2014 including an impacted wisdom tooth \u2014 discuss the assessment, options and aftercare with us. This website is not a substitute for that individual conversation.','booking':'Tooth removal enquiry','image':'assets/extraction.webp','alt':'Illustrative image: a dentist explaining a wisdom tooth on a jaw model before treatment','wa':'Hi AJ Dental, I would like to book an appointment about tooth removal or an impacted tooth. Please let me know the available slots.','questions':['Is removal the right next step for this tooth?','Is my tooth impacted, and what does that mean?','What should I expect at the appointment?','What aftercare and follow-up should I plan for?']}
]
 
for item in CARE:
    item['wa_url'] = wa(item['wa'])
(ROOT / 'care-topics.json').write_text(json.dumps(CARE, indent=2, ensure_ascii=False))

def data_uri(path, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode((ROOT / path).read_bytes()).decode()

star = '<svg class="star" aria-hidden="true"><use href="#i-star"/></svg>'
stars = star * 5
CHAT = '<svg class="icon" aria-hidden="true"><use href="#i-chat"/></svg>'
PHONE = '<svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg>'

def card(item, n):
    img = data_uri(item['image'], 'image/webp')
    return (f'<article class="care-item"><button class="care-media" data-care="{item["id"]}" aria-label="Explore {html.escape(item["title"], quote=True)}">'
            f'<img data-care-img="{item["id"]}" src="{img}" width="1000" height="558" loading="lazy" alt="{html.escape(item["alt"], quote=True)}">'
            f'<span class="care-chip" aria-hidden="true">Illustrative</span></button>'
            f'<div class="care-body"><span class="care-number" aria-hidden="true">{n:02}</span><h3>{html.escape(item["title"])}</h3><p>{html.escape(item["short"])}</p>'
            f'<div class="care-actions">'
            f'<button class="care-more" data-care="{item["id"]}">Details</button>'
            f'<a class="care-wa" href="{html.escape(item["wa_url"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp AJ Dental about {html.escape(item["title"], quote=True)}">{CHAT}</a>'
            f'<a class="care-call" href="tel:+917997911390" aria-label="Call AJ Dental about {html.escape(item["title"], quote=True)}">{PHONE}</a></div></div></article>')

def highlight(text, phrases):
    out = html.escape(text)
    for phrase in sorted(phrases, key=len, reverse=True):
        ep = html.escape(phrase)
        if ep in out:
            out = out.replace(ep, f'<strong>{ep}</strong>', 1)
    return out

def review_card(r, n):
    more = f'<button class="review-more" data-review="{n}">Read full review</button>' if r['is_excerpt'] else ''
    return (f'<article class="review-card" data-review="{n}" aria-label="Google review by {html.escape(r["name"], quote=True)}">'
            f'<div class="review-card-top"><div class="stars" role="img" aria-label="Rated 5 out of 5 stars">{stars}</div>'
            f'<span class="review-google"><span class="google-g" aria-hidden="true">G</span> Google</span></div>'
            f'<blockquote class="review-quote">“{highlight(r["quote"], r.get("highlights", []))}”</blockquote>{more}'
            f'<footer><span class="review-author">{html.escape(r["name"])}</span>'
            f'<span class="review-meta">Google review · {html.escape(r["date_label_observed"])}</span></footer></article>')

fonts = []
for name, path, style, weight in [('Instrument Serif','assets/instrument-serif-normal.woff2','normal','400'),('Instrument Serif','assets/instrument-serif-italic.woff2','italic','400'),('Manrope','assets/manrope-normal.woff2','normal','200 800')]:
    fonts.append(f"@font-face{{font-family:'{name}';src:url('{data_uri(path,'font/woff2')}') format('woff2');font-style:{style};font-weight:{weight};font-display:swap;}}")
telugu = ROOT / 'assets/noto-sans-telugu-600.woff2'
if telugu.exists():
    fonts.append(f"@font-face{{font-family:'Noto Sans Telugu';src:url('{data_uri('assets/noto-sans-telugu-600.woff2','font/woff2')}') format('woff2');font-style:normal;font-weight:400 700;font-display:swap;}}")
licenses = []
for p in ['assets/instrumentserif-OFL.txt','assets/manrope-OFL.txt']:
    if (ROOT / p).exists():
        licenses.append('<!-- Embedded-font license: ' + p + ' (Noto Sans Telugu subset is OFL-licensed; source: fonts.google.com/noto/specimen/Noto+Sans+Telugu)\n' + (ROOT / p).read_text().replace('--', '—') + '\n-->')

schema = {
 '@context':'https://schema.org','@type':'Dentist','name':site['name'],'alternateName':['Jubeda Dental', "Dr. Jubeda’s Dental & Facial Aesthetics"],
 'telephone':site['phone_e164'],
 'address':{'@type':'PostalAddress','streetAddress':'Road No. 3, Ayodhya Nagar','addressLocality':'Kakinada','addressRegion':'Andhra Pradesh','postalCode':'533001','addressCountry':'IN'},
 'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],'opens':'09:00','closes':'20:00'}],
 'hasMap':site['maps_url'],'sameAs':[site['maps_url'], site.get('instagram_url','https://www.instagram.com/aj_dental_facial_aesthetics/'), site.get('facebook_url',''), site.get('youtube_url','')]
}
public_site = {k: site[k] for k in ['name','phone_e164','phone_display','whatsapp','maps_url','opening_hours','review_policy','publication_ready']}
public_site['reviews'] = [{k: r[k] for k in ['name','quote','full_text','rating','source','source_url','checked_date','is_excerpt','date_label_observed','highlights']} for r in site['reviews']]
public_care = [{k: c[k] for k in ['id','title','short','detail','questions','wa_url']} for c in CARE]

replacements = {
 'FONTS':'\n'.join(fonts),'CSS':(ROOT / 'styles.css').read_text(),'JS':(ROOT / 'app.js').read_text(),
 'MARK':data_uri('assets/aj-mark-ivory.webp','image/webp'),'FAVICON':data_uri('assets/aj-favicon.png','image/png'),'DOCTOR':data_uri('assets/doctor-ankitha.webp','image/webp'),'DOCTOR_JOE':data_uri('assets/doctor-joe.webp','image/webp'),
 'OPERATORY':data_uri('assets/clinic-operatory.webp','image/webp'),'RECEPTION':data_uri('assets/clinic-reception.webp','image/webp'),'EXTERIOR':data_uri('assets/clinic-exterior.webp','image/webp'),
 'STARS':stars,'MAP':html.escape(site['maps_url'], quote=True),'DIRECTIONS':html.escape(site['directions_url'], quote=True),
 'WA_GENERAL':html.escape(WA_GENERAL, quote=True),'WA_AESTHETICS':html.escape(WA_AESTHETICS, quote=True),'WA_HAIR':html.escape(WA_HAIR, quote=True),
 'SCHEMA':json.dumps(schema, ensure_ascii=False).replace('</', '<\\/'),
 'SITE_DATA':json.dumps(public_site, ensure_ascii=False).replace('</', '<\\/'),
 'CARE_DATA':json.dumps(public_care, ensure_ascii=False).replace('</', '<\\/'),
 'FONT_LICENSES':'\n'.join(licenses),
 'CARE_ALL':'\n'.join(card(x, i + 1) for i, x in enumerate(CARE)),
 'REVIEW_CARDS':'\n'.join(review_card(r, n) for n, r in enumerate(site['reviews']))
}
s = (ROOT / 'template.html').read_text()
for key, value in replacements.items():
    s = s.replace('@@' + key + '@@', value)
assert not re.search(r'@@[A-Z_]+@@', s), 'Unreplaced template token'
for disallowed in ['9008553086','9010000021','7383581638','25,000','25000','localhost','127.0.0.1']:
    assert disallowed not in s, disallowed
assert '<meta name="robots" content="index,follow">' in s and 'noindex' not in s, 'Site is live: must be indexable, no preview markers'
assert 'Design preview' not in s and 'Not live' not in s, 'No preview wording may ship'
assert 'aggregateRating' not in json.dumps(schema)
assert len(site['reviews']) == 10 and all(r['source'] == 'Google' for r in site['reviews'])
assert len({r['name'] for r in site['reviews']}) == 10, 'Reviewer names must be unique'
assert '<form' not in s and 'appointmentDialog' not in s and 'data-book' not in s, 'No forms or form-style booking may remain'
assert 'Request a visit' not in s and 'Request your visit' not in s
assert 'Book Appointment' in s and s.count('wa.me/917997911390?text=') >= 12, 'Direct WhatsApp deep links expected throughout'
assert 'instagram.com/aj_dental_facial_aesthetics' in s
assert 'facebook.com/people/AJ-Dental-Facial-Aesthetics' in s and 'youtube.com/@AJ_Dental_Facial_Aesthetics' in s
assert 'Oral Physician & Radiologist' in s and 'Oral Medicine' not in s
assert '9 AM–8 PM' in s and '10 AM–8 PM' not in s and 'Sunday closed' not in s
assert 'Earlier known as Jubeda Dental' not in s, 'Footer legacy line removed by client decision'
assert len(CARE) == 4
assert 'G-LHL2H84Z37' in s and 'www.googletagmanager.com' in s, 'GA4 tag must be wired'
assert all((ROOT / c['image']).exists() for c in CARE), 'Every service needs an image'
assert 'A16267' in s and 'A23045' in s, 'Doctor registration numbers must appear'
assert 'Dr. B. Joe Praveen' in s and 'Dr. M. Ankitha' in s, 'Visiting-card doctor names must appear'
assert 'Ankitha Masa' not in s, 'Use the visiting-card name Dr. M. Ankitha everywhere'
(ROOT / 'AJ_Dental_Preview.html').write_text(s)
(ROOT / 'index.html').write_text(s)
print('Generated self-contained HTML:', len(s.encode()), 'bytes; Google reviews:', len(site['reviews']), 'of', site['review_policy']['target_count'])
print('Services with illustrative images:', len(CARE), '; WhatsApp deep links:', s.count('wa.me/917997911390?text='), '; tel links:', s.count('tel:+917997911390'))
print('Fonts embedded: Instrument Serif, Manrope, Noto Sans Telugu subset; external runtime assets: 0')
