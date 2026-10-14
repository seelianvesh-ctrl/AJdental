from pathlib import Path
from urllib.parse import quote
import json, base64, html, re

ROOT = Path(__file__).resolve().parent
site = json.loads((ROOT / 'content.json').read_text())
WA_BASE = site['whatsapp']  # https://wa.me/917997911390

def wa(message):
    return WA_BASE + '?text=' + quote(message)

WA_GENERAL = wa('Hi AJ Dental, I would like to book an appointment. Please let me know the available slots.')
WA_AESTHETICS = wa('Hi AJ Dental, I would like to enquire about a facial aesthetics consultation. Please share the details.')
WA_HAIR = wa('Hi AJ Dental, I would like to enquire about hair care. Please share the details.')

CARE = [
 {'id':'checkup','group':'routine','title':'Check-ups & consultations','short':'A place to begin when you have questions about your teeth, gums or mouth.','detail':'Start with a conversation about your concerns and an assessment of your oral health. You do not need to choose a procedure before meeting a dentist.','booking':'General dental consultation','image':'assets/checkup.webp','alt':'Illustrative image: a dentist discussing a dental chart on a tablet with a patient','wa':'Hi AJ Dental, I would like to book a dental check-up and consultation. Please let me know the available slots.','questions':['What should I bring to the appointment?','Which concerns should we look at first?','What would the next step involve?']},
 {'id':'cleaning','group':'routine','title':'Teeth cleaning & polishing','short':'Professional cleaning, and looking after your teeth between visits.','detail':'If you would like to enquire about professional teeth cleaning and polishing, book a visit and ask the dentist about your gum health and the care that may be appropriate for you.','booking':'Teeth cleaning enquiry','image':'assets/cleaning.webp','alt':'Illustrative image: professional teeth cleaning in progress','wa':'Hi AJ Dental, I would like to book an appointment for teeth cleaning and polishing. Please let me know the available slots.','questions':['Would cleaning be appropriate for me now?','What should I expect at the visit?','How should I look after my teeth afterwards?']},
 {'id':'screening','group':'routine','title':'Oral-health checks','short':'Questions about your mouth, gums or changes you have noticed.','detail':'A consultation is a sensible starting point for questions about your mouth or gums. Tell us about any changes you have noticed when you visit; we can’t diagnose from a website.','booking':'Oral-health consultation','image':'assets/oralcheck.webp','alt':'Illustrative image: a dentist examining a patient’s teeth with a dental mirror','wa':'Hi AJ Dental, I would like to book an appointment to discuss an oral health concern. Please let me know the available slots.','questions':['What should I tell the dentist about my concern?','Are any further checks or referrals appropriate?','When should I come back for a review?']},
 {'id':'fillings','group':'restore','title':'Dental fillings','short':'Discuss options when a tooth needs repair.','detail':'If a tooth needs repair, an assessment helps clarify the available options. Ask us what is suitable, what the treatment would involve and how to care for the tooth afterwards.','booking':'Dental fillings enquiry','image':'assets/filling.webp','alt':'Illustrative image: a tooth-coloured filling being placed and cured','wa':'Hi AJ Dental, I would like to book an appointment about a dental filling. Please let me know the available slots.','questions':['What are the repair options for this tooth?','What would treatment involve?','What follow-up or aftercare would I need?']},
 {'id':'root-canal','group':'restore','title':'Root canal care','short':'Explore the next step when a tooth needs attention on the inside.','detail':'If you have a question about root canal treatment or a tooth that is troubling you, start with an assessment. We can discuss the concern with you and which options may be suitable.','booking':'Root canal consultation','image':'assets/rootcanal.webp','alt':'Illustrative image: root canal treatment using a dental microscope','wa':'Hi AJ Dental, I would like to book an appointment about root canal treatment. Please let me know the available slots.','questions':['Is this treatment appropriate for my tooth?','What would the visits involve?','What should I ask about recovery and follow-up?']},
 {'id':'implants','group':'restore','title':'Dental implants','short':'A conversation about replacing a missing tooth.','detail':'If you are considering a dental implant, ask about an assessment and the options for replacing your missing tooth. We’ll discuss suitability, the treatment plan and our current availability with you at your consultation.','booking':'Dental implant enquiry','image':'assets/implants.webp','alt':'Illustrative image: a dentist explaining a dental implant model to a patient','wa':'Hi AJ Dental, I would like to enquire about dental implants for a missing tooth. Please let me know the available slots for a consultation.','questions':['What options are appropriate in my situation?','Which practitioner would assess and treat me?','What would the treatment and follow-up involve?']},
 {'id':'dentures','group':'restore','title':'Dentures & bridges','short':'Discuss other approaches to replacing missing teeth.','detail':'There may be different ways to replace a missing tooth or several teeth. Use a consultation to ask about the options, their suitability and what to expect over time.','booking':'Dentures or bridges enquiry','image':'assets/dentures.webp','alt':'Illustrative image: ceramic bridge work being prepared on a dental model','wa':'Hi AJ Dental, I would like to book an appointment about dentures or a bridge. Please let me know the available slots.','questions':['Which options could be considered?','What is involved in making and fitting them?','How would I care for them afterwards?']},
 {'id':'extraction','group':'restore','title':'Tooth removal','short':'Ask about assessment, what to expect and aftercare.','detail':'If you have been advised to consider removing a tooth, discuss the assessment, options and aftercare with us. This website is not a substitute for that individual conversation.','booking':'Tooth removal enquiry','image':'assets/extraction.webp','alt':'Illustrative image: a dentist explaining a wisdom tooth on a jaw model before treatment','wa':'Hi AJ Dental, I would like to book an appointment about tooth removal. Please let me know the available slots.','questions':['Is removal the right next step for this tooth?','What should I expect at the appointment?','What aftercare and follow-up should I plan for?']},
 {'id':'orthodontics','group':'smile','title':'Braces & teeth alignment','short':'Bring your questions about alignment or your bite.','detail':'If you are considering orthodontic care, start with a consultation about your teeth alignment and bite. Ask which options may be appropriate and what the process would involve.','booking':'Orthodontic consultation','image':'assets/braces.webp','alt':'Illustrative image: a smiling patient wearing braces','wa':'Hi AJ Dental, I would like to book an orthodontic consultation about braces and teeth alignment. Please let me know the available slots.','questions':['What alignment options could suit me?','How are the treatment and follow-up planned?','What should I understand before deciding?']},
 {'id':'whitening','group':'smile','title':'Teeth whitening','short':'Explore your options for a brighter-looking smile.','detail':'Before choosing whitening, ask about an assessment, suitability and current treatment options. Individual results vary, and we’ll happily go through your questions with you.','booking':'Teeth whitening enquiry','image':'assets/whitening.webp','alt':'Illustrative image: teeth whitening consultation with a shade guide','wa':'Hi AJ Dental, I would like to enquire about teeth whitening. Please let me know the available slots for a consultation.','questions':['Is whitening appropriate for my teeth?','What should I expect from the options available?','How do I look after my teeth afterwards?']},
 {'id':'bonding','group':'smile','title':'Smile design & cosmetic dentistry','short':'Discuss a chipped tooth, a small gap or a change you are considering.','detail':'A smile-design or cosmetic dental consultation can start with what you would like to discuss about your smile. Ask about the options, their limitations and the steps involved before choosing a procedure.','booking':'Cosmetic dental consultation','image':'assets/smiledesign.webp','alt':'Illustrative image: a smile design consultation with a digital preview on a tablet','wa':'Hi AJ Dental, I would like to book a smile design / cosmetic dentistry consultation. Please let me know the available slots.','questions':['Which options could address my concern?','What are the limitations of those options?','What should I know before deciding?']}
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
            f'<div class="care-actions"><a class="btn btn-primary care-book" href="{html.escape(item["wa_url"], quote=True)}" target="_blank" rel="noopener noreferrer">{CHAT} Book Appointment</a>'
            f'<button class="care-more" data-care="{item["id"]}">Details</button>'
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
 'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],'opens':'10:00','closes':'20:00'}],
 'hasMap':site['maps_url'],'sameAs':[site['maps_url'], site.get('instagram_url','https://www.instagram.com/aj_dental_facial_aesthetics/')]
}
public_site = {k: site[k] for k in ['name','phone_e164','phone_display','whatsapp','maps_url','opening_hours','review_policy','publication_ready']}
public_site['reviews'] = [{k: r[k] for k in ['name','quote','full_text','rating','source','source_url','checked_date','is_excerpt','date_label_observed','highlights']} for r in site['reviews']]
public_care = [{k: c[k] for k in ['id','group','title','short','detail','questions','wa_url']} for c in CARE]

