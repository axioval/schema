(() => {
  "use strict";

  const script = document.currentScript;
  const siteRoot = new URL("../../", script.src);
  const languageKey = "axioval.language";

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
