/* BULDO web: interakce a animace (bez knihoven) */
(() => {
  const doc = document.documentElement;
  doc.classList.add('js');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const range = (p, a, b) => clamp((p - a) / (b - a));
  const ease = t => 1 - Math.pow(1 - t, 3);
  const easeInOut = t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

  /* ---------- Mobilní menu ---------- */
  const burger = document.querySelector('.nav-burger');
  if (burger) {
    const header = burger.closest('.site-header');
    const toggle = open => {
      header.classList.toggle('nav-open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Zavřít menu' : 'Otevřít menu');
      document.body.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', () => toggle(!header.classList.contains('nav-open')));
    header.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => toggle(false)));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
  }

  /* ---------- Objevení při scrollu ---------- */
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-visible');
      io.unobserve(e.target);
      if (e.target.classList.contains('stats')) countUp(e.target);
    });
  }, { threshold: .2, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal, .stats').forEach(el => io.observe(el));

  /* ---------- Čísla: vyjedou nahoru a napočítají se ---------- */
  document.querySelectorAll('.stat').forEach((s, i) => s.style.setProperty('--i', i));
  function countUp(root) {
    root.querySelectorAll('[data-count]').forEach((el, i) => {
      const end = +el.dataset.count, suf = el.dataset.suffix || '';
      if (reduce) { el.textContent = end + suf; return; }
      const dur = 1600, start = performance.now() + i * 120;
      const tick = now => {
        const t = clamp((now - start) / dur);
        el.textContent = Math.round(end * ease(t)) + suf;
        if (t < 1) requestAnimationFrame(tick);
      };
      el.textContent = '0' + suf;
      requestAnimationFrame(tick);
    });
  }

  /* ---------- Scéna: papírky se při scrollu složí do telefonu ---------- */
  const scene = document.getElementById('scene');
  if (scene) {
    if (reduce) {
      doc.classList.add('no-scene');
    } else {
      const t1 = scene.querySelector('.scene-t1');
      const t2 = scene.querySelector('.scene-t2');
      const items = [...scene.querySelectorAll('.chaos-item')];
      const phone = scene.querySelector('.control-phone');
      const fit = scene.querySelector('.control-fit');
      const notifs = [...scene.querySelectorAll('.notif')];
      const cta = scene.querySelector('.scene-cta');
      let geo = null, ticking = false;

      const measure = () => {
        // měřítko telefonu a bublin podle výšky okna
        const mobile = window.innerWidth <= 960;
        const availH = window.innerHeight - (mobile ? 330 : 420);
        const availW = window.innerWidth - 16;
        const s = clamp(Math.min(availH / 560, availW / (mobile ? 360 : 860)), .55, 1);
        fit.style.setProperty('--s', s.toFixed(3));
        // výchozí pozice bez transformací
        items.forEach(el => (el.style.transform = 'none'));
        phone.style.transform = 'none';
        const pr = phone.getBoundingClientRect();
        const target = { x: pr.left + pr.width / 2, y: pr.top + pr.height * .42 };
        geo = items.map(el => {
          const r = el.getBoundingClientRect();
          return { dx: target.x - (r.left + r.width / 2), dy: target.y - (r.top + r.height / 2), w: r.width, pw: pr.width };
        });
        update();
      };

      const update = () => {
        ticking = false;
        if (!geo) return;
        const r = scene.getBoundingClientRect();
        const total = scene.offsetHeight - window.innerHeight;
        const p = clamp(-r.top / total);

        // 1) titulek chaosu mizí
        const a = range(p, .06, .22);
        t1.style.opacity = 1 - a;
        t1.style.transform = `translate(-50%, calc(-50% - ${a * 40}px))`;

        // 2) papírky letí do telefonu, zmenšují se a mizí
        items.forEach((el, i) => {
          const g = geo[i];
          const k = easeInOut(range(p, .12 + i * .015, .5 + i * .015));
          const sc = 1 - k * (1 - (g.pw * .25) / g.w);
          // v klidu žádná transformace, aby papírky zůstaly ostré
          el.style.transform = k === 0 ? 'none' : `translate(${g.dx * k}px, ${g.dy * k}px) scale(${sc}) rotate(${k * (i % 2 ? 8 : -8)}deg)`;
          el.style.opacity = 1 - range(p, .42 + i * .015, .52 + i * .015);
        });

        // 3) telefon vyjede zespodu
        const ph = ease(range(p, .14, .45));
        phone.style.transform = `translateY(${(1 - ph) * 70}vh)`;
        phone.style.opacity = range(p, .14, .26);

        // 4) titulek „S BULDO máte vše pod kontrolou.“
        const b = ease(range(p, .48, .6));
        t2.style.opacity = b;
        t2.style.transform = `translateY(${(1 - b) * 24}px)`;

        // 5) bubliny vyskakují postupně
        notifs.forEach((n, i) => {
          const q = range(p, .58 + i * .07, .66 + i * .07);
          const e = 1 - Math.pow(1 - q, 3);
          n.style.opacity = q;
          n.style.transform = `translateY(${(1 - e) * 18}px) scale(${.86 + .14 * e})`;
        });

        // 6) tlačítko
        const c = ease(range(p, .86, .94));
        cta.style.opacity = c;
        cta.style.transform = `translateY(${(1 - c) * 12}px)`;
      };

      const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
      window.addEventListener('scroll', onScroll, { passive: true });
      let rt;
      window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(measure, 120); });
      window.addEventListener('load', measure);
      measure();
    }
  }

  /* ---------- Hlavní funkce: přepínání videí ---------- */
  const tabs = [...document.querySelectorAll('.feature-tab')];
  if (tabs.length) {
    const videos = tabs.map(t => document.getElementById(t.getAttribute('aria-controls')));
    const prev = document.querySelector('.f-prev'), next = document.querySelector('.f-next');
    let cur = 0;
    const play = v => { const pr = v.play(); if (pr) pr.catch(() => {}); };
    const select = (i, focus) => {
      i = clamp(i, 0, tabs.length - 1);
      tabs.forEach((t, j) => { t.setAttribute('aria-selected', String(i === j)); t.tabIndex = i === j ? 0 : -1; });
      videos.forEach((v, j) => {
        if (j === i) {
          if (!v.src && v.dataset.src) v.src = v.dataset.src;
          v.currentTime = 0; v.classList.add('active'); play(v);
        } else { v.classList.remove('active'); v.pause(); }
      });
      cur = i;
      prev.disabled = i === 0; next.disabled = i === tabs.length - 1;
      if (focus) tabs[i].focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', e => {
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); select(cur + 1, true); }
        if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); select(cur - 1, true); }
      });
    });
    prev.addEventListener('click', () => select(cur - 1));
    next.addEventListener('click', () => select(cur + 1));
    // přehrávat jen když je sekce vidět
    const box = document.querySelector('.features-box');
    new IntersectionObserver(([e]) => {
      const v = videos[cur];
      if (e.isIntersecting) play(v); else v.pause();
    }, { threshold: .25 }).observe(box);
    select(0);
  }

  /* ---------- Ceník: roční / měsíční ---------- */
  const pricing = document.querySelector('.pricing');
  if (pricing) {
    const btns = [...pricing.querySelectorAll('.switch button')];
    const knob = pricing.querySelector('.switch .knob');
    const place = b => { knob.style.width = b.offsetWidth + 'px'; knob.style.transform = `translateX(${b.offsetLeft - 6}px)`; };
    const set = period => {
      pricing.dataset.period = period;
      btns.forEach(b => { const on = b.dataset.period === period; b.setAttribute('aria-pressed', String(on)); if (on) place(b); });
      pricing.querySelectorAll('.price strong').forEach(s => (s.textContent = s.dataset[period]));
      pricing.querySelectorAll('.save').forEach(s => (s.style.visibility = period === 'yearly' ? 'visible' : 'hidden'));
    };
    btns.forEach(b => b.addEventListener('click', () => set(b.dataset.period)));
    window.addEventListener('resize', () => place(btns.find(b => b.getAttribute('aria-pressed') === 'true')));
    document.fonts && document.fonts.ready.then(() => set(pricing.dataset.period));
    set(pricing.dataset.period);
  }

  /* ---------- Tabulka tarifů: přepínač na mobilu ---------- */
  const ctabs = [...document.querySelectorAll('.compare-tabs button')];
  const ctable = document.querySelector('.compare');
  ctabs.forEach(b => b.addEventListener('click', () => {
    ctabs.forEach(x => x.setAttribute('aria-selected', String(x === b)));
    ctable.dataset.col = b.dataset.col;
  }));

  /* ---------- Články: Načíst více ---------- */
  const more = document.querySelector('[data-more]');
  if (more) more.addEventListener('click', () => {
    document.querySelectorAll('.acard.is-hidden').forEach(c => c.classList.remove('is-hidden'));
    more.remove();
  });

  /* ---------- Kontaktní formulář (ukázka bez serveru) ---------- */
  const form = document.getElementById('contact-form');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    const msg = form.querySelector('.form-msg');
    if (!form.checkValidity()) {
      msg.style.background = '#FDECEC'; msg.style.color = '#9B1C1C';
      msg.textContent = 'Vyplňte prosím jméno, platný e-mail a potvrďte souhlas se zpracováním údajů.';
    } else {
      msg.style.background = ''; msg.style.color = '';
      msg.textContent = 'Děkujeme, zprávu jsme přijali. Ozveme se vám do 1 pracovního dne.';
      form.reset();
    }
    msg.classList.add('show');
  });

  /* ---------- Poradna: hledání a aktivní kategorie ---------- */
  const q = document.getElementById('help-q');
  if (q) {
    const sections = [...document.querySelectorAll('[data-help-section]')];
    const empty = document.querySelector('.help-empty');
    const norm = s => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    const filter = () => {
      const term = norm(q.value.trim());
      let any = false;
      sections.forEach(sec => {
        const title = norm(sec.querySelector('h2').textContent);
        let hit = false;
        sec.querySelectorAll('details').forEach(d => {
          const ok = !term || title.includes(term) || norm(d.textContent).includes(term);
          d.classList.toggle('is-hidden', !ok); if (ok) hit = true;
        });
        sec.classList.toggle('is-hidden', !hit); if (hit) any = true;
      });
      empty.classList.toggle('show', !any);
    };
    q.addEventListener('input', filter);
    q.form.addEventListener('submit', filter);
    const links = [...document.querySelectorAll('.help-side a')];
    const helpIO = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    sections.forEach(s => helpIO.observe(s));
  }
})();
