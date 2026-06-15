const splash = document.querySelector("[data-splash]");
const navToggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");
const navLinks = [...document.querySelectorAll(".site-nav a")];
const videoFrame = document.querySelector("[data-video-frame]");
const video = document.querySelector("[data-video-player]");
const videoPlaceholder = document.querySelector("[data-video-placeholder]");
const certificateGrid = document.querySelector("#certificate-grid");
const evidenceGrid = document.querySelector("#evidence-grid");
const filterButtons = [...document.querySelectorAll("[data-filter]")];
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function hideSplash() {
  if (!splash) return;
  splash.classList.add("hide");
  window.setTimeout(() => splash.remove(), 650);
}

window.addEventListener("load", () => {
  window.setTimeout(hideSplash, prefersReducedMotion ? 0 : 650);
});
window.setTimeout(hideSplash, 3200);

if (navToggle && nav) {
  navToggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    document.body.classList.toggle("nav-open", isOpen);
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("open");
      document.body.classList.remove("nav-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

function setupReveal() {
  const items = [...document.querySelectorAll(".reveal")];
  if (!items.length) return;
  if (prefersReducedMotion || !("IntersectionObserver" in window)) {
    items.forEach((item) => item.classList.add("visible"));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.14 });

  items.forEach((item) => observer.observe(item));
}

function setupActiveNav() {
  if (!navLinks.length || !("IntersectionObserver" in window)) return;
  const sections = navLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navLinks.forEach((link) => {
        link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`);
      });
    });
  }, { rootMargin: "-35% 0px -55% 0px", threshold: 0.01 });

  sections.forEach((section) => observer.observe(section));
}

async function fileExists(path) {
  try {
    const response = await fetch(path, { method: "HEAD", cache: "no-store" });
    return response.ok;
  } catch {
    return false;
  }
}

async function setupVideo() {
  if (!video || !videoPlaceholder) return;

  const srcEl = video.querySelector && video.querySelector("source");
  const src = srcEl && srcEl.getAttribute("src");
  function showVideo() {
    video.hidden = false;
    videoPlaceholder.hidden = true;
  }
  function showPlaceholder() {
    video.hidden = true;
    videoPlaceholder.hidden = false;
  }

  if (!src) {
    showPlaceholder();
    return;
  }

  // Try a quick HEAD check when possible, then attempt to load the media.
  try {
    const exists = await fileExists(src);
    if (!exists) {
      showPlaceholder();
      return;
    }
  } catch {
    // ignore network errors and attempt to load — fallback handled by events below
  }

  let settled = false;
  const onLoaded = () => {
    if (settled) return;
    settled = true;
    showVideo();
    cleanup();
  };
  const onError = () => {
    if (settled) return;
    settled = true;
    showPlaceholder();
    cleanup();
  };
  const cleanup = () => {
    video.removeEventListener("loadedmetadata", onLoaded);
    video.removeEventListener("error", onError);
  };

  video.addEventListener("loadedmetadata", onLoaded);
  video.addEventListener("error", onError);

  // Start loading the video. If metadata arrives we show it, otherwise fall back after timeout.
  try {
    video.load();
    // Optimistically show the video (better UX when the file is present locally).
    showVideo();
  } catch {
    onError();
    return;
  }

  // Safety timeout: if neither loaded nor errored, check readyState then decide.
  setTimeout(() => {
    if (settled) return;
    if (video.readyState > 0) onLoaded();
    else onError();
  }, 2000);
}

if (video) {
  video.addEventListener("loadedmetadata", () => {
    if (videoFrame && video.videoHeight > video.videoWidth) {
      videoFrame.classList.add("portrait");
    }
  });
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function loadJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) return fallback;
    return await response.json();
  } catch {
    return fallback;
  }
}

function renderCertificates(items) {
  if (!certificateGrid) return;
  if (!items.length) {
    certificateGrid.innerHTML = '<div class="empty-state">No certificates have been added yet. Add PDF files under assets/certificates and run the sync script.</div>';
    return;
  }

  certificateGrid.innerHTML = items.map((item, index) => {
    const review = item.needsReview ? '<span class="review-flag">Needs title review</span>' : "";
    const source = item.source ? `<small>Auto-loaded from ${escapeHtml(item.source)}</small>` : "<small>Auto-loaded from certificate assets</small>";
    return `
      <article class="certificate-card reveal visible">
        <span class="cert-code">C${index + 1}</span>
        <div>
          <h3>${escapeHtml(item.title)}</h3>
          <small>${escapeHtml(item.type || "PDF")}</small>
          ${source}
          ${review}
        </div>
        <a href="${escapeHtml(item.file)}" target="_blank" rel="noopener">Open PDF</a>
      </article>
    `;
  }).join("");
}

let evidenceItems = [];

function renderEvidence(items, filter = "all") {
  if (!evidenceGrid) return;
  const visibleItems = filter === "all" ? items : items.filter((item) => item.category === filter);
  if (!visibleItems.length) {
    evidenceGrid.innerHTML = '<div class="empty-state">No evidence entries are available for this filter.</div>';
    return;
  }

  evidenceGrid.innerHTML = visibleItems.map((item) => `
    <figure class="evidence-card reveal visible" data-category="${escapeHtml(item.category)}">
      <img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.title)}" loading="lazy" />
      <figcaption>
        <span>${escapeHtml(item.group)}</span>
        <strong>${escapeHtml(item.title)}</strong>
        <p>${escapeHtml(item.caption)}</p>
      </figcaption>
    </figure>
  `).join("");
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter || "all";
    filterButtons.forEach((item) => item.classList.toggle("active", item === button));
    renderEvidence(evidenceItems, filter);
  });
});

setupReveal();
setupActiveNav();
setupVideo();
loadJson("certificates.json", []).then(renderCertificates);
loadJson("evidence.json", []).then((items) => {
  evidenceItems = Array.isArray(items) ? items : [];
  renderEvidence(evidenceItems);
});
