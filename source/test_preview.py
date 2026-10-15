import asyncio, json
from pathlib import Path
from urllib.parse import unquote
from playwright.async_api import async_playwright, expect

ROOT = Path('/home/user/aj-dental-website')
URL = 'http://127.0.0.1:3000/'

async def main():
    results = {'url': 'Local preview server', 'desktop': {}, 'mobile': {}, 'checks': [], 'errors': []}
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
        ctx = await browser.new_context(viewport={'width': 1440, 'height': 950}, locale='en-IN', timezone_id='Asia/Kolkata')
        p = await ctx.new_page(); errors = []; requests = []
        p.on('pageerror', lambda e: errors.append(str(e)))
        p.on('request', lambda req: requests.append(req.url))
        await p.goto(URL, wait_until='load')
        await p.evaluate('document.fonts.ready')
        await p.wait_for_function('document.querySelector(".hero-photo").complete')
        await p.evaluate('''async()=>{await Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(async i=>{i.loading='eager';try{await i.decode();}catch(_){}}));}''')
        await p.screenshot(path=str(ROOT/'evidence'/'preview-desktop.jpg'), type='jpeg', quality=88)
        metrics = await p.evaluate('''() => ({title:document.title,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
          fontsLoaded:document.fonts.check('16px Manrope')&&document.fonts.check('16px "Instrument Serif"')&&document.fonts.check('16px "Noto Sans Telugu"'),
          teluguLoaded:document.fonts.check('600 20px "Noto Sans Telugu"'),
          imageErrors:[...document.images].filter(i=>i.getAttribute('src')&&(!i.complete||i.naturalWidth===0)).map(i=>i.alt),
          reviews:document.querySelectorAll('.review-card').length,
          reviewNames:[...document.querySelectorAll('.review-author')].map(e=>e.textContent.trim()),
          forms:document.querySelectorAll('form').length,
          bookLinks:[...document.querySelectorAll('a[href^="https://wa.me/917997911390?text="]')].length,
          telLinks:document.querySelectorAll('a[href="tel:+917997911390"]').length,
          bodyFont:parseFloat(getComputedStyle(document.body).fontSize),
          careCards:document.querySelectorAll('.care-item').length,
          careImages:[...document.querySelectorAll('.care-media img')].filter(i=>i.naturalWidth>0).length})''')
        assert metrics['scrollWidth'] <= metrics['width'], metrics
        assert not metrics['imageErrors'], metrics['imageErrors']
        assert metrics['fontsLoaded'], metrics
        assert metrics['reviews'] == 10, metrics
        assert len(set(metrics['reviewNames'])) == 10, metrics['reviewNames']
        assert metrics['forms'] == 0, 'No form may exist in Preview 02'
        assert metrics['bookLinks'] >= 18, metrics
        assert metrics['telLinks'] >= 8, metrics
        assert metrics['bodyFont'] >= 17, metrics
        assert metrics['careCards'] == 10 and metrics['careImages'] == 10, metrics
        results['desktop'] = metrics
        text = await p.locator('body').inner_text()
        for disallowed in ['9008553086', '9010000021', '7383581638', '₹25,000', 'Permanently closed', 'Request a visit', 'Request your visit']:
            assert disallowed not in text, disallowed
        for required in ['Sunday by appointment', '533001', 'Book Appointment', 'కాకినాడకు స్వాగతం', 'aj_dental_facial_aesthetics', 'Deepika Cheemala', 'Tarun Gundrathi', 'Kommanapalli Ashmi']:
            assert required not in text if required == 'Kommanapalli Ashmi' else required in text, required
        results['checks'].append('Single canonical phone, confirmed address/hours, no implant price, no form, 10 unique named Google reviews, Telugu + Instagram present.')

        # Per-service WhatsApp deep link carries the right context (read href only; never navigate).
        card = p.locator('.care-item', has_text='Dental implants').first
        href = await card.locator('.care-book').get_attribute('href')
        assert 'dental implants' in unquote(href).lower(), href
        assert await card.locator('.care-call').get_attribute('href') == 'tel:+917997911390'
        await card.locator('.care-media').click()
        assert await p.locator('#detailDialog').is_visible()
        assert 'Dental implants' in await p.locator('#detailTitle').inner_text()
        dhref = await p.locator('#detailDialog .btn-primary').get_attribute('href')
        assert 'dental implants' in unquote(dhref).lower(), dhref
        await p.keyboard.press('Escape')
        results['checks'].append('Service cards: image, per-service WhatsApp message, call link and details dialog all wired.')

        # Journey tabs.
        await p.locator('[data-journey="2"]').scroll_into_view_if_needed()
        await p.locator('[data-journey="2"]').click()
        assert 'step 3 of 4' in (await p.locator('#journeyCount').inner_text()).lower()
        assert 'decide in your own time' in await p.locator('#journeyText').inner_text()
        results['checks'].append('Interactive first-visit journey tabs update content accessibly.')

        # Nav Book Appointment is a direct WhatsApp anchor.
        navhref = await p.locator('.nav-action').get_attribute('href')
        assert navhref.startswith('https://wa.me/917997911390?text='), navhref
        assert 'book an appointment' in unquote(navhref).lower()

        # Gallery keyboard navigation.
        await p.locator('[data-photo="0"]').scroll_into_view_if_needed()
        await p.locator('[data-photo="0"]').click()
        assert await p.locator('#lightboxDialog').is_visible()
        caption0 = await p.locator('#lightboxCaption').inner_text()
        await p.keyboard.press('ArrowRight')
        assert caption0 != await p.locator('#lightboxCaption').inner_text()
        await p.keyboard.press('Escape')
        results['checks'].append('Photo viewer, next/previous and Escape close.')

        # FAQ single-open behaviour.
        await p.locator('.faq-item summary').first.scroll_into_view_if_needed()
        await p.locator('.faq-item summary').first.click()
        assert await p.locator('.faq-item').first.get_attribute('open') is not None

        # Reviews: arrows advance, card tap opens the full text, "read all" lists 10.
        await p.locator('#reviewNext').scroll_into_view_if_needed()
        await p.locator('#reviewNext').click()
        await expect(p.locator('#reviewCount')).to_have_text('2 / 10')
        await p.locator('#reviewPrev').click()
        await expect(p.locator('#reviewCount')).to_have_text('1 / 10')
        await p.locator('.review-card[data-review="1"]').click()
        assert await p.locator('#detailDialog').is_visible()
        body = await p.locator('#detailContent').inner_text()
        assert 'Tarun Gundrathi' in body and 'attention to detail' in body, body[:300]
        await p.keyboard.press('Escape')
        await p.locator('#allReviewsBtn').click()
        assert await p.locator('.all-review').count() == 10
        await p.keyboard.press('Escape')
        results['checks'].append('Drag/scroll review carousel, full-review dialog and 10-review index.')

        # Doctor dialog books with that doctor on WhatsApp.
        await p.locator('[data-doctor="ankitha"]').scroll_into_view_if_needed()
        await p.locator('[data-doctor="ankitha"]').click()
        dhref = await p.locator('#detailDialog .btn-primary').get_attribute('href')
        assert 'Dr. M. Ankitha' in unquote(dhref), dhref
        await p.keyboard.press('Escape')

        # Motion toggle off exposes everything.
        await p.locator('#motionToggle').click()
        assert 'motion-off' in await p.locator('html').get_attribute('class')
        await p.evaluate('document.querySelectorAll(".reveal").forEach(x=>x.classList.add("is-visible"));window.scrollTo(0,0)')
        await p.screenshot(path=str(ROOT/'evidence'/'preview-desktop-full.jpg'), type='jpeg', quality=78, full_page=True)

        axe = ROOT/'evidence'/'axe.min.js'
        if axe.exists():
            await p.add_script_tag(content=axe.read_text())
            audit = await p.evaluate('''async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});return {violations:r.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))})),passes:r.passes.length,incomplete:r.incomplete.length};}''')
            results['accessibility_audit'] = audit
            print('AXE', json.dumps(audit, indent=2))
        results['external_runtime_requests'] = [u for u in requests if not u.startswith('http://127.0.0.1:3000') and not u.startswith('data:')]
        assert not results['external_runtime_requests'], results['external_runtime_requests']

        # Mobile.
        mobile = await ctx.new_page()
        await mobile.set_viewport_size({'width': 390, 'height': 844})
        mobile.on('pageerror', lambda e: errors.append('Mobile: ' + str(e)))
        await mobile.goto(URL, wait_until='load'); await mobile.evaluate('document.fonts.ready')
        await mobile.evaluate('''async()=>{await Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(async i=>{i.loading='eager';try{await i.decode();}catch(_){}}));}''')
        await mobile.screenshot(path=str(ROOT/'evidence'/'preview-mobile.jpg'), type='jpeg', quality=88)
        await mobile.locator('#menuToggle').click()
        assert await mobile.locator('#mobileNav').is_visible()
        await mobile.locator('#mobileNav a[href="#doctors"]').click()
        assert not await mobile.locator('#mobileNav').is_visible()
        mmetrics = await mobile.evaluate('''()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
          dockDisplay:getComputedStyle(document.querySelector('.mobile-dock')).display,
          dockBook:document.querySelector('.mobile-dock .btn').textContent.trim(),
          bodyFont:parseFloat(getComputedStyle(document.body).fontSize),
          heroDesc:parseFloat(getComputedStyle(document.querySelector('.hero-description')).fontSize),
          floatHidden:getComputedStyle(document.querySelector('.float-book')).display==='none'||parseFloat(getComputedStyle(document.querySelector('.float-book')).opacity)===0,
          images:[...document.images].filter(i=>i.getAttribute('src')&&(!i.complete||i.naturalWidth===0)).map(i=>i.alt)})''')
        assert mmetrics['scrollWidth'] <= mmetrics['width'], mmetrics
        assert mmetrics['dockDisplay'] == 'flex' and 'Book Appointment' in mmetrics['dockBook'], mmetrics
        assert mmetrics['bodyFont'] >= 16 and mmetrics['heroDesc'] >= 16, mmetrics
        assert not mmetrics['images'], mmetrics
        results['mobile'] = mmetrics
        # Review arrows on mobile.
        await mobile.locator('#reviewNext').scroll_into_view_if_needed()
        await mobile.locator('#reviewNext').click()
        await expect(mobile.locator('#reviewCount')).to_have_text('2 / 10')
        await mobile.locator('#motionToggle').click()
        await mobile.evaluate('document.querySelectorAll(".reveal").forEach(x=>x.classList.add("is-visible"));window.scrollTo(0,0)')
        await mobile.screenshot(path=str(ROOT/'evidence'/'preview-mobile-full.jpg'), type='jpeg', quality=78, full_page=True)
        results['checks'].append('390px mobile layout, sticky Call/Book dock, menu, review navigation, >=16px reading text.')

        for width in [320, 360, 768, 1024, 720]:
            await mobile.set_viewport_size({'width': width, 'height': 900})
            overflow = await mobile.evaluate('document.documentElement.scrollWidth>innerWidth')
            assert not overflow, ('overflow', width)
        results['checks'].append('No horizontal overflow at 320, 360, 390, 720 (200% zoom proxy), 768, 1024 and 1440px.')

        zoomctx = await browser.new_context(viewport={'width': 720, 'height': 500}, device_scale_factor=2, locale='en-IN')
        zp = await zoomctx.new_page(); await zp.goto(URL, wait_until='load')
        assert await zp.evaluate('document.documentElement.scrollWidth<=innerWidth')
        results['checks'].append('200% zoom (720 CSS px @2x) reflows without horizontal loss.')

        reducedctx = await browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
        reduced = await reducedctx.new_page(); await reduced.goto(URL, wait_until='load')
        cls = await reduced.locator('html').get_attribute('class'); assert 'motion-off' in cls
        styles = await reduced.evaluate('''()=>({ribbon:getComputedStyle(document.querySelector('.te-ribbon-track')).animationName,hiddenReveals:[...document.querySelectorAll('.reveal')].filter(e=>getComputedStyle(e).opacity==='0').length})''')
        assert styles['ribbon'] == 'none' and styles['hiddenReveals'] == 0, styles
        results['checks'].append('OS reduced-motion honoured; ribbon paused, no hidden content.')
        results['errors'] = errors
        assert not errors, errors
        results['status'] = 'Functional tests passed; inspect accessibility audit separately.'
        (ROOT/'evidence'/'preview-qa.json').write_text(json.dumps(results, indent=2))
        print(json.dumps({k: v for k, v in results.items() if k != 'accessibility_audit'}, indent=2))
        await browser.close()

asyncio.run(main())
