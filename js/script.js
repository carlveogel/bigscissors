/* Aussie Casinos — site behaviour (no dependencies) */
(function () {
    'use strict';

    /* Mobile navigation */
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('site-nav');

    function setNav(open) {
        if (!toggle || !nav) return;
        nav.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
        document.body.classList.toggle('nav-open', open);
    }

    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            setNav(!nav.classList.contains('is-open'));
        });
        nav.addEventListener('click', function (e) {
            if (e.target.closest('a')) setNav(false);
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && nav.classList.contains('is-open')) {
                setNav(false);
                toggle.focus();
            }
        });
        window.addEventListener('resize', function () {
            if (window.innerWidth > 960) setNav(false);
        });
    }

    /* Header shadow once the page scrolls */
    var header = document.querySelector('.site-header');
    function onScroll() {
        if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* Highlight the current section in the contents list */
    var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"]'));
    if (tocLinks.length && 'IntersectionObserver' in window) {
        var bySection = new Map();
        tocLinks.forEach(function (link) {
            var section = document.getElementById(link.getAttribute('href').slice(1));
            if (section) bySection.set(section, link);
        });

        var toc = document.querySelector('.toc');
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var active = bySection.get(entry.target);
                tocLinks.forEach(function (l) { l.classList.toggle('is-active', l === active); });
                /* Keep the active chip visible in the horizontal mobile bar */
                if (toc && toc.scrollWidth > toc.clientWidth) {
                    toc.scrollTo({ left: active.offsetLeft - 16, behavior: 'smooth' });
                }
            });
        }, { rootMargin: '-35% 0px -60% 0px' });

        bySection.forEach(function (_link, section) { observer.observe(section); });
    }
})();