replacements = {
 'FONTS':'\n'.join(fonts),'CSS':(ROOT / 'styles.css').read_text(),'JS':(ROOT / 'app.js').read_text(),
 'MARK':data_uri('assets/aj-mark-ivory.webp','image/webp'),'FAVICON':data_uri('assets/aj-favicon.png','image/png'),'DOCTOR':data_uri('assets/doctor-ankitha.webp','image/webp'),
 'OPERATORY':data_uri('assets/clinic-operatory.webp','image/webp'),'RECEPTION':data_uri('assets/clinic-reception.webp','image/webp'),'EXTERIOR':data_uri('assets/clinic-exterior.webp','image/webp'),
 'STARS':stars,'MAP':html.escape(site['maps_url'], quote=True),'DIRECTIONS':html.escape(site['directions_url'], quote=True),
 'WA_GENERAL':html.escape(WA_GENERAL, quote=True),'WA_AESTHETICS':html.escape(WA_AESTHETICS, quote=True),'WA_HAIR':html.escape(WA_HAIR, quote=True),
 'SCHEMA':json.dumps(schema, ensure_ascii=False).replace('</', '<\\/'),
 'SITE_DATA':json.dumps(public_site, ensure_ascii=False).replace('</', '<\\/'),
 'CARE_DATA':json.dumps(public_care, ensure_ascii=False).replace('</', '<\\/'),
 'FONT_LICENSES':'\n'.join(licenses),
 'CARE_ROUTINE':'\n'.join(card(x, i + 1) for i, x in enumerate([c for c in CARE if c['group'] == 'routine'])),
 'CARE_RESTORE':'\n'.join(card(x, i + 1) for i, x in enumerate([c for c in CARE if c['group'] == 'restore'])),
 'CARE_SMILE':'\n'.join(card(x, i + 1) for i, x in enumerate([c for c in CARE if c['group'] == 'smile'])),
 'REVIEW_CARDS':'\n'.join(review_card(r, n) for n, r in enumerate(site['reviews']))
}
s = (ROOT / 'template.html').read_text()
for key, value in replacements.items():
    s = s.replace('@@' + key + '@@', value)
