// Navbar interactions
const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

if (navToggle && navLinks) {
	navToggle.addEventListener('click', () => {
		navLinks.classList.toggle('open');
	});
}

// Sticky navbar color change on scroll
const onScroll = () => {
	const scrolled = window.scrollY > 10;
	navbar && navbar.style.setProperty('background', scrolled ? 'rgba(255,255,255,0.92)' : 'rgba(255,255,255,0.75)');
};
window.addEventListener('scroll', onScroll);
onScroll();

// Smooth scroll for same-page anchors
document.addEventListener('click', (e) => {
	const link = e.target.closest('a[href^="#"]');
	if (!link) return;
	const target = document.querySelector(link.getAttribute('href'));
	if (target) {
		e.preventDefault();
		target.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}
});

// Reveal on scroll using IntersectionObserver
const revealEls = Array.from(document.querySelectorAll('.reveal'));
if (revealEls.length) {
	const io = new IntersectionObserver((entries) => {
		entries.forEach((entry) => {
			if (entry.isIntersecting) {
				entry.target.classList.add('revealed');
				io.unobserve(entry.target);
			}
		});
	}, { threshold: 0.15 });
	revealEls.forEach((el) => io.observe(el));
}

// Simple carousel
const carousel = document.querySelector('[data-carousel]');
if (carousel) {
	const track = carousel.querySelector('[data-carousel-track]');
	const prevBtn = carousel.querySelector('[data-carousel-prev]');
	const nextBtn = carousel.querySelector('[data-carousel-next]');
	const slides = Array.from(track.children);
	let index = 0;
	const update = () => {
		track.style.transform = `translateX(-${index * 100}%)`;
	};
	const next = () => { index = (index + 1) % slides.length; update(); };
	const prev = () => { index = (index - 1 + slides.length) % slides.length; update(); };
	nextBtn?.addEventListener('click', next);
	prevBtn?.addEventListener('click', prev);
	let timer = setInterval(next, 3500);
	carousel.addEventListener('mouseenter', () => clearInterval(timer));
	carousel.addEventListener('mouseleave', () => (timer = setInterval(next, 3500)));
}

// Floating report button bob
const reportBtn = document.getElementById('reportBtn');
if (reportBtn) {
	let up = true;
	setInterval(() => {
		reportBtn.style.transform = `translateY(${up ? '-2px' : '0'})`;
		up = !up;
	}, 800);
}

// Dynamic testimonials auto-slide
const testimonials = document.querySelector('[data-testimonials]');
if (testimonials) {
	const items = Array.from(testimonials.querySelectorAll('.testimonial'));
	let i = 0;
	setInterval(() => {
		items[i].classList.remove('active');
		i = (i + 1) % items.length;
		items[i].classList.add('active');
	}, 4000);
}

// Contact form: floating paw on submit + fake send
const contactForm = document.getElementById('contactForm');
if (contactForm) {
	const paw = document.getElementById('pawFloat');
	contactForm.addEventListener('submit', (e) => {
		e.preventDefault();
		if (paw) {
			paw.style.opacity = '1';
			paw.style.transform = 'translateY(-18px) scale(1)';
			setTimeout(() => {
				paw.style.opacity = '0';
				paw.style.transform = 'translateY(10px) scale(.9)';
			}, 900);
		}
		contactForm.reset();
		alert('Thanks! Your message has been sent.');
	});
}

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Accessibility: close nav on outside click (mobile)
document.addEventListener('click', (e) => {
	if (!navLinks || !navToggle) return;
	if (!navLinks.classList.contains('open')) return;
	if (!e.target.closest('#navLinks') && !e.target.closest('#navToggle')) {
		navLinks.classList.remove('open');
	}
});


