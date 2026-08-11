/* ============================
   MOBILE HAMBURGER MENU
   ============================ */
(function() {
    const hamburger = document.getElementById('hamburger');
    const nav = document.getElementById('nav');

    if (hamburger && nav) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            nav.classList.toggle('nav--open');
        });

        document.addEventListener('click', function(e) {
            if (!nav.contains(e.target) && !hamburger.contains(e.target)) {
                hamburger.classList.remove('active');
                nav.classList.remove('nav--open');
            }
        });

        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                nav.classList.remove('nav--open');
            });
        });
    }
})();

/* ============================
   FAQ ACCORDION
   ============================ */
(function() {
    const questions = document.querySelectorAll('.faq__question');

    questions.forEach(btn => {
        btn.addEventListener('click', function() {
            const item = this.parentElement;
            const isActive = item.classList.contains('active');

            questions.forEach(q => {
                q.parentElement.classList.remove('active');
                q.setAttribute('aria-expanded', 'false');
            });

            if (!isActive) {
                item.classList.add('active');
                this.setAttribute('aria-expanded', 'true');
            }
        });
    });
})();

/* ============================
   SMOOTH SCROLL
   ============================ */
(function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
})();

/* ============================
   STICKY HEADER SHADOW
   ============================ */
(function() {
    const header = document.getElementById('header');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.style.borderBottomColor = 'rgba(255,255,255,0.1)';
        } else {
            header.style.borderBottomColor = 'rgba(255,255,255,0.06)';
        }
    });
})();