assert not re.search(r'@@[A-Z_]+@@', s), 'Unreplaced template token'
for disallowed in ['9008553086','9010000021','7383581638','25,000','25000','localhost','127.0.0.1']:
    assert disallowed not in s, disallowed
assert '<meta name="robots" content="noindex,nofollow">' in s
assert 'aggregateRating' not in json.dumps(schema)
assert len(site['reviews']) == 10 and all(r['source'] == 'Google' for r in site['reviews'])
assert len({r['name'] for r in site['reviews']}) == 10, 'Reviewer names must be unique'
assert '<form' not in s and 'appointmentDialog' not in s and 'data-book' not in s, 'No forms or form-style booking may remain'
assert 'Request a visit' not in s and 'Request your visit' not in s
assert 'Book Appointment' in s and s.count('wa.me/917997911390?text=') >= 18, 'Direct WhatsApp deep links expected throughout'
assert 'instagram.com/aj_dental_facial_aesthetics' in s
assert all((ROOT / c['image']).exists() for c in CARE), 'Every service needs an image'
(ROOT / 'AJ_Dental_Preview.html').write_text(s)
(ROOT / 'index.html').write_text(s)
print('Generated self-contained HTML:', len(s.encode()), 'bytes; Google reviews:', len(site['reviews']), 'of', site['review_policy']['target_count'])
print('Services with illustrative images:', len(CARE), '; WhatsApp deep links:', s.count('wa.me/917997911390?text='), '; tel links:', s.count('tel:+917997911390'))
print('Fonts embedded: Instrument Serif, Manrope, Noto Sans Telugu subset; external runtime assets: 0')
