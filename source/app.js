(() => {
'use strict';
const site = JSON.parse(document.getElementById('siteData').textContent);
const care = JSON.parse(document.getElementById('careData').textContent);
const $ = (id) => document.getElementById(id);
const esc = (value) => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const arrow = '<svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg>';
const chat = '<svg class="icon" aria-hidden="true"><use href="#i-chat"/></svg>';
const starRow = '<svg class="star" aria-hidden="true"><use href="#i-star"/></svg>'.repeat(5);
const waLink = (message) => site.whatsapp + '?text=' + encodeURIComponent(message);
function hlText(text, phrases) {
 let out = esc(text);
 [...(phrases || [])].sort((a, b) => b.length - a.length).forEach(phrase => {
  const ep = esc(phrase);
  if(out.includes(ep)) out = out.replace(ep, '<strong>' + ep + '</strong>');
 });
 return out;
}
const dialogs = [...document.querySelectorAll('dialog')];
let lastTrigger = null;
let toastTimer;
function toast(message) { const el = $('toast'); el.textContent = message; el.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 3500); }
function closeDialog(d) { if(d && d.open) d.close(); document.body.classList.toggle('dialog-open', dialogs.some(x => x.open)); }
function openDialog(d, trigger) {
 lastTrigger = trigger || document.activeElement;
 dialogs.forEach(x => { if(x.open && x !== d) x.close(); });
 if(!d.open) d.showModal();
 document.body.classList.add('dialog-open');
}
dialogs.forEach(d => {
 d.addEventListener('close', () => { document.body.classList.toggle('dialog-open', dialogs.some(x => x.open)); if(lastTrigger && document.contains(lastTrigger)) lastTrigger.focus({preventScroll:true}); });
 d.addEventListener('click', e => {
  if(e.target !== d) return;
  const r = d.getBoundingClientRect();
  if(e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) closeDialog(d);
 });
 d.querySelectorAll('[data-close]').forEach(b => b.addEventListener('click', () => closeDialog(d)));
});
/* Navigation */
const menuToggle = $('menuToggle');
function toggleMenu(open) { menuToggle.setAttribute('aria-expanded', String(open)); menuToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation'); $('mobileNav').hidden = !open; }
menuToggle.addEventListener('click', () => toggleMenu(menuToggle.getAttribute('aria-expanded') !== 'true'));
$('mobileNav').querySelectorAll('a,button').forEach(a => a.addEventListener('click', () => toggleMenu(false)));
document.addEventListener('keydown', e => { if(e.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') { toggleMenu(false); menuToggle.focus(); } });
/* Motion: optional, one-off/decorative or user-controlled; reviews never auto-advance. */
const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
let motionAllowed = !motionQuery.matches;
function setMotion(on, explicit = false) {
 motionAllowed = on;
 document.documentElement.classList.toggle('motion-on', on);
 document.documentElement.classList.toggle('motion-off', !on);
 document.documentElement.classList.toggle('motion-explicit-on', !!(on && explicit));
 $('motionToggle').setAttribute('aria-pressed', String(!on));
 $('motionToggle').querySelector('span').textContent = on ? 'Motion on' : 'Motion off';
 if(!on) document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
}
setMotion(motionAllowed);
$('motionToggle').addEventListener('click', () => { setMotion(!motionAllowed, true); toast(motionAllowed ? 'Subtle motion is on.' : 'Motion is off. All content remains available.'); });
if(motionQuery.addEventListener) motionQuery.addEventListener('change', e => setMotion(!e.matches));
if('IntersectionObserver' in window && motionAllowed) {
 const io = new IntersectionObserver(entries => entries.forEach(e => { if(e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); } }), {threshold:.08, rootMargin:'0px 0px -15px 0px'});
 document.querySelectorAll('.reveal').forEach(el => io.observe(el));
} else document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-visible'));
if('IntersectionObserver' in window) {
 const links = [...document.querySelectorAll('.desktop-nav a')];
 const sections = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
 const io = new IntersectionObserver(entries => entries.forEach(e => { if(e.isIntersecting) links.forEach(a => a.classList.toggle('is-current', a.getAttribute('href') === '#' + e.target.id)); }), {rootMargin:'-20% 0px -50% 0px', threshold:0});
 sections.forEach(s => io.observe(s));
}
/* Scroll progress and a whisper of hero parallax. */
const progressBar = $('scrollProgress'); const heroStage = $('heroStage');
let ticking = false;
function onScroll() {
 if(ticking) return; ticking = true;
 requestAnimationFrame(() => {
  const max = document.documentElement.scrollHeight - innerHeight;
  const y = window.scrollY || 0;
  progressBar.style.transform = `scaleX(${max > 0 ? Math.min(1, y / max) : 0})`;
  if(motionAllowed && heroStage && y < innerHeight) heroStage.style.transform = `translateY(${Math.min(14, y * 0.04)}px)`;
  ticking = false;
 });
}
addEventListener('scroll', onScroll, {passive:true}); onScroll();
/* Hero doctor stage: one full portrait at a time, crossfading between our two doctors. */
const heroBtns = [...document.querySelectorAll('[data-hero-doc]')];
const heroImgs = [...document.querySelectorAll('[data-hero-photo]')];
let heroTimer = null, heroAuto = true;
function showHeroDoc(id) {
 heroImgs.forEach(img => { const on = img.dataset.heroPhoto === id; img.classList.toggle('is-active', on); if(on) img.removeAttribute('aria-hidden'); else img.setAttribute('aria-hidden','true'); });
 heroBtns.forEach(b => { const on = b.dataset.heroDoc === id; b.classList.toggle('is-active', on); b.setAttribute('aria-pressed', String(on)); });
}
function heroOrder() { return heroBtns.map(b => b.dataset.heroDoc); }
function heroAdvance() { if(!motionAllowed) return; const order = heroOrder(); const cur = (heroBtns.find(b => b.classList.contains('is-active')) || {}).dataset?.heroDoc; showHeroDoc(order[(order.indexOf(cur) + 1) % order.length]); }
function heroPlay() { if(!motionAllowed || !heroAuto || heroImgs.length < 2) return; clearInterval(heroTimer); heroTimer = setInterval(heroAdvance, 6000); }
function heroPause() { clearInterval(heroTimer); }
heroBtns.forEach(b => b.addEventListener('click', () => { heroAuto = false; heroPause(); showHeroDoc(b.dataset.heroDoc); }));
if(heroStage) { heroStage.addEventListener('pointerenter', heroPause); heroStage.addEventListener('pointerleave', heroPlay); heroStage.addEventListener('focusin', heroPause); heroStage.addEventListener('focusout', heroPlay); }
heroPlay();
/* Detail dialogs: every booking action is a direct WhatsApp deep link — no forms anywhere. */
function showCare(id, trigger) {
 const item = care.find(x => x.id === id); if(!item) return;
 const media = document.querySelector(`[data-care-img="${id}"]`);
 const img = media ? `<img class="detail-hero" src="${media.src}" alt="">` : '';
 $('detailContent').innerHTML = `${img}<p class="dialog-kicker">A topic for your dental consultation</p><h2 class="dialog-title" id="detailTitle">${esc(item.title)}</h2><p class="dialog-description">${esc(item.detail)}</p><div class="detail-block"><h3>Questions you can bring</h3><ul>${item.questions.map(q => '<li>' + esc(q) + '</li>').join('')}</ul><p>We’ll confirm what’s suitable for you after an assessment.</p><div class="dialog-actions"><a class="btn btn-primary" href="${esc(item.wa_url)}" target="_blank" rel="noopener noreferrer">${chat} Book Appointment</a><a class="text-link" href="tel:+917997911390">Call us instead</a></div></div>`;
 openDialog($('detailDialog'), trigger);
}
function showDoctor(id, trigger) {
 const joe = id === 'joe';
 const name = joe ? 'Dr. B. Joe Praveen' : 'Dr. M. Ankitha';
 const role = joe ? 'MDS · Orthodontist · Assistant Professor' : 'MDS · Oral Physician & Radiologist · Asst. Professor';
 const reg = joe ? 'Reg No: A16267' : 'Reg No: A23045';
 const text = joe ? 'Dr. B. Joe Praveen is our orthodontist and an Assistant Professor. He specialises in the diagnosis, prevention and correction of misaligned teeth and jaws, looking after patients who need braces, clear aligners, bite correction, teeth alignment and smile enhancement — helping them achieve a healthier, well-aligned and confident smile through personalised orthodontic care.' : 'Dr. M. Ankitha is a dental healthcare provider — MDS, Oral Physician & Radiologist, and an Assistant Professor. She authored the book “Cone Beam Computed Tomography: Oral and Maxillofacial Diagnosis & Applications”, which focuses on advanced dental radiography. She has also contributed to several international clinical research papers, exploring areas such as transcutaneous electrical nerve stimulation (TENS) on salivary flow in diabetic patients, maxillary odontomas, and forensic cheiloscopy.';
 const msg = joe ? 'Hi AJ Dental, I would like to book an orthodontic consultation with Dr. B. Joe Praveen. Please let me know the available slots.' : 'Hi AJ Dental, I would like to book an appointment with Dr. M. Ankitha. Please let me know the available slots.';
 const media = document.querySelector(`[data-doctor-img="${id}"]`);
 const img = media ? `<img class="detail-hero doctor-hero-img" src="${media.src}" alt="">` : '';
 $('detailContent').innerHTML = `${img}<p class="dialog-kicker">Meet your dentist</p><h2 class="dialog-title" id="detailTitle">${esc(name)}</h2><p class="doctor-role">${esc(role)}</p><p class="doctor-reg">${esc(reg)}</p><p class="dialog-description">${esc(text)}</p><div class="detail-block"><h3>Plan your visit</h3><p>Message or call us to ask about availability. We’re open Monday–Saturday, 9 AM–8 PM, and Sundays by appointment.</p><div class="dialog-actions"><a class="btn btn-primary" href="${esc(waLink(msg))}" target="_blank" rel="noopener noreferrer">${chat} Book Appointment</a><a class="text-link" href="tel:+917997911390">Call us instead</a></div></div>`;
 openDialog($('detailDialog'), trigger);
}
/* Photo viewer uses only the actual business-gallery photos embedded in the file. */
const photos = [
 {src:document.querySelector('[data-photo="0"] img').src,caption:'Our reception',alt:'The reception at AJ Dental & Facial Aesthetics in Ayodhya Nagar, Kakinada, with seating on both sides and our clinic sign'},
 {src:document.querySelector('[data-photo="1"] img').src,caption:'The treatment room',alt:'The dental treatment room at AJ Dental & Facial Aesthetics in Ayodhya Nagar, Kakinada, with the dental chair, stool and operatory light'},
 {src:document.querySelector('[data-photo="2"] img').src,caption:'Aesthetics treatment room',alt:'The aesthetics treatment room at AJ Dental & Facial Aesthetics in Ayodhya Nagar, Kakinada, with the treatment table, ring light and aesthetics equipment'},
 {src:document.querySelector('[data-photo="3"] img').src,caption:'The AJ storefront · Road No. 3',alt:'AJ Dental signage and clinic entrance in Ayodhya Nagar'}
];
let photoIndex = 0;
function renderPhoto() {
 const photo = photos[photoIndex]; $('lightboxImage').src = photo.src; $('lightboxImage').alt = photo.alt;
 $('lightboxCaption').textContent = photo.caption;
 const small = document.createElement('small'); small.textContent = (photoIndex + 1) + ' / ' + photos.length + ' · Business-gallery photograph'; $('lightboxCaption').appendChild(small);
}
function showPhoto(index, trigger) { photoIndex = index; renderPhoto(); openDialog($('lightboxDialog'), trigger); }
$('photoPrev').addEventListener('click', () => { photoIndex = (photoIndex - 1 + photos.length) % photos.length; renderPhoto(); });
$('photoNext').addEventListener('click', () => { photoIndex = (photoIndex + 1) % photos.length; renderPhoto(); });
$('lightboxDialog').addEventListener('keydown', e => { if(e.key === 'ArrowLeft') { e.preventDefault(); $('photoPrev').click(); } if(e.key === 'ArrowRight') { e.preventDefault(); $('photoNext').click(); } });
/* Reviews: a drag/scroll-snap carousel. Tap a card to read the full Google review. */
const viewport = $('reviewViewport'); const track = $('reviewTrack');
const reviewCards = [...track.querySelectorAll('.review-card')];
function cardStep() { if(!reviewCards.length) return 320; const gap = parseFloat(getComputedStyle(track).gap) || 0; return reviewCards[0].getBoundingClientRect().width + gap; }
function updateReviewUI() {
 if(!reviewCards.length) return;
 const step = cardStep(); const maxScroll = viewport.scrollWidth - viewport.clientWidth;
 const idx = Math.min(reviewCards.length - 1, Math.max(0, Math.round(viewport.scrollLeft / step)));
 $('reviewCount').textContent = (idx + 1) + ' / ' + reviewCards.length;
 $('reviewProgress').style.width = (maxScroll > 0 ? ((viewport.scrollLeft / maxScroll) * 90 + 10) : 100) + '%';
 $('reviewPrev').disabled = viewport.scrollLeft <= 4;
 $('reviewNext').disabled = viewport.scrollLeft >= maxScroll - 4;
}
let reviewTick = false;
viewport.addEventListener('scroll', () => { if(reviewTick) return; reviewTick = true; requestAnimationFrame(() => { updateReviewUI(); reviewTick = false; }); }, {passive:true});
$('reviewPrev').addEventListener('click', () => viewport.scrollBy({left:-cardStep(), behavior: motionAllowed ? 'smooth' : 'auto'}));
$('reviewNext').addEventListener('click', () => viewport.scrollBy({left:cardStep(), behavior: motionAllowed ? 'smooth' : 'auto'}));
let dragStartX = 0, dragStartScroll = 0, dragging = false, dragged = false;
viewport.addEventListener('pointerdown', e => { if(e.pointerType === 'touch') return; dragging = true; dragged = false; dragStartX = e.clientX; dragStartScroll = viewport.scrollLeft; viewport.classList.add('dragging'); });
viewport.addEventListener('pointermove', e => { if(!dragging) return; const dx = e.clientX - dragStartX; if(Math.abs(dx) > 6) dragged = true; viewport.scrollLeft = dragStartScroll - dx; });
['pointerup','pointercancel'].forEach(ev => window.addEventListener(ev, () => { if(!dragging) return; dragging = false; viewport.classList.remove('dragging'); setTimeout(() => { dragged = false; }, 80); }));
function showReview(i, trigger) {
 const r = site.reviews[i]; if(!r) return;
 const full = (r.full_text || r.quote).split('\n\n').map(p => `<p>${hlText(p, r.highlights)}</p>`).join('');
 $('detailContent').innerHTML = `<p class="dialog-kicker">Google review · ${esc(r.date_label_observed || '')}</p><h2 class="dialog-title" id="detailTitle">${esc(r.name)}</h2><div class="stars" role="img" aria-label="Rated 5 out of 5 stars">${starRow}</div><div class="full-review">${full}</div><div class="detail-block"><div class="dialog-actions"><a class="btn btn-primary" href="${esc(site.maps_url)}" target="_blank" rel="noopener noreferrer">View on Google ${arrow}</a><a class="text-link" href="${esc(waLink('Hi AJ Dental, I would like to book an appointment. Please let me know the available slots.'))}" target="_blank" rel="noopener noreferrer">Book Appointment</a></div></div>`;
 openDialog($('detailDialog'), trigger);
}
$('allReviewsBtn').addEventListener('click', e => {
 $('detailContent').innerHTML = `<p class="dialog-kicker">From our current Google profile</p><h2 class="dialog-title" id="detailTitle">In our patients’ own words.</h2><p class="dialog-description">Ten named reviews from our Google profile. Tap “View on Google” to read them in context.</p><div class="all-reviews-list">${site.reviews.map(r => `<article class="all-review"><div class="stars" role="img" aria-label="Rated 5 out of 5 stars">${starRow}</div><blockquote>“${hlText(r.full_text || r.quote, r.highlights)}”</blockquote><strong>${esc(r.name)}</strong><a href="${esc(site.maps_url)}" target="_blank" rel="noopener noreferrer">Google review · ${esc(r.date_label_observed || '')} · View on Google ↗</a></article>`).join('')}</div>`;
 openDialog($('detailDialog'), e.currentTarget);
});
updateReviewUI();
/* Delegated clicks for dynamically meaningful controls. */
document.addEventListener('click', e => {
 const item = e.target.closest('[data-care]'); if(item) return showCare(item.dataset.care, item);
 const doc = e.target.closest('[data-doctor]'); if(doc) return showDoctor(doc.dataset.doctor, doc);
 const photo = e.target.closest('[data-photo]'); if(photo) return showPhoto(Number(photo.dataset.photo), photo);
 const rev = e.target.closest('[data-review]');
 if(rev && !dragged && !e.target.closest('a')) return showReview(Number(rev.dataset.review), rev);
});
let resizeFrame;
addEventListener('resize', () => { cancelAnimationFrame(resizeFrame); resizeFrame = requestAnimationFrame(() => { updateReviewUI(); if(innerWidth > 780) toggleMenu(false); }); });
/* FAQ disclosure retains native keyboard support; only one open at a time. */
document.querySelectorAll('.faq-item').forEach(d => d.addEventListener('toggle', () => { if(d.open) document.querySelectorAll('.faq-item').forEach(other => { if(other !== d) other.open = false; }); }));
$('year').textContent = new Intl.DateTimeFormat('en',{year:'numeric',timeZone:'Asia/Kolkata'}).format(new Date());
})();
/* Analytics: count the taps that matter. gtag exists only on the live host, so test/QA traffic is never recorded. */
document.addEventListener('click', e => {
 if(!window.gtag || !e.target.closest) return;
 const a = e.target.closest('a[href]'); if(!a) return;
 const href = a.href;
 const label = (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60);
 if(href.includes('wa.me/')) gtag('event', 'whatsapp_click', {link_text: label, page_path: location.pathname});
 else if(href.startsWith('tel:')) gtag('event', 'call_click', {link_text: label, page_path: location.pathname});
 else if(href.includes('google.com/maps/dir')) gtag('event', 'directions_click', {link_text: label, page_path: location.pathname});
 else if(/instagram\.com|facebook\.com|youtube\.com/.test(href)) gtag('event', 'social_click', {link_url: href});
}, {passive:true});
