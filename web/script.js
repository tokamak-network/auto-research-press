// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offset = 80; // Offset for sticky nav
            const targetPosition = target.offsetTop - offset;
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Highlight active section in TOC
const sections = document.querySelectorAll('.section');
const navLinks = document.querySelectorAll('.toc-nav a');

function highlightActiveSection() {
    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 150;
        const sectionBottom = sectionTop + section.offsetHeight;

        if (window.pageYOffset >= sectionTop && window.pageYOffset < sectionBottom) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

// Throttle scroll event for performance
let scrollTimeout;
window.addEventListener('scroll', () => {
    if (!scrollTimeout) {
        scrollTimeout = setTimeout(() => {
            highlightActiveSection();
            scrollTimeout = null;
        }, 100);
    }
});

// Initial highlight
highlightActiveSection();

// Add fade-in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all sections for fade-in effect
document.querySelectorAll('.section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
});

// Copy code blocks on click
document.querySelectorAll('.code-block, .breakdown-chart').forEach(block => {
    block.style.cursor = 'pointer';
    block.title = 'Click to copy';

    block.addEventListener('click', async () => {
        const text = block.textContent;
        try {
            await navigator.clipboard.writeText(text);

            // Visual feedback
            const originalBg = block.style.backgroundColor;
            block.style.backgroundColor = '#10b981';
            block.style.transition = 'background-color 0.3s';

            setTimeout(() => {
                block.style.backgroundColor = originalBg;
            }, 300);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    });
});

// Add reading progress bar
const progressBar = document.createElement('div');
progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 4px;
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    width: 0%;
    z-index: 1000;
    transition: width 0.1s;
`;
document.body.prepend(progressBar);

window.addEventListener('scroll', () => {
    const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (window.scrollY / windowHeight) * 100;
    progressBar.style.width = scrolled + '%';
});

// Table of contents sticky behavior enhancement
const tocNav = document.querySelector('.toc-nav');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > lastScroll && currentScroll > 100) {
        tocNav.style.transform = 'translateY(-100%)';
    } else {
        tocNav.style.transform = 'translateY(0)';
    }

    lastScroll = currentScroll;
});

tocNav.style.transition = 'transform 0.3s ease';

// Print friendly
window.addEventListener('beforeprint', () => {
    document.querySelectorAll('.section').forEach(section => {
        section.style.opacity = '1';
        section.style.transform = 'none';
    });
});

console.log('📊 Research Report Loaded Successfully');