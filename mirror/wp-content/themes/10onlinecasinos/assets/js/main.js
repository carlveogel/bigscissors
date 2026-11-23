/**
 * Main theme JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // Wrap classic content tables so they can scroll on small screens.
    document.querySelectorAll('.lucky-entry-content table').forEach(function (table) {
        if (table.closest('.wp-block-table') || table.closest('.lucky-table-scroll')) {
            return;
        }

        const wrapper = document.createElement('div');
        wrapper.className = 'lucky-table-scroll';
        // Make the scrollable region reachable and named for keyboard / screen reader users.
        wrapper.setAttribute('tabindex', '0');
        wrapper.setAttribute('role', 'region');
        const caption = table.querySelector('caption');
        wrapper.setAttribute('aria-label', caption ? caption.textContent.trim() : 'Table');
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });

    // Mobile navigation toggle
    const siteNavigation = document.getElementById('site-navigation');

    if (siteNavigation) {
        const button = siteNavigation.querySelector('.lucky-menu-toggle');
        const menu = siteNavigation.querySelector('.lucky-menu-list');

        if (button && menu) {
            const hamburgerIcon = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>`;
            const closeIcon = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`;
            const mobileQuery = window.matchMedia('(max-width: 768px)');
            const parentItems = siteNavigation.querySelectorAll('.menu-item-has-children');

            function isMenuOpen() {
                return siteNavigation.classList.contains('is-toggled');
            }

            function closeMenu(returnFocus) {
                siteNavigation.classList.remove('is-toggled');
                button.setAttribute('aria-expanded', 'false');
                button.innerHTML = hamburgerIcon + '<span class="lucky-screen-reader-text">Menu</span>';
                document.body.style.overflow = '';

                if (returnFocus) {
                    button.focus();
                }
            }

            button.addEventListener('click', function () {
                const isOpen = siteNavigation.classList.toggle('is-toggled');
                button.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
                button.innerHTML = isOpen
                    ? closeIcon + '<span class="lucky-screen-reader-text">Close Menu</span>'
                    : hamburgerIcon + '<span class="lucky-screen-reader-text">Menu</span>';
                document.body.style.overflow = isOpen ? 'hidden' : '';
            });

            // Close when the backdrop (the nav element itself) is tapped.
            siteNavigation.addEventListener('click', function (event) {
                if (!mobileQuery.matches) {
                    return;
                }

                if (event.target === siteNavigation) {
                    closeMenu(false);
                }
            });

            // Close after choosing a link, but not for parent links that open a submenu.
            menu.querySelectorAll('a').forEach(function (link) {
                link.addEventListener('click', function () {
                    if (!mobileQuery.matches) {
                        return;
                    }

                    const parentItem = link.parentElement;
                    if (parentItem && parentItem.classList.contains('menu-item-has-children')) {
                        return;
                    }

                    closeMenu(false);
                });
            });

            // Close on Escape key and give focus back to the toggle.
            document.addEventListener('keydown', function (e) {
                if (e.key === 'Escape' && isMenuOpen()) {
                    closeMenu(true);
                }
            });

            // Reset the drawer if the viewport grows past the mobile breakpoint.
            function handleBreakpointChange() {
                if (!mobileQuery.matches && isMenuOpen()) {
                    closeMenu(false);
                }
            }

            if (mobileQuery.addEventListener) {
                mobileQuery.addEventListener('change', handleBreakpointChange);
            } else if (mobileQuery.addListener) {
                mobileQuery.addListener(handleBreakpointChange);
            }

            // Reset state when the page is restored from the back/forward cache.
            window.addEventListener('pageshow', function (event) {
                if (event.persisted && isMenuOpen()) {
                    closeMenu(false);
                }
            });

            // Mobile: accordion toggle for parent items with submenus
            parentItems.forEach(function (item) {
                const link = item.querySelector(':scope > a');
                const sub = item.querySelector(':scope > .sub-menu');
                if (!link || !sub) return;

                link.setAttribute('aria-expanded', 'false');

                link.addEventListener('click', function (e) {
                    // Only intercept on mobile (toggle is visible)
                    if (window.getComputedStyle(button).display === 'none') return;

                    e.preventDefault();

                    // Close siblings
                    parentItems.forEach(function (sibling) {
                        if (sibling !== item) {
                            sibling.classList.remove('is-open');
                            const siblingLink = sibling.querySelector(':scope > a');
                            if (siblingLink) siblingLink.setAttribute('aria-expanded', 'false');
                        }
                    });

                    const isOpen = item.classList.toggle('is-open');
                    link.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
                });
            });
        }
    }

    const searchWrap = document.getElementById('bw-search-wrap');
    const searchButton = document.getElementById('bw-search-btn');
    const searchDropdown = document.getElementById('bw-search-dropdown');

    if (searchWrap && searchButton && searchDropdown) {
        const searchField = searchDropdown.querySelector('.bw-search-input');
        let focusTimer = null;

        // inert keeps the hidden dropdown out of the tab order as well as the accessibility tree.
        searchDropdown.inert = !searchWrap.classList.contains('is-open');

        function isSearchOpen() {
            return searchWrap.classList.contains('is-open');
        }

        function closeSearch(returnFocus) {
            window.clearTimeout(focusTimer);
            searchWrap.classList.remove('is-open');
            searchButton.setAttribute('aria-expanded', 'false');
            searchDropdown.setAttribute('aria-hidden', 'true');
            searchDropdown.inert = true;

            if (returnFocus) {
                searchButton.focus();
            }
        }

        searchButton.addEventListener('click', function (event) {
            event.preventDefault();

            if (isSearchOpen()) {
                closeSearch(false);
                return;
            }

            searchWrap.classList.add('is-open');
            searchButton.setAttribute('aria-expanded', 'true');
            searchDropdown.setAttribute('aria-hidden', 'false');
            searchDropdown.inert = false;

            if (searchField) {
                focusTimer = window.setTimeout(function () {
                    searchField.focus();
                }, 60);
            }
        });

        document.addEventListener('click', function (event) {
            if (isSearchOpen() && !searchWrap.contains(event.target)) {
                closeSearch(false);
            }
        });

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && isSearchOpen()) {
                closeSearch(searchWrap.contains(document.activeElement));
            }
        });
    }

    // Shortlist carousel with category tabs
    document.querySelectorAll('.shortlist').forEach(function (shortlist) {
        const track = shortlist.querySelector('.carousel__track');
        if (!track) return;

        const prevButton = shortlist.querySelector('.carousel__arrow--prev');
        const nextButton = shortlist.querySelector('.carousel__arrow--next');
        const dotsWrap = shortlist.querySelector('.carousel__dots');
        const tabs = Array.prototype.slice.call(shortlist.querySelectorAll('.tab'));
        let ticking = false;

        function visibleCards() {
            return Array.prototype.slice.call(track.querySelectorAll('.casino-card:not([hidden])'));
        }

        function stepSize() {
            const card = visibleCards()[0];
            const gap = parseFloat(window.getComputedStyle(track).columnGap) || 16;
            return card ? card.offsetWidth + gap : 300;
        }

        function maxScroll() {
            return Math.max(0, track.scrollWidth - track.clientWidth);
        }

        function pageCount() {
            return Math.round(maxScroll() / stepSize()) + 1;
        }

        // One dot per scroll position, rebuilt when the card set or width changes.
        function buildDots() {
            if (!dotsWrap) return;

            const count = pageCount();
            dotsWrap.innerHTML = '';
            for (let n = 0; n < count; n++) {
                dotsWrap.appendChild(document.createElement('span'));
            }
            dotsWrap.style.display = count > 1 ? '' : 'none';
        }

        function updateState() {
            ticking = false;

            const max = maxScroll();
            const atStart = track.scrollLeft <= 1;
            const atEnd = track.scrollLeft >= max - 1;

            if (prevButton) prevButton.disabled = atStart;
            if (nextButton) nextButton.disabled = atEnd;

            if (dotsWrap) {
                const dots = dotsWrap.querySelectorAll('span');
                const active = atEnd ? dots.length - 1 : Math.round(track.scrollLeft / stepSize());
                dots.forEach(function (dot, n) {
                    dot.classList.toggle('is-active', n === active);
                });
            }
        }

        function refresh() {
            buildDots();
            updateState();
        }

        if (prevButton) {
            prevButton.addEventListener('click', function () {
                track.scrollBy({ left: -stepSize(), behavior: 'smooth' });
            });
        }

        if (nextButton) {
            nextButton.addEventListener('click', function () {
                track.scrollBy({ left: stepSize(), behavior: 'smooth' });
            });
        }

        track.addEventListener('scroll', function () {
            if (!ticking) {
                ticking = true;
                window.requestAnimationFrame(updateState);
            }
        }, { passive: true });

        if ('ResizeObserver' in window) {
            new ResizeObserver(refresh).observe(track);
        } else {
            window.addEventListener('resize', refresh);
        }

        // Tabs: ARIA tabs pattern with roving tabindex and arrow-key navigation.
        if (!track.id) {
            track.id = 'shortlist-track-' + Math.random().toString(36).slice(2, 8);
        }
        if (tabs.length) {
            track.setAttribute('role', 'tabpanel');
        }

        function selectTab(tab) {
            tabs.forEach(function (t) {
                const selected = t === tab;
                t.classList.toggle('is-active', selected);
                t.setAttribute('aria-selected', selected ? 'true' : 'false');
                t.setAttribute('tabindex', selected ? '0' : '-1');
            });

            const filter = tab.dataset.filter;
            track.querySelectorAll('.casino-card').forEach(function (card) {
                card.hidden = filter !== 'all' && card.dataset.category !== filter;
            });

            track.scrollLeft = 0;
            refresh();
        }

        tabs.forEach(function (tab, index) {
            tab.setAttribute('aria-controls', track.id);
            tab.setAttribute('tabindex', tab.classList.contains('is-active') ? '0' : '-1');

            tab.addEventListener('click', function () {
                selectTab(tab);
            });

            tab.addEventListener('keydown', function (event) {
                let next = null;

                if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
                if (event.key === 'ArrowLeft') next = tabs[(index - 1 + tabs.length) % tabs.length];
                if (event.key === 'Home') next = tabs[0];
                if (event.key === 'End') next = tabs[tabs.length - 1];

                if (next) {
                    event.preventDefault();
                    next.focus();
                    selectTab(next);
                }
            });
        });

        refresh();
    });
});
