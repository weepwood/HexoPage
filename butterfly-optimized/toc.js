/* HALO: cancellable article navigation, stable tree and independent scrollspy. */
(function () {
  'use strict'
  window.haloInitToc = function () {
    const card = document.getElementById('card-toc')
    const content = card?.querySelector('.toc-content')
    const article = document.getElementById('article-container')
    if (!content || !article || card.dataset.haloToc) return
    const resolve = hash => {
      if (!hash || hash[0] !== '#') return null
      try { return document.getElementById(decodeURIComponent(hash.slice(1))) } catch (_) { return null }
    }
    const entries = [...content.querySelectorAll('.toc-link')].map(link => ({
      link, heading: resolve(link.getAttribute('href')), item: link.closest('li')
    })).filter(e => e.heading && article.contains(e.heading))
    if (!entries.length) return
    card.dataset.haloToc = 'true'
    const reduced = matchMedia('(prefers-reduced-motion: reduce)')
    const mobile = matchMedia('(max-width: 900px)')
    const toggle = document.getElementById('mobile-toc-button')
    const progress = document.createElement('span')
    progress.className = 'halo-toc-progress'
    progress.setAttribute('aria-hidden', 'true')
    card.querySelector('.item-headline')?.append(progress)
    const bar = document.createElement('div')
    bar.className = 'halo-toc-track'
    bar.innerHTML = '<span></span>'
    bar.setAttribute('aria-hidden', 'true')
    content.before(bar)
    const fill = bar.firstElementChild
    content.setAttribute('role', 'navigation')
    content.setAttribute('aria-label', '文章目录')
    content.id ||= 'halo-toc-content'
    toggle?.setAttribute('aria-controls', card.id)
    toggle?.setAttribute('aria-expanded', 'false')
    const groups = [...content.querySelectorAll('li.toc-item')].filter(li => li.querySelector(':scope > .toc-child'))
    for (const li of groups) {
      const branch = li.querySelector(':scope > .toc-child')
      const button = document.createElement('button')
      button.type = 'button'
      button.className = 'halo-toc-branch'
      button.setAttribute('aria-label', '展开或折叠子目录')
      button.setAttribute('aria-expanded', 'false')
      button.innerHTML = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="m4 2.5 3.5 3.5L4 9.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
      li.insertBefore(button, branch)
    }
    const ancestors = e => {
      const result = new Set()
      for (let li = e?.item; li && content.contains(li); li = li.parentElement.closest('li.toc-item')) result.add(li)
      return result
    }
    const manual = new Map()
    let active = null, animation = null, frame = 0, positions = [], dirty = true, sidebarUntil = 0
    const maxScroll = () => Math.max(0, document.documentElement.scrollHeight - innerHeight)
    const offset = () => Math.max(72, (document.getElementById('nav')?.offsetHeight || 60) + 18)
    const clamp = (n, min, max) => Math.min(max, Math.max(min, n))
    function tree() {
      const path = ancestors(active)
      for (const li of groups) {
        const open = manual.has(li) ? manual.get(li) : path.has(li)
        li.classList.toggle('halo-expanded', open)
        li.querySelector(':scope > .halo-toc-branch').setAttribute('aria-expanded', String(open))
      }
    }
    function reveal(entry, force) {
      if (!entry || (!force && performance.now() < sidebarUntil)) return
      if (!content.clientHeight || !entry.link.getClientRects().length) return
      const r = entry.link.getBoundingClientRect(), box = content.getBoundingClientRect()
      const padding = 18
      if (r.top < box.top + padding || r.bottom > box.bottom - padding) {
        const target = clamp(content.scrollTop + r.top - box.top - content.clientHeight * .34, 0, content.scrollHeight - content.clientHeight)
        content.scrollTo({ top: target, behavior: reduced.matches ? 'instant' : 'smooth' })
      }
    }
    function select(entry, force = false) {
      if (active === entry && !force) return
      if (active) { active.link.classList.remove('active'); active.link.removeAttribute('aria-current') }
      active = entry
      for (const li of ancestors(active)) manual.delete(li)
      if (active) { active.link.classList.add('active'); active.link.setAttribute('aria-current', 'location') }
      tree()
      reveal(active, force)
    }
    function measure() {
      positions = entries.filter(e => e.heading.getClientRects().length).map(e => ({
        e, top: e.heading.getBoundingClientRect().top + scrollY
      })).sort((a,b) => a.top-b.top)
      dirty = false
    }
    function tick() {
      frame = 0
      if (dirty) measure()
      const start = article.getBoundingClientRect().top + scrollY
      const end = start + article.offsetHeight
      const pct = Math.round(clamp((scrollY + offset() - start) / Math.max(1, end - start - innerHeight + offset()), 0, 1) * 100)
      progress.textContent = pct + '%'
      fill.style.transform = 'scaleX(' + pct / 100 + ')'
      if (animation || !positions.length) return
      let low = 0, high = positions.length - 1, i = -1
      const line = scrollY + offset() + 12
      while (low <= high) {
        const mid = (low + high) >> 1
        if (positions[mid].top <= line) { i = mid; low = mid + 1 } else high = mid - 1
      }
      if (scrollY >= maxScroll() - 2 && maxScroll() > 0) i = positions.length - 1
      select(i < 0 ? null : positions[i].e)
    }
    function schedule() { if (!frame) frame = requestAnimationFrame(tick) }
    function invalidate() { dirty = true; schedule() }
    function cancel() {
      if (!animation) return
      cancelAnimationFrame(animation.raf)
      animation = null
      schedule()
    }
    function jump(entry, updateHash = true, instant = false) {
      cancel()
      select(entry, true)
      if (updateHash && location.hash !== entry.link.hash) history.pushState(null, '', entry.link.hash)
      const start = scrollY
      const destination = () => clamp(entry.heading.getBoundingClientRect().top + scrollY - offset(), 0, maxScroll())
      const distance = Math.abs(destination() - start)
      if (instant || reduced.matches || distance < 2) {
        window.scrollTo({top: destination(), behavior:'instant'})
        schedule()
        return
      }
      const duration = clamp(250 + Math.sqrt(distance) * 6, 300, 680)
      const state = animation = {raf:0, start:performance.now(), entry}
      function step(now) {
        if (animation !== state) return
        const p = clamp((now - state.start) / duration, 0, 1)
        const eased = p < .5 ? 4*p*p*p : 1-Math.pow(-2*p+2,3)/2
        window.scrollTo({top: start + (destination() - start) * eased, behavior:'instant'})
        if (p < 1) state.raf = requestAnimationFrame(step)
        else {
          window.scrollTo({top:destination(), behavior:'instant'})
          animation = null
          select(entry, true)
          schedule()
        }
      }
      state.raf = requestAnimationFrame(step)
    }
    function panel(open) {
      card.classList.toggle('halo-toc-open', open)
      toggle?.setAttribute('aria-expanded', String(open))
      card.inert = mobile.matches && !open
      if (open) requestAnimationFrame(() => reveal(active, true))
    }
    toggle?.addEventListener('click', () => panel(!card.classList.contains('halo-toc-open')))
    mobile.addEventListener?.('change', () => panel(false))
    panel(false)
    content.addEventListener('click', event => {
      const branch = event.target.closest('.halo-toc-branch')
      if (branch) {
        const li = branch.closest('li')
        manual.set(li, !li.classList.contains('halo-expanded')); tree()
        return
      }
      const link = event.target.closest('.toc-link')
      const entry = entries.find(e => e.link === link)
      if (!entry || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return
      event.preventDefault()
      if (mobile.matches) { panel(false); toggle?.focus({preventScroll:true}) }
      jump(entry)
    })
    document.addEventListener('click', e => {
      if (mobile.matches && card.classList.contains('halo-toc-open') && !card.contains(e.target) && !toggle?.contains(e.target)) panel(false)
    })
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && card.classList.contains('halo-toc-open')) { panel(false); toggle?.focus() }
      if (['ArrowUp','ArrowDown','PageUp','PageDown','Home','End',' '].includes(e.key) && !content.contains(e.target)) cancel()
    })
    window.addEventListener('wheel', e => { if (!content.contains(e.target)) cancel() }, {passive:true})
    window.addEventListener('touchstart', e => { if (!content.contains(e.target)) cancel() }, {passive:true})
    content.addEventListener('wheel', () => { sidebarUntil = performance.now() + 1600 }, {passive:true})
    content.addEventListener('touchstart', () => { sidebarUntil = performance.now() + 1600 }, {passive:true})
    window.addEventListener('scroll', schedule, {passive:true})
    window.addEventListener('resize', invalidate, {passive:true})
    article.addEventListener('load', invalidate, true)
    document.fonts?.ready.then(invalidate)
    if ('ResizeObserver' in window) new ResizeObserver(invalidate).observe(article)
    function hashJump() {
      const heading = resolve(location.hash)
      const e = entries.find(x => x.heading === heading)
      if (e) jump(e, false, true)
      else { cancel(); schedule() }
    }
    window.addEventListener('hashchange', hashJump)
    window.addEventListener('popstate', hashJump)
    if (location.hash) requestAnimationFrame(hashJump)
    schedule()
  }
})()
