(() => {
  const STORAGE_KEY = "training-open-menu-modules";

  const readState = () => {
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      const parsed = value ? JSON.parse(value) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  };

  const writeState = (values) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(values));
    } catch {
      // ignore storage errors
    }
  };

  const setModuleOpen = (block, isOpen) => {
    const list = block.querySelector("[data-module-list]");
    const button = block.querySelector("[data-module-toggle]");
    const caretIcon = block.querySelector("[data-module-caret] i");

    if (!list || !button) return;

    list.classList.toggle("is-hidden", !isOpen);
    button.setAttribute("aria-expanded", isOpen ? "true" : "false");

    if (caretIcon) {
      caretIcon.className = isOpen ? "ph ph-caret-up" : "ph ph-caret-down";
    }
  };

  const syncModuleButtonState = (block, currentModule) => {
    const button = block.querySelector("[data-module-toggle]");
    const moduleIcon = block.querySelector("[data-module-icon] i");
    const slug = block.dataset.moduleBlock;

    if (!button) return;

    const isCurrentModule = slug === currentModule;

    button.classList.remove("is-link");
    button.classList.remove("is-light");

    if (isCurrentModule) {
      button.classList.add("is-link");
      button.classList.add("is-light");
    } else {
      button.classList.add("is-light");
    }

    if (moduleIcon) {
      moduleIcon.className = isCurrentModule
        ? "ph-fill ph-check-circle"
        : "ph ph-folder-open";
    }
  };

  const syncLinks = (sidebar, currentSlug, currentModule) => {
    const links = sidebar.querySelectorAll("[data-link-slug]");

    links.forEach((link) => {
      const linkSlug = link.dataset.linkSlug;
      const linkModule = link.dataset.linkModule;
      const kind = link.dataset.linkKind;
      const icon = link.querySelector("[data-link-icon] i");

      link.classList.remove("is-active");
      link.classList.remove("has-background-light");

      if (linkSlug === currentSlug) {
        link.classList.add("is-active");
        if (icon) icon.className = "ph-fill ph-check-circle";
        link.setAttribute("data-active-link", "true");
      } else {
        link.removeAttribute("data-active-link");

        if (kind === "overview" && linkModule === currentModule) {
          link.classList.add("has-background-light");
          if (icon) icon.className = "ph ph-book-open";
        } else if (kind === "overview") {
          if (icon) icon.className = "ph ph-book-open";
        } else {
          if (icon) icon.className = "ph ph-play-circle";
        }
      }
    });
  };

  const initShell = (shell) => {
    const sidebar = shell.querySelector("[data-training-sidebar]");
    if (!sidebar) return;

    const currentSlug = shell.dataset.currentSlug || "";
    const currentModule = shell.dataset.currentModule || "";
    const blocks = Array.from(sidebar.querySelectorAll("[data-module-block]"));
    const storedOpen = readState();

    blocks.forEach((block) => {
      const slug = block.dataset.moduleBlock;
      const toggle = block.querySelector("[data-module-toggle]");
      const shouldStartOpen = slug === currentModule || storedOpen.includes(slug);

      setModuleOpen(block, shouldStartOpen);
      syncModuleButtonState(block, currentModule);

      if (!toggle) return;

      toggle.addEventListener("click", () => {
        const list = block.querySelector("[data-module-list]");
        if (!list) return;

        const currentlyOpen = !list.classList.contains("is-hidden");
        const isCurrentModule = slug === currentModule;

        if (isCurrentModule && currentlyOpen) {
          setModuleOpen(block, true);
          return;
        }

        setModuleOpen(block, !currentlyOpen);

        const openSlugs = blocks
          .filter((item) => {
            const moduleList = item.querySelector("[data-module-list]");
            return moduleList && !moduleList.classList.contains("is-hidden");
          })
          .map((item) => item.dataset.moduleBlock)
          .filter(Boolean);

        writeState(openSlugs);
      });
    });

    syncLinks(sidebar, currentSlug, currentModule);

    const activeLink = sidebar.querySelector("[data-active-link='true']");
    if (activeLink) {
      requestAnimationFrame(() => {
        activeLink.scrollIntoView({
          block: "nearest",
          inline: "nearest",
        });
      });
    }
  };

  const boot = () => {
    document.querySelectorAll("[data-training-shell]").forEach(initShell);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();