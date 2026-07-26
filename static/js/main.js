// main.js — students will add JavaScript here as features are built

function animateHeroStats() {
    const duration = 1200;
    const start = performance.now();

    const counters = Array.from(document.querySelectorAll(".mock-stat-value[data-count-to]")).map((el) => ({
        el,
        target: Number(el.dataset.countTo),
        prefix: el.dataset.prefix || "",
    }));

    const bars = Array.from(document.querySelectorAll(".mock-bar[data-width]"));
    bars.forEach((bar) => {
        requestAnimationFrame(() => {
            bar.style.width = bar.dataset.width + "%";
        });
    });

    if (!counters.length) return;

    function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);

        counters.forEach(({ el, target, prefix }) => {
            const value = Math.round(target * eased);
            el.textContent = prefix + value.toLocaleString("en-IN");
        });

        if (progress < 1) {
            requestAnimationFrame(tick);
        }
    }

    requestAnimationFrame(tick);
}

document.addEventListener("DOMContentLoaded", animateHeroStats);
