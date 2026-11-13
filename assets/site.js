(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header-Linie nach dem ersten Scrollen */
  var sentinel = document.createElement('div');
  sentinel.style.cssText = 'position:absolute;top:0;height:1px;width:1px;';
  document.body.prepend(sentinel);
  new IntersectionObserver(function (e) { header.classList.toggle('is-scrolled', !e[0].isIntersecting); }).observe(sentinel);

  /* Mobiles Menü */
  function setMenu(open) {
    header.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');
  }
  if (toggle) {
    toggle.addEventListener('click', function () { setMenu(!header.classList.contains('is-open')); });
    document.querySelectorAll('.nav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && header.classList.contains('is-open')) { setMenu(false); toggle.focus(); } });
    window.matchMedia('(min-width: 901px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  /* Einblenden beim Scrollen */
  var reveal = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); reveal.unobserve(en.target); } });
  }, { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('.tile, .reveal-img, .svc-ov__list').forEach(function (el) { reveal.observe(el); });

  /* Touch-Geräte: Kacheln werden farbig, sobald sie im Bild sind */
  if (window.matchMedia('(hover: none)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.target.classList.toggle('is-colored', en.intersectionRatio > 0.75); });
    }, { threshold: [0, 0.75, 1] });
    document.querySelectorAll('.tile').forEach(function (t) { io.observe(t); });
  }

  /* Projektdetail als Overlay */
  var dataEl = document.getElementById('projects-data');
  var dlg = document.getElementById('pd');
  if (dataEl && dlg) {
    var projects = JSON.parse(dataEl.textContent);
    var idx = 0, img = 0, opener = null;
    var $ = function (s) { return dlg.querySelector(s); };
    var mediaImg = $('.pd__media img'), caption = $('.pd__media figcaption'), thumbs = $('.pd__thumbs');

    function showImage(i) {
      var p = projects[idx], im = p.images[i];
      img = i;
      mediaImg.src = im.src; mediaImg.alt = im.alt; mediaImg.width = im.w; mediaImg.height = im.h;
      if (!reduce) { mediaImg.classList.remove('swap'); void mediaImg.offsetWidth; mediaImg.classList.add('swap'); }
      caption.textContent = im.note || '';
      thumbs.querySelectorAll('button').forEach(function (b, j) { b.setAttribute('aria-current', j === i ? 'true' : 'false'); });
    }
    function render(i) {
      idx = (i + projects.length) % projects.length;
      var p = projects[idx];
      $('#pd-title').textContent = p.name;
      $('.pd__count').textContent = (idx + 1) + ' / ' + projects.length;
      $('.pd__data').innerHTML = p.data.map(function (d) { return '<div><dt>' + d[0] + '</dt><dd>' + d[1] + '</dd></div>'; }).join('');
      thumbs.innerHTML = p.images.length > 1 ? p.images.map(function (im, j) {
        return '<button type="button" aria-label="Bild ' + (j + 1) + ' anzeigen"><img src="' + im.src + '" alt="" loading="lazy"></button>';
      }).join('') : '';
      thumbs.querySelectorAll('button').forEach(function (b, j) { b.addEventListener('click', function () { showImage(j); }); });
      showImage(0);
      dlg.scrollTop = 0;
      history.replaceState(null, '', '#' + p.id);
    }
    function open(i, from) {
      opener = from || null;
      render(i);
      if (!dlg.open) dlg.showModal();
      document.body.classList.add('pd-open');
    }
    function close() { dlg.close(); }
    dlg.addEventListener('close', function () {
      document.body.classList.remove('pd-open');
      history.replaceState(null, '', location.pathname);
      if (opener) opener.focus();
    });
    $('.pd__close').addEventListener('click', close);
    $('.pd__prev').addEventListener('click', function () { render(idx - 1); });
    $('.pd__next').addEventListener('click', function () { render(idx + 1); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') render(idx + 1);
      if (e.key === 'ArrowLeft') render(idx - 1);
    });
    document.querySelectorAll('[data-project]').forEach(function (t) {
      t.addEventListener('click', function () { open(+t.getAttribute('data-project'), t); });
    });
    var hash = location.hash.slice(1);
    if (hash) projects.forEach(function (p, i) { if (p.id === hash) open(i); });
  }

  /* Kontaktformular (Prototyp) */
  var form = document.getElementById('anfrage');
  if (form) {
    var status = form.querySelector('.form__status');
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var mail = form.querySelector('#f-mail');
      if (mail.value.trim() && !mail.checkValidity()) {
        status.textContent = 'Die E-Mail-Adresse scheint unvollständig zu sein. Bitte prüfen Sie die Schreibweise.';
        mail.focus();
        return;
      }
      var btn = form.querySelector('button[type=submit]');
      btn.disabled = true;
      status.textContent = 'Wird gesendet …';
      setTimeout(function () {
        form.reset();
        btn.disabled = false;
        status.textContent = 'Danke für Ihre Anfrage. Sie erhalten in Kürze eine persönliche Rückmeldung.';
      }, 900);
    });
  }
})();
