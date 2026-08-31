(() => {
  "use strict";

  const script = document.currentScript;
  const siteRoot = new URL("../../", script.src);
  const languageKey = "axioval.language";
  const navKey = "axioval.navigation-collapsed";

  function currentLanguage() {
    return document.documentElement.lang.toLowerCase().startsWith("de") ? "de" : "en";
  }

  function preferredLanguage() {
    const explicit = new URLSearchParams(location.search).get("lang");
    if (explicit === "de" || explicit === "en") {
      localStorage.setItem(languageKey, explicit);
      return explicit;
    }
    return localStorage.getItem(languageKey);
  }

  function routeInitialLanguage() {
    const rootPath = siteRoot.pathname.endsWith("/") ? siteRoot.pathname : `${siteRoot.pathname}/`;
    const onRoot = location.pathname === rootPath || location.pathname === `${rootPath}index.html`;
    const saved = preferredLanguage();
    const browser = (navigator.languages?.[0] || navigator.language || "en").toLowerCase();
    if (onRoot && currentLanguage() === "en" && (saved === "de" || (!saved && browser.startsWith("de")))) {
      location.replace(new URL(`de/${location.search}${location.hash}`, siteRoot));
    }
  }

  function iconFor(text) {
    const value = text.toLowerCase();
    const matches = [
      [/^home$|^start$/, "home"], [/meet axioval|kennenlernen/, "compass"],
      [/idea|idee/, "lightbulb"], [/building|baustein/, "shape"],
      [/wall|wand/, "wall"], [/make and share|erstellen und teilen/, "share"],
      [/location|ort/, "map-marker"], [/bundle|paket/, "package"],
      [/tool|werkzeug|technical|technik/, "tools"], [/fits together|zusammen/, "layers"],
      [/safe|sicher|trust|vertrau/, "shield-check"],
      [/reference|referenz/, "file-document"], [/project|projekt/, "source-repository"],
      [/contribut|mitarbeit/, "account-group"], [/change|änderung/, "file-document"],
      [/roadmap|ausblick/, "map-marker-path"], [/licen|lizenz/, "license"],
      [/not own|nicht.*gehört|deliberately not/, "close-circle"],
      [/own|gehört|checklist|checkliste|write|schreib|prüfung|check/, "check-circle"],
      [/why|warum/, "help-circle"], [/next|weiter|begin/, "arrow-right"],
      [/example|beispiel/, "file-document"],
    ];
    return matches.find(([pattern]) => pattern.test(value))?.[1] || "file-document";
  }

  function applyIcon(element, text) {
    element.style.setProperty("--axioval-icon", `url('${new URL(`assets/icons/${iconFor(text)}.svg`, siteRoot)}')`);
  }

  function decorateNavigation(sidebar) {
    sidebar.querySelectorAll(".md-ellipsis").forEach((label) => {
      if (label.querySelector(".nav-rail-icon")) return;
      const text = label.textContent.trim();
      const icon = document.createElement("span");
      icon.className = "nav-rail-icon";
      icon.setAttribute("aria-hidden", "true");
      applyIcon(icon, text);
      const words = document.createElement("span");
      words.className = "nav-rail-label";
      words.textContent = text;
      label.replaceChildren(icon, words);
      label.closest("a, label")?.setAttribute("aria-label", text);
      label.closest("a, label")?.setAttribute("title", text);
    });
  }

  function setNavigationState(collapsed, button) {
    document.body.classList.toggle("axioval-nav-collapsed", collapsed);
    button.setAttribute("aria-expanded", String(!collapsed));
    const german = currentLanguage() === "de";
    const label = collapsed
      ? (german ? "Navigation ausklappen" : "Expand navigation")
      : (german ? "Navigation einklappen" : "Collapse navigation");
    button.setAttribute("aria-label", label);
    button.title = label;
    button.textContent = collapsed ? "›" : "‹";
  }

  function initNavigation() {
    const sidebar = document.querySelector(".md-sidebar--primary");
    if (!sidebar) return;
    decorateNavigation(sidebar);
    const button = document.createElement("button");
    button.type = "button";
    button.className = "nav-rail-toggle";
    sidebar.prepend(button);
    let collapsed = localStorage.getItem(navKey) === "true";
    setNavigationState(collapsed, button);
    button.addEventListener("click", () => {
      collapsed = !collapsed;
      localStorage.setItem(navKey, String(collapsed));
      setNavigationState(collapsed, button);
    });
  }

  function decorateHeadings() {
    document.querySelectorAll(".md-content h1, .md-content h2").forEach((heading) => {
      if (heading.querySelector(".section-icon")) return;
      const icon = document.createElement("span");
      icon.className = "section-icon";
      icon.setAttribute("aria-hidden", "true");
      applyIcon(icon, heading.textContent);
      heading.prepend(icon);
    });
  }

  async function enhanceDiagram(image) {
    if (image.dataset.enhanced === "true" || !image.currentSrc.endsWith(".svg")) return;
    image.dataset.enhanced = "true";
    try {
      const url = new URL(image.currentSrc, location.href);
      if (url.origin !== location.origin || !url.pathname.includes("/assets/images/")) return;
      const response = await fetch(url);
      if (!response.ok) throw new Error(`SVG request failed: ${response.status}`);
      const documentSvg = new DOMParser().parseFromString(await response.text(), "image/svg+xml");
      const svg = documentSvg.documentElement;

      if (svg.localName !== "svg" || svg.querySelector("script, foreignObject")) {
        throw new Error("Unsafe SVG content");
      }
      for (const node of svg.querySelectorAll("[href]")) {
        const href = node.getAttribute("href");
        if (href && !href.startsWith("#")) throw new Error("External SVG reference");
      }
      svg.classList.add("axioval-diagram");
      svg.setAttribute("focusable", "false");
      const imported = document.importNode(svg, true);
      const target = image.parentElement?.tagName === "PICTURE" ? image.parentElement : image;
      target.replaceWith(imported);
    } catch (error) {
      image.dataset.enhanced = "false";
      console.warn("Axioval kept the static diagram fallback", error);
    }
  }

  function rememberLanguageChoice() {
    document.querySelectorAll("a[hreflang]").forEach((link) => {
      const language = link.getAttribute("hreflang")?.toLowerCase().split("-")[0];
      if (language === "de" || language === "en") {
        link.addEventListener("click", () => localStorage.setItem(languageKey, language));
      }
    });
  }

  function init() {
    initNavigation();
    decorateHeadings();
    rememberLanguageChoice();
    document.querySelectorAll(".diagram-frame img[src$='.svg']").forEach(enhanceDiagram);
  }

  routeInitialLanguage();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
