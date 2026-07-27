/* @ds-bundle: {"format":4,"namespace":"NamasteUIDesignSystem_e97b71","components":[{"name":"AvatarRing","sourcePath":"components/core/AvatarRing.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Chip","sourcePath":"components/core/Chip.jsx"},{"name":"CodeBlock","sourcePath":"components/core/CodeBlock.jsx"},{"name":"CodePanel","sourcePath":"components/core/CodePanel.jsx"},{"name":"Footer","sourcePath":"components/core/Footer.jsx"},{"name":"Hero","sourcePath":"components/core/Hero.jsx"},{"name":"Input","sourcePath":"components/core/Input.jsx"},{"name":"Kicker","sourcePath":"components/core/Kicker.jsx"},{"name":"Logo","sourcePath":"components/core/Logo.jsx"},{"name":"Navbar","sourcePath":"components/core/Navbar.jsx"},{"name":"TableOfContents","sourcePath":"components/core/TableOfContents.jsx"},{"name":"TimelineStepper","sourcePath":"components/core/TimelineStepper.jsx"},{"name":"AdSlot","sourcePath":"components/course/AdSlot.jsx"},{"name":"AuthorBox","sourcePath":"components/course/AuthorBox.jsx"},{"name":"BlogCard","sourcePath":"components/course/BlogCard.jsx"},{"name":"CourseCard","sourcePath":"components/course/CourseCard.jsx"},{"name":"CourseStats","sourcePath":"components/course/CourseStats.jsx"},{"name":"CurriculumList","sourcePath":"components/course/CurriculumList.jsx"},{"name":"LevelBadge","sourcePath":"components/course/LevelBadge.jsx"},{"name":"ResourceCard","sourcePath":"components/course/ResourceCard.jsx"},{"name":"RoadmapCard","sourcePath":"components/course/RoadmapCard.jsx"},{"name":"TrainingCard","sourcePath":"components/course/TrainingCard.jsx"},{"name":"VideoPoster","sourcePath":"components/course/VideoPoster.jsx"}],"sourceHashes":{"components/core/AvatarRing.jsx":"b9b165c92c64","components/core/Badge.jsx":"9f75a63366ec","components/core/Button.jsx":"5e48f59f4675","components/core/Chip.jsx":"e30ffa8fd331","components/core/CodeBlock.jsx":"f07f61886202","components/core/CodePanel.jsx":"fc31d5d72043","components/core/Footer.jsx":"72203483a2a8","components/core/Hero.jsx":"c6c3fb43142a","components/core/Input.jsx":"3e1c7d5992bc","components/core/Kicker.jsx":"330487987fbb","components/core/Logo.jsx":"c5e5d1acbf14","components/core/Navbar.jsx":"ab241a8ef436","components/core/TableOfContents.jsx":"745302859ef7","components/core/TimelineStepper.jsx":"4774cb80c614","components/course/AdSlot.jsx":"36692d75255e","components/course/AuthorBox.jsx":"7954eb76f05f","components/course/BlogCard.jsx":"d527c8c8c330","components/course/CourseCard.jsx":"77b2d2580f52","components/course/CourseStats.jsx":"ff1fcc25f763","components/course/CurriculumList.jsx":"99529da45637","components/course/LevelBadge.jsx":"b9e2289c169d","components/course/ResourceCard.jsx":"a886a7b3e741","components/course/RoadmapCard.jsx":"1463b980c021","components/course/TrainingCard.jsx":"ac284212d2c3","components/course/VideoPoster.jsx":"19af59640c15","ui_kits/lms/App.jsx":"f079c79a1e34","ui_kits/lms/BlogScreen.jsx":"2e04a605eee4","ui_kits/lms/CourseDetailScreen.jsx":"358ec01a5d7e","ui_kits/lms/CoursesScreen.jsx":"6db5170457c6","ui_kits/lms/DocsScreen.jsx":"f479ff349cca","ui_kits/lms/HomeScreen.jsx":"7471b949c319","ui_kits/lms/Nav.jsx":"114c162650a4","ui_kits/lms/PlayerScreen.jsx":"82081e63beb3","ui_kits/lms/ResourcesScreen.jsx":"df809f56e9d5","ui_kits/lms/TrainingScreen.jsx":"414cb233af38"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.NamasteUIDesignSystem_e97b71 = window.NamasteUIDesignSystem_e97b71 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/AvatarRing.jsx
try { (() => {
/** Avatar with a thin hairline brand ring (offset, not a solid color wrap) — precise, not decorative. */
function AvatarRing({
  src,
  alt = "",
  size = 40
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      position: "relative",
      width: size,
      height: size
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: alt,
    style: {
      width: size,
      height: size,
      borderRadius: "9999px",
      display: "block",
      objectFit: "cover"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      inset: -3,
      borderRadius: "9999px",
      boxShadow: "0 0 0 1.5px var(--color-brand-500)"
    }
  }));
}
Object.assign(__ds_scope, { AvatarRing });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/AvatarRing.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
/* Principle: status reads as a bordered mono tag with a dot, not a solid
   pastel-tint pill — the same information, told through a status dot + text
   color instead of a background wash, so a row of badges reads like a status
   line in a build log rather than a marketing chip. */
const colors = {
  default: "var(--color-brand-500)",
  accent: "var(--color-accent-500)",
  success: "var(--color-success)",
  warning: "var(--color-warning)",
  error: "var(--color-error)"
};
function Badge({
  children,
  variant = "default",
  icon,
  dot = true
}) {
  const c = colors[variant] || colors.default;
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.4rem",
      borderRadius: "var(--radius-sm)",
      padding: "0.2rem 0.55rem",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: "var(--color-ink)",
      boxShadow: "inset 0 0 0 1px var(--color-border)"
    }
  }, icon ? /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`,
    style: {
      color: c,
      fontSize: "0.9rem"
    }
  }) : dot && /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: 9999,
      background: c,
      flexShrink: 0
    }
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
/* Principle: no spring/bounce — press states are instant border/opacity
   shifts, never a translateY bounce. Radius is --radius-btn (sharp), not a
   pill; pill shape is reserved for tags. Primary is the only variant with a
   solid brand fill — everything else is a hairline border, so the one solid
   button on a screen reads as the one thing to click. */
const sizes = {
  sm: {
    padding: "0.4rem 0.85rem",
    fontSize: "0.8125rem"
  },
  md: {
    padding: "0.6rem 1.25rem",
    fontSize: "0.9rem"
  },
  lg: {
    padding: "0.75rem 1.5rem",
    fontSize: "1rem"
  }
};
const variants = {
  primary: {
    color: "#fff",
    background: "var(--color-brand-500)",
    border: "1px solid var(--color-brand-500)"
  },
  accent: {
    color: "#fff",
    background: "var(--color-accent-600)",
    border: "1px solid var(--color-accent-600)"
  },
  outline: {
    color: "var(--color-ink)",
    background: "transparent",
    border: "1px solid var(--color-border)"
  },
  white: {
    color: "var(--color-brand-800)",
    background: "#fff",
    border: "1px solid #fff"
  },
  ghost: {
    color: "#fff",
    background: "transparent",
    border: "1px solid rgb(255 255 255 / 0.3)"
  }
};
const hoverStyle = {
  primary: {
    background: "var(--color-brand-600)",
    borderColor: "var(--color-brand-600)"
  },
  accent: {
    background: "var(--color-accent-700)",
    borderColor: "var(--color-accent-700)"
  },
  outline: {
    borderColor: "var(--color-brand-500)",
    color: "var(--color-brand-600)"
  },
  white: {
    background: "var(--color-brand-50)"
  },
  ghost: {
    background: "rgb(255 255 255 / 0.1)",
    borderColor: "rgb(255 255 255 / 0.5)"
  }
};

/** Namaste UI's action button — sharp corners, hairline border by default, solid fill reserved for `primary`. Press is instant (no bounce, no lift). */
function Button({
  variant = "primary",
  size = "md",
  icon,
  iconPosition = "left",
  disabled,
  children,
  onClick,
  style
}) {
  const [hover, setHover] = React.useState(false);
  const [active, setActive] = React.useState(false);
  const v = variants[variant] || variants.primary;
  const s = sizes[size] || sizes.md;
  const hv = hover && !disabled ? hoverStyle[variant] : {};
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    disabled: disabled,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setActive(false);
    },
    onMouseDown: () => setActive(true),
    onMouseUp: () => setActive(false),
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      gap: "0.5rem",
      borderRadius: "var(--radius-btn)",
      fontWeight: 700,
      fontFamily: "var(--font-sans)",
      cursor: disabled ? "not-allowed" : "pointer",
      opacity: disabled ? 0.45 : active ? 0.85 : 1,
      transition: `background-color var(--duration-fast) var(--ease-out), border-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out), opacity var(--duration-fast) linear`,
      ...s,
      ...v,
      ...hv,
      ...style
    }
  }, icon && iconPosition === "left" && /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`,
    "aria-hidden": "true"
  }), children, icon && iconPosition === "right" && /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`,
    "aria-hidden": "true"
  }));
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Chip.jsx
try { (() => {
/** Icon tile — sharp radius, hairline border, quiet tint. No soft glow. */
function Chip({
  icon,
  variant = "brand",
  size = 40
}) {
  const isAccent = variant === "accent";
  const color = isAccent ? "var(--color-accent-500)" : "var(--color-brand-500)";
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      height: size,
      width: size,
      borderRadius: "var(--radius-sm)",
      fontSize: size * 0.42,
      color,
      background: "color-mix(in srgb, " + color + " 8%, transparent)",
      boxShadow: "inset 0 0 0 1px color-mix(in srgb, " + color + " 30%, transparent)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`,
    "aria-hidden": "true"
  }));
}
Object.assign(__ds_scope, { Chip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Chip.jsx", error: String((e && e.message) || e) }); }

// components/core/CodeBlock.jsx
try { (() => {
/* Formalizes the theme's own .ns-code motif: a navy console bar with a mono
   filename tab + copy button, flush white/surface code area, all-blue token
   palette (never a rainbow highlighter) — matches prompt.md's brand voice. */
const RULES = [[/(\/\/.*$)/gm, "var(--color-muted)", "italic"], [/\b(public|private|static|class|return|if|else|for|while|new|trigger|on|insert|update|delete|SELECT|FROM|WHERE|GROUP BY)\b/g, "var(--color-brand-600)", "700"], [/'([^']*)'/g, "var(--color-brand-500)", "400"]];
function highlight(code) {
  let html = code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  RULES.forEach(([re, color, weight]) => {
    html = html.replace(re, m => `<span style="color:${color};font-weight:${weight}">${m}</span>`);
  });
  return html;
}
function CodeBlock({
  code,
  filename = "apex",
  copyable = true
}) {
  const [copied, setCopied] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      boxShadow: "inset 0 0 0 1px var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--color-brand-900)",
      padding: "0.5rem 0.75rem 0",
      display: "flex",
      alignItems: "flex-end",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      background: "var(--color-surface)",
      color: "var(--color-brand-600)",
      fontFamily: "var(--font-mono)",
      fontSize: "0.72rem",
      fontWeight: 700,
      borderRadius: "4px 4px 0 0",
      padding: "0.4rem 0.75rem"
    }
  }, filename), copyable && /*#__PURE__*/React.createElement("button", {
    onClick: () => {
      navigator.clipboard?.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    },
    style: {
      all: "unset",
      cursor: "pointer",
      marginBottom: 6,
      fontFamily: "var(--font-mono)",
      fontSize: "0.7rem",
      fontWeight: 700,
      color: copied ? "#9ee8b0" : "rgb(255 255 255 / 0.75)",
      padding: "0.3rem 0.5rem"
    }
  }, copied ? "COPIED" : "COPY")), /*#__PURE__*/React.createElement("pre", {
    style: {
      margin: 0,
      background: "var(--color-surface)",
      padding: "1rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.85rem",
      lineHeight: 1.6,
      color: "var(--color-ink)",
      overflowX: "auto"
    }
  }, /*#__PURE__*/React.createElement("code", {
    dangerouslySetInnerHTML: {
      __html: highlight(code)
    }
  })));
}
Object.assign(__ds_scope, { CodeBlock });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/CodeBlock.jsx", error: String((e && e.message) || e) }); }

// components/core/CodePanel.jsx
try { (() => {
/* SLDS-flavored code panel: a proper multi-token syntax highlighter (keywords,
   strings, comments, numbers, functions) with an in-panel light/dark toggle.
   Unlike CodeBlock (the restrained all-blue inline motif), this is the full
   developer-console treatment for docs and lesson code — the palette is tuned
   to read cleanly on both a navy SLDS background and a white one. */

const THEMES = {
  dark: {
    bg: "var(--color-brand-900)",
    barBg: "#001127",
    text: "#e6eefc",
    keyword: "#78b0ff",
    string: "#7ce3b0",
    comment: "#6f89a8",
    number: "#f6a4c0",
    func: "#ffd479",
    punct: "#b8c7dc",
    tab: "rgba(255,255,255,0.08)",
    tabText: "#cfe0f7",
    lineNo: "rgba(255,255,255,0.28)"
  },
  light: {
    bg: "#ffffff",
    barBg: "var(--color-surface-sunken)",
    text: "#0b1b34",
    keyword: "#0b5cab",
    string: "#0a7d4f",
    comment: "#6b7a90",
    number: "#b02a6f",
    func: "#9a5b00",
    punct: "#46546b",
    tab: "var(--color-brand-50, #eef4fc)",
    tabText: "var(--color-brand-700)",
    lineNo: "rgba(0,0,30,0.26)"
  }
};
const KEYWORDS = /\b(public|private|protected|global|static|final|virtual|abstract|override|class|interface|extends|implements|return|if|else|for|while|do|switch|case|break|continue|new|this|super|try|catch|finally|throw|void|null|true|false|const|var|let|function|import|export|trigger|on|insert|update|upsert|delete|undelete|SELECT|FROM|WHERE|LIMIT|ORDER\s+BY|GROUP\s+BY|with|sharing|without)\b/g;
function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function highlight(code, t) {
  const store = [];
  const stash = html => {
    store.push(html);
    return `\u0000${store.length - 1}\u0000`;
  };
  let s = escapeHtml(code);
  // comments (line + block) and strings first — protected from keyword matching
  s = s.replace(/(\/\/[^\n]*|\/\*[\s\S]*?\*\/)/g, m => stash(`<span style="color:${t.comment};font-style:italic">${m}</span>`));
  s = s.replace(/('[^']*'|"[^"]*")/g, m => stash(`<span style="color:${t.string}">${m}</span>`));
  // numbers
  s = s.replace(/\b(\d+\.?\d*)\b/g, m => `<span style="color:${t.number}">${m}</span>`);
  // function calls
  s = s.replace(/\b([A-Za-z_]\w*)(\s*\()/g, (m, name, paren) => `<span style="color:${t.func}">${name}</span>${paren}`);
  // keywords
  s = s.replace(KEYWORDS, m => `<span style="color:${t.keyword};font-weight:700">${m}</span>`);
  // restore protected spans
  s = s.replace(/\u0000(\d+)\u0000/g, (_, i) => store[+i]);
  return s;
}
function CodePanel({
  code = "",
  filename = "apex",
  language,
  copyable = true,
  defaultTheme = "dark",
  showLineNumbers = true
}) {
  const [theme, setTheme] = React.useState(defaultTheme === "light" ? "light" : "dark");
  const [copied, setCopied] = React.useState(false);
  const t = THEMES[theme];
  const lines = code.replace(/\n$/, "").split("\n");
  const gutterW = String(lines.length).length;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      fontFamily: "var(--font-mono)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: t.barBg,
      padding: "0.5rem 0.65rem 0",
      display: "flex",
      alignItems: "flex-end",
      justifyContent: "space-between",
      gap: "0.5rem"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      background: t.bg,
      color: t.tabText,
      fontSize: "0.72rem",
      fontWeight: 700,
      borderRadius: "5px 5px 0 0",
      padding: "0.4rem 0.8rem",
      boxShadow: theme === "light" ? "inset 0 0 0 1px var(--color-border)" : "none",
      borderBottom: "none"
    }
  }, filename), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "0.25rem",
      marginBottom: 6
    }
  }, language && /*#__PURE__*/React.createElement("span", {
    style: {
      color: t.lineNo,
      fontSize: "0.66rem",
      fontWeight: 700,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      padding: "0 0.4rem"
    }
  }, language), /*#__PURE__*/React.createElement("button", {
    onClick: () => setTheme(theme === "dark" ? "light" : "dark"),
    "aria-label": "Toggle code theme",
    title: "Toggle light / dark",
    style: {
      all: "unset",
      cursor: "pointer",
      display: "inline-flex",
      alignItems: "center",
      gap: "0.3rem",
      height: 22,
      padding: "0 0.5rem",
      borderRadius: 4,
      fontSize: "0.66rem",
      fontWeight: 700,
      letterSpacing: "0.06em",
      color: t.tabText,
      boxShadow: `inset 0 0 0 1px ${theme === "dark" ? "rgba(255,255,255,0.18)" : "var(--color-border)"}`
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ph ph-lightbulb",
    style: {
      fontSize: "0.8rem"
    }
  }), theme === "dark" ? "LIGHT" : "DARK"), copyable && /*#__PURE__*/React.createElement("button", {
    onClick: () => {
      navigator.clipboard?.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    },
    style: {
      all: "unset",
      cursor: "pointer",
      display: "inline-flex",
      alignItems: "center",
      gap: "0.3rem",
      height: 22,
      padding: "0 0.5rem",
      borderRadius: 4,
      fontSize: "0.68rem",
      fontWeight: 700,
      color: copied ? theme === "dark" ? "#9ee8b0" : "#0a7d4f" : t.tabText,
      boxShadow: `inset 0 0 0 1px ${theme === "dark" ? "rgba(255,255,255,0.18)" : "var(--color-border)"}`
    }
  }, copied && /*#__PURE__*/React.createElement("i", {
    className: "ph ph-check-circle",
    style: {
      fontSize: "0.8rem"
    }
  }), copied ? "COPIED" : "COPY"))), /*#__PURE__*/React.createElement("div", {
    style: {
      background: t.bg,
      display: "flex",
      overflowX: "auto"
    }
  }, showLineNumbers && /*#__PURE__*/React.createElement("pre", {
    "aria-hidden": "true",
    style: {
      margin: 0,
      padding: "1rem 0.5rem 1rem 0.9rem",
      textAlign: "right",
      color: t.lineNo,
      fontSize: "0.82rem",
      lineHeight: 1.6,
      userSelect: "none",
      background: theme === "dark" ? "rgba(0,0,0,0.18)" : "rgba(0,0,30,0.03)",
      minWidth: `${gutterW + 1}ch`
    }
  }, lines.map((_, i) => `${i + 1}\n`).join("")), /*#__PURE__*/React.createElement("pre", {
    style: {
      margin: 0,
      padding: "1rem 1.1rem",
      fontSize: "0.82rem",
      lineHeight: 1.6,
      color: t.text,
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("code", {
    dangerouslySetInnerHTML: {
      __html: highlight(code, t)
    }
  }))));
}
Object.assign(__ds_scope, { CodePanel });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/CodePanel.jsx", error: String((e && e.message) || e) }); }

// components/core/Hero.jsx
try { (() => {
/* Principle: reuse the hairline-grid dark canvas everywhere a hero appears —
   course, blog, docs, resources all share this one hero language, only the
   content composition changes (matches the source's own data-hero 1–5). */
function Hero({
  variant = "split",
  kicker,
  title,
  subtitle,
  media,
  stats,
  actions
}) {
  const isCentered = variant === "centered";
  const isCompact = variant === "compact";
  return /*#__PURE__*/React.createElement("section", {
    style: {
      position: "relative",
      overflow: "hidden",
      background: "var(--color-brand-900)",
      color: "#fff",
      padding: isCompact ? "2rem 1.5rem" : "4rem 1.5rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: "linear-gradient(to right, rgb(255 255 255 / 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgb(255 255 255 / 0.05) 1px, transparent 1px)",
      backgroundSize: "44px 44px",
      WebkitMaskImage: "radial-gradient(ellipse 100% 100% at 50% 20%, #000 20%, transparent 72%)",
      maskImage: "radial-gradient(ellipse 100% 100% at 50% 20%, #000 20%, transparent 72%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      maxWidth: 1120,
      margin: "0 auto",
      display: isCentered || isCompact || !media ? "block" : "grid",
      gridTemplateColumns: !isCentered && !isCompact && media ? "1.3fr 1fr" : undefined,
      gap: "3rem",
      alignItems: "center",
      textAlign: isCentered ? "center" : "left"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      alignItems: isCentered ? "center" : "flex-start",
      gap: "1rem",
      maxWidth: isCentered ? 720 : undefined,
      margin: isCentered ? "0 auto" : undefined
    }
  }, kicker && /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: "0.4em",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      letterSpacing: "var(--tracking-label)",
      textTransform: "uppercase"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: "rgb(255 255 255 / 0.4)"
    }
  }, "//"), kicker), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "var(--font-heading)",
      fontSize: isCompact ? "1.75rem" : "var(--size-display)",
      fontWeight: 800,
      lineHeight: 1.12
    }
  }, title), subtitle && /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "1.05rem",
      color: "rgb(255 255 255 / 0.72)",
      maxWidth: 560
    }
  }, subtitle), actions && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "0.75rem"
    }
  }, actions), stats && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "0.5rem",
      borderTop: "1px solid rgb(255 255 255 / 0.12)",
      paddingTop: "1.1rem"
    }
  }, stats)), !isCentered && !isCompact && media && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      aspectRatio: "4/3",
      borderRadius: "var(--radius-card)",
      background: "rgb(255 255 255 / 0.04)",
      boxShadow: "inset 0 0 0 1px rgb(255 255 255 / 0.14)"
    }
  }, media)));
}
Object.assign(__ds_scope, { Hero });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Hero.jsx", error: String((e && e.message) || e) }); }

// components/core/Input.jsx
try { (() => {
/** Sharp-radius text input with a command-palette hint slot on the right (⌘K-style), not just a plain pill. */
function Input({
  placeholder,
  icon,
  hint,
  type = "text",
  value,
  onChange,
  style
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      position: "relative",
      display: "block",
      width: "100%"
    }
  }, icon && /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`,
    "aria-hidden": "true",
    style: {
      position: "absolute",
      left: "0.9rem",
      top: "50%",
      transform: "translateY(-50%)",
      color: "var(--color-muted)"
    }
  }), /*#__PURE__*/React.createElement("input", {
    type: type,
    placeholder: placeholder,
    value: value,
    onChange: onChange,
    style: {
      width: "100%",
      boxSizing: "border-box",
      borderRadius: "var(--radius-btn)",
      border: "1px solid var(--color-border)",
      background: "var(--color-surface)",
      color: "var(--color-ink)",
      padding: `0.65rem ${hint ? "3.5rem" : "1rem"} 0.65rem ${icon ? "2.4rem" : "1rem"}`,
      fontSize: "0.9375rem",
      fontFamily: "var(--font-sans)",
      outline: "none",
      transition: "border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out)",
      ...style
    },
    onFocus: e => {
      e.target.style.borderColor = "var(--color-brand-500)";
      e.target.style.boxShadow = "var(--shadow-focus)";
    },
    onBlur: e => {
      e.target.style.borderColor = "var(--color-border)";
      e.target.style.boxShadow = "none";
    }
  }), hint && /*#__PURE__*/React.createElement("kbd", {
    style: {
      position: "absolute",
      right: "0.7rem",
      top: "50%",
      transform: "translateY(-50%)",
      fontFamily: "var(--font-mono)",
      fontSize: "0.7rem",
      color: "var(--color-muted)",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-sm)",
      padding: "0.15rem 0.4rem"
    }
  }, hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Input.jsx", error: String((e && e.message) || e) }); }

// components/core/Kicker.jsx
try { (() => {
/* Principle: kickers render as a code comment, not a pastel eyebrow pill —
   the theme's own content is full of Apex/SOQL comments, so this borrows that
   voice for section labels instead of inventing a decorative motif. */
function Kicker({
  children,
  align = "left",
  light = false
}) {
  const commentColor = light ? "rgb(255 255 255 / 0.4)" : "var(--color-muted)";
  const textColor = light ? "#fff" : "var(--color-ink)";
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      alignItems: "baseline",
      justifyContent: align === "center" ? "center" : "flex-start",
      gap: "0.4em",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: "var(--weight-label)",
      letterSpacing: "var(--tracking-label)",
      textTransform: "uppercase"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: commentColor
    }
  }, "//"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: textColor
    }
  }, children));
}
Object.assign(__ds_scope, { Kicker });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Kicker.jsx", error: String((e && e.message) || e) }); }

// components/core/Logo.jsx
try { (() => {
/** Responsive wordmark lockup — icon (favicon.svg) + text, or icon-only when compact. Never invent a pictorial mark beyond the source's own favicon asset. */
function Logo({
  iconSrc = "assets/logo/favicon.svg",
  text = "Namaste Salesforce",
  compact = false,
  light = false,
  size = 24
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.55rem",
      fontFamily: "var(--font-heading)",
      fontWeight: 800,
      fontSize: size * 0.66,
      color: light ? "#fff" : "var(--color-ink)",
      whiteSpace: "nowrap"
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: iconSrc,
    alt: "",
    style: {
      width: size,
      height: size,
      flexShrink: 0
    }
  }), !compact && /*#__PURE__*/React.createElement("span", null, text));
}
Object.assign(__ds_scope, { Logo });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Logo.jsx", error: String((e && e.message) || e) }); }

// components/core/Footer.jsx
try { (() => {
/** Site footer — logo, link columns, mono copyright line. Hairline top border, no dark band. */
function Footer({
  columns = [],
  socialIcons = []
}) {
  return /*#__PURE__*/React.createElement("footer", {
    style: {
      borderTop: "1px solid var(--color-border)",
      padding: "3rem 1.5rem 2rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto",
      display: "flex",
      flexWrap: "wrap",
      gap: "3rem",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "0.75rem",
      maxWidth: 260
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.Logo, null), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "0.85rem",
      color: "var(--color-muted)",
      lineHeight: 1.6
    }
  }, "An open-source Salesforce learning platform \u2014 courses, a training roadmap, and developer docs."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "0.6rem"
    }
  }, socialIcons.map(icon => /*#__PURE__*/React.createElement("span", {
    key: icon,
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: 30,
      height: 30,
      borderRadius: "var(--radius-sm)",
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      color: "var(--color-muted)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`
  }))))), columns.map(col => /*#__PURE__*/React.createElement("div", {
    key: col.title,
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "0.6rem",
      minWidth: 140
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      letterSpacing: "var(--tracking-label)",
      textTransform: "uppercase",
      color: "var(--color-label)"
    }
  }, col.title), col.links.map(l => /*#__PURE__*/React.createElement("a", {
    key: l,
    href: "#",
    style: {
      fontSize: "0.85rem",
      color: "var(--color-muted)",
      textDecoration: "none"
    }
  }, l))))), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "2.5rem auto 0",
      paddingTop: "1.25rem",
      borderTop: "1px solid var(--color-border)",
      fontFamily: "var(--font-mono)",
      fontSize: "0.72rem",
      color: "var(--color-label)"
    }
  }, "\xA9 ", new Date().getFullYear(), " Namaste Salesforce \u2014 MIT licensed, forked from Ghost Casper."));
}
Object.assign(__ds_scope, { Footer });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Footer.jsx", error: String((e && e.message) || e) }); }

// components/core/Navbar.jsx
try { (() => {
/** Site header — logo, nav links with active-state hairline underline, theme toggle, primary CTA. */
function Navbar({
  links = [],
  activeId,
  onNavigate,
  dark,
  onToggleDark,
  ctaLabel = "Sign up",
  onCta,
  logo
}) {
  return /*#__PURE__*/React.createElement("header", {
    style: {
      position: "sticky",
      top: 0,
      zIndex: 40,
      borderBottom: "1px solid var(--color-border)",
      background: "color-mix(in srgb, var(--color-surface) 94%, transparent)",
      backdropFilter: "blur(8px)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0.85rem 1.5rem",
      gap: "1.5rem"
    }
  }, logo, /*#__PURE__*/React.createElement("nav", {
    style: {
      display: "flex",
      gap: "0.35rem",
      flex: 1,
      justifyContent: "center",
      fontFamily: "var(--font-sans)"
    }
  }, links.map(l => /*#__PURE__*/React.createElement("button", {
    key: l.id,
    onClick: () => onNavigate?.(l.id),
    style: {
      all: "unset",
      cursor: "pointer",
      display: "inline-flex",
      alignItems: "center",
      gap: "0.4rem",
      padding: "0.4rem 0.75rem",
      borderRadius: "var(--radius-sm)",
      fontSize: "0.9rem",
      fontWeight: activeId === l.id ? 600 : 450,
      letterSpacing: "-0.005em",
      color: activeId === l.id ? "var(--color-brand-600)" : "var(--color-label)",
      background: activeId === l.id ? "color-mix(in srgb, var(--color-brand-500) 9%, transparent)" : "transparent"
    }
  }, l.icon && /*#__PURE__*/React.createElement("i", {
    className: `ph ${l.icon}`,
    style: {
      fontSize: "1rem",
      opacity: 0.8
    }
  }), l.label))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "0.5rem",
      alignItems: "center"
    }
  }, onToggleDark && /*#__PURE__*/React.createElement("button", {
    onClick: onToggleDark,
    "aria-label": "Toggle dark mode",
    style: {
      all: "unset",
      cursor: "pointer",
      display: "inline-flex",
      height: 32,
      alignItems: "center",
      justifyContent: "center",
      borderRadius: "var(--radius-sm)",
      padding: "0 0.55rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.65rem",
      fontWeight: 700,
      letterSpacing: "0.06em",
      color: "var(--color-label)",
      boxShadow: "inset 0 0 0 1px var(--color-border)"
    }
  }, dark ? "LIGHT" : "DARK"), /*#__PURE__*/React.createElement(__ds_scope.Button, {
    size: "sm",
    onClick: onCta
  }, ctaLabel))));
}
Object.assign(__ds_scope, { Navbar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Navbar.jsx", error: String((e && e.message) || e) }); }

// components/core/TableOfContents.jsx
try { (() => {
/** Scroll-spy table of contents — hairline left rail, active item gets a brand-blue left bar (mono index optional). */
function TableOfContents({
  items = [],
  activeId,
  onNavigate
}) {
  return /*#__PURE__*/React.createElement("nav", {
    "aria-label": "Table of contents",
    style: {
      display: "flex",
      flexDirection: "column",
      borderLeft: "1px solid var(--color-border)"
    }
  }, items.map(it => {
    const active = it.id === activeId;
    return /*#__PURE__*/React.createElement("a", {
      key: it.id,
      href: `#${it.id}`,
      onClick: e => {
        e.preventDefault();
        onNavigate?.(it.id);
      },
      style: {
        padding: it.level === 3 ? "0.35rem 0.9rem 0.35rem 1.6rem" : "0.35rem 0.9rem",
        marginLeft: -1,
        borderLeft: "2px solid " + (active ? "var(--color-brand-500)" : "transparent"),
        fontSize: it.level === 3 ? "0.78rem" : "0.85rem",
        fontWeight: active ? 700 : 500,
        color: active ? "var(--color-brand-600)" : "var(--color-muted)",
        textDecoration: "none"
      }
    }, it.label);
  }));
}
Object.assign(__ds_scope, { TableOfContents });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/TableOfContents.jsx", error: String((e && e.message) || e) }); }

// components/core/TimelineStepper.jsx
try { (() => {
/** Horizontal step progress — mono-numbered nodes on a connecting hairline, distinct from CurriculumList (lesson rows) and RoadmapCard (section stop). For course/lesson players and multi-step flows. */
function TimelineStepper({
  steps = [],
  activeIndex = 0
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-start"
    }
  }, steps.map((s, i) => {
    const done = i < activeIndex,
      active = i === activeIndex;
    return /*#__PURE__*/React.createElement(React.Fragment, {
      key: i
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "0.5rem",
        minWidth: 64
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        width: 28,
        height: 28,
        borderRadius: "9999px",
        fontFamily: "var(--font-mono)",
        fontSize: "0.7rem",
        fontWeight: 700,
        color: done || active ? "#fff" : "var(--color-muted)",
        background: done || active ? "var(--color-brand-500)" : "transparent",
        boxShadow: done || active ? "none" : "inset 0 0 0 1px var(--color-border)"
      }
    }, done ? /*#__PURE__*/React.createElement("i", {
      className: "ph ph-check-circle"
    }) : String(i + 1).padStart(2, "0")), /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: "0.7rem",
        fontWeight: active ? 700 : 500,
        color: active ? "var(--color-ink)" : "var(--color-muted)",
        textAlign: "center"
      }
    }, s)), i < steps.length - 1 && /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1,
        height: 2,
        marginTop: 13,
        background: i < activeIndex ? "var(--color-brand-500)" : "var(--color-border)"
      }
    }));
  }));
}
Object.assign(__ds_scope, { TimelineStepper });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/TimelineStepper.jsx", error: String((e && e.message) || e) }); }

// components/course/AdSlot.jsx
try { (() => {
/** Dashed placeholder ad slot — mono uppercase label, sharp corners. */
function AdSlot({
  label = "Advertise with us",
  height = 120
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      margin: "1.5rem 0"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      width: "100%",
      height,
      border: "1px dashed var(--color-border)",
      borderRadius: "var(--radius-sm)",
      background: "var(--color-surface-sunken)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.4rem",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color: "var(--color-label)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ph ph-megaphone",
    style: {
      fontFamily: "initial"
    }
  }), " ", label)));
}
Object.assign(__ds_scope, { AdSlot });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/AdSlot.jsx", error: String((e && e.message) || e) }); }

// components/course/AuthorBox.jsx
try { (() => {
/** Instructor byline — hairline card, mono "INSTRUCTOR" role tag instead of decorative framing. */
function AuthorBox({
  name,
  bio,
  avatar
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "1rem",
      alignItems: "flex-start",
      padding: "1.1rem 1.25rem",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-card)",
      background: "var(--color-surface-raised)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      position: "relative",
      flexShrink: 0,
      width: 44,
      height: 44
    }
  }, avatar ? /*#__PURE__*/React.createElement("img", {
    src: avatar,
    alt: name,
    style: {
      width: 44,
      height: 44,
      borderRadius: 9999,
      display: "block",
      objectFit: "cover"
    }
  }) : /*#__PURE__*/React.createElement("span", {
    style: {
      width: 44,
      height: 44,
      borderRadius: 9999,
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "var(--color-brand-600)",
      fontWeight: 700,
      fontFamily: "var(--font-mono)"
    }
  }, name?.[0]), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      inset: -3,
      borderRadius: "9999px",
      boxShadow: "0 0 0 1.5px var(--color-brand-500)"
    }
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "0.55rem"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 700,
      fontFamily: "var(--font-heading)"
    }
  }, name), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "0.6rem",
      fontWeight: 700,
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color: "var(--color-label)",
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      borderRadius: "var(--radius-sm)",
      padding: "0.1rem 0.35rem"
    }
  }, "Instructor")), /*#__PURE__*/React.createElement("p", {
    style: {
      marginTop: "0.35rem",
      fontSize: "0.9rem",
      color: "var(--color-muted)",
      lineHeight: 1.55
    }
  }, bio)));
}
Object.assign(__ds_scope, { AuthorBox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/AuthorBox.jsx", error: String((e && e.message) || e) }); }

// components/course/BlogCard.jsx
try { (() => {
/** Blog post collection card — same visual grammar as CourseCard (mono index, hover accent line) minus price/level; tag pill + author/date/read-time meta instead. */
function BlogCard({
  index,
  title,
  excerpt,
  image,
  tag,
  authorName,
  date,
  readTime,
  href = "#",
  onClick
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("a", {
    href: href,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      textDecoration: "none",
      color: "inherit",
      position: "relative",
      display: "flex",
      flexDirection: "column",
      height: "100%",
      overflow: "hidden",
      border: "1px solid " + (hover ? "var(--color-brand-500)" : "var(--color-border)"),
      borderRadius: "var(--radius-card)",
      background: "var(--color-surface-raised)",
      transition: "border-color var(--duration-base) var(--ease-out)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      height: 2,
      background: "var(--color-brand-500)",
      transform: hover ? "scaleX(1)" : "scaleX(0)",
      transformOrigin: "left",
      transition: "transform var(--duration-base) var(--ease-out)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      aspectRatio: "16/9",
      overflow: "hidden",
      background: "var(--color-surface-sunken)",
      borderBottom: "1px solid var(--color-border)"
    }
  }, image ? /*#__PURE__*/React.createElement("img", {
    src: image,
    alt: "",
    style: {
      height: "100%",
      width: "100%",
      objectFit: "cover"
    }
  }) : /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      height: "100%",
      width: "100%",
      alignItems: "center",
      justifyContent: "center",
      color: "var(--color-brand-300)",
      fontSize: "2.25rem"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ph ph-article"
  })), typeof index !== "undefined" && /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: "0.6rem",
      left: "0.6rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.7rem",
      fontWeight: 700,
      color: "#fff",
      background: "rgb(0 0 0 / 0.55)",
      borderRadius: "var(--radius-sm)",
      padding: "0.15rem 0.4rem"
    }
  }, String(index).padStart(2, "0"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flex: 1,
      flexDirection: "column",
      padding: "1rem",
      gap: "0.6rem"
    }
  }, tag && /*#__PURE__*/React.createElement("span", {
    style: {
      alignSelf: "flex-start",
      fontFamily: "var(--font-mono)",
      fontSize: "0.65rem",
      fontWeight: 700,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: "var(--color-brand-600)"
    }
  }, tag), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: "1.05rem",
      fontWeight: 700,
      lineHeight: 1.3,
      fontFamily: "var(--font-heading)"
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "0.875rem",
      color: "var(--color-muted)",
      display: "-webkit-box",
      WebkitLineClamp: 2,
      WebkitBoxOrient: "vertical",
      overflow: "hidden",
      margin: 0
    }
  }, excerpt), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "auto",
      paddingTop: "0.6rem",
      borderTop: "1px solid var(--color-border)",
      display: "flex",
      alignItems: "center",
      gap: "0.5rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.72rem",
      color: "var(--color-label)"
    }
  }, /*#__PURE__*/React.createElement("span", null, authorName), /*#__PURE__*/React.createElement("span", null, "\xB7"), /*#__PURE__*/React.createElement("span", null, date), /*#__PURE__*/React.createElement("span", null, "\xB7"), /*#__PURE__*/React.createElement("span", null, readTime))));
}
Object.assign(__ds_scope, { BlogCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/BlogCard.jsx", error: String((e && e.message) || e) }); }

// components/course/CourseCard.jsx
try { (() => {
/* Principle: data-forward. The card's corner carries a large mono index/
   duration readout — a spec-sheet number, not a hidden tooltip — and the
   whole card's hover state is a 1px top accent line + border brighten, never
   a shadow lift. This is the single most "console" component in the kit. */
function CourseCard({
  index,
  title,
  excerpt,
  image,
  level = "beginner",
  price = "free",
  priceLabel,
  lessons,
  duration,
  authorName,
  featured,
  sponsored,
  href = "#",
  onClick
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("a", {
    href: href,
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      textDecoration: "none",
      color: "inherit",
      position: "relative",
      display: "flex",
      flexDirection: "column",
      height: "100%",
      overflow: "hidden",
      border: "1px solid " + (hover ? "var(--color-brand-500)" : "var(--color-border)"),
      borderRadius: "var(--radius-card)",
      background: "var(--color-surface-raised)",
      transition: "border-color var(--duration-base) var(--ease-out)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      height: 2,
      background: "var(--color-brand-500)",
      transform: hover ? "scaleX(1)" : "scaleX(0)",
      transformOrigin: "left",
      transition: "transform var(--duration-base) var(--ease-out)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      aspectRatio: "16/9",
      overflow: "hidden",
      background: "var(--color-surface-sunken)",
      borderBottom: "1px solid var(--color-border)"
    }
  }, image ? /*#__PURE__*/React.createElement("img", {
    src: image,
    alt: "",
    style: {
      height: "100%",
      width: "100%",
      objectFit: "cover"
    }
  }) : /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      height: "100%",
      width: "100%",
      alignItems: "center",
      justifyContent: "center",
      color: "var(--color-brand-300)",
      fontSize: "2.25rem"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ph ph-graduation-cap"
  })), typeof index !== "undefined" && /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: "0.6rem",
      left: "0.6rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.7rem",
      fontWeight: 700,
      color: "#fff",
      background: "rgb(0 0 0 / 0.55)",
      borderRadius: "var(--radius-sm)",
      padding: "0.15rem 0.4rem",
      letterSpacing: "0.04em"
    }
  }, String(index).padStart(2, "0")), (featured || sponsored) && /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: "0.6rem",
      right: "0.6rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.65rem",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "0.06em",
      color: "#fff",
      background: sponsored ? "var(--color-brand-700)" : "var(--color-warning)",
      borderRadius: "var(--radius-sm)",
      padding: "0.15rem 0.45rem"
    }
  }, sponsored ? "Sponsored" : "Featured")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flex: 1,
      flexDirection: "column",
      padding: "1rem",
      gap: "0.6rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "0.5rem"
    }
  }, /*#__PURE__*/React.createElement(LevelBadgeInline, {
    level: level
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "auto",
      fontFamily: "var(--font-mono)",
      fontSize: "0.75rem",
      fontWeight: 700,
      color: price === "free" ? "var(--color-success)" : "var(--color-ink)"
    }
  }, priceLabel || (price === "free" ? "FREE" : "PAID"))), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: "1.05rem",
      fontWeight: 700,
      lineHeight: 1.3,
      fontFamily: "var(--font-heading)"
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "0.875rem",
      color: "var(--color-muted)",
      display: "-webkit-box",
      WebkitLineClamp: 2,
      WebkitBoxOrient: "vertical",
      overflow: "hidden",
      margin: 0
    }
  }, excerpt), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "0.9rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.72rem",
      color: "var(--color-label)",
      letterSpacing: "0.02em",
      borderTop: "1px solid var(--color-border)",
      paddingTop: "0.6rem"
    }
  }, typeof lessons !== "undefined" && /*#__PURE__*/React.createElement("span", null, String(lessons).padStart(2, "0"), " LESSONS"), duration && /*#__PURE__*/React.createElement("span", null, duration.toUpperCase())), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "auto",
      paddingTop: "0.4rem",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: "0.75rem"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "0.78rem",
      fontWeight: 600,
      color: "var(--color-muted)"
    }
  }, authorName), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: hover ? "0.5rem" : "0.3rem",
      fontSize: "0.8rem",
      fontWeight: 700,
      color: "var(--color-brand-600)",
      transition: "gap var(--duration-fast) var(--ease-out)"
    }
  }, "View ", /*#__PURE__*/React.createElement("i", {
    className: "ph ph-arrow-right"
  })))));
}
function LevelBadgeInline({
  level
}) {
  const map = {
    beginner: ["var(--color-success)", "Beginner"],
    intermediate: ["var(--color-warning)", "Intermediate"],
    advanced: ["var(--color-brand-500)", "Advanced"]
  };
  const [color, label] = map[level] || map.beginner;
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.35rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.65rem",
      fontWeight: 700,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: "var(--color-muted)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: 9999,
      background: color
    }
  }), label);
}
Object.assign(__ds_scope, { CourseCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/CourseCard.jsx", error: String((e && e.message) || e) }); }

// components/course/CourseStats.jsx
try { (() => {
/** Big tabular-mono stat readout — reads like a metrics panel, not a marketing counter. */
function CourseStats({
  stats = [],
  onDark = true
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: "0"
    }
  }, stats.map((s, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "0.2rem",
      padding: "0 1.5rem",
      borderLeft: i > 0 ? "1px solid " + (onDark ? "rgb(255 255 255 / 0.15)" : "var(--color-border)") : "none"
    }
  }, /*#__PURE__*/React.createElement("b", {
    style: {
      fontFamily: "var(--font-mono)",
      fontVariantNumeric: "tabular-nums",
      fontSize: "1.5rem",
      fontWeight: 700,
      lineHeight: 1,
      color: onDark ? "#fff" : "var(--color-ink)"
    }
  }, s.value), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "0.3rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.65rem",
      fontWeight: 700,
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color: onDark ? "rgb(255 255 255 / 0.55)" : "var(--color-label)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ph ${s.icon}`
  }), " ", s.label))));
}
Object.assign(__ds_scope, { CourseStats });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/CourseStats.jsx", error: String((e && e.message) || e) }); }

// components/course/CurriculumList.jsx
try { (() => {
/* Principle: terminal-row list. The index is a real mono tabular number
   (00, 01, 02…), hover is a left accent bar (not a background tint or lift),
   and every row prints its metadata in mono on the right — reads like `ls -l`
   for a course, not a stock "lesson card". */
function CurriculumList({
  items = [],
  variant = "list"
}) {
  const isCard = variant === "cards" || variant === "detailed";
  const wrap = isCard ? {
    display: "grid",
    gap: "0.6rem"
  } : {
    border: "1px solid var(--color-border)",
    borderRadius: "var(--radius-card)",
    overflow: "hidden",
    background: "var(--color-surface-raised)"
  };
  return /*#__PURE__*/React.createElement("div", {
    style: wrap
  }, items.map((it, i) => /*#__PURE__*/React.createElement(Row, {
    key: i,
    item: it,
    index: i,
    variant: variant,
    isLast: i === items.length - 1
  })));
}
function Row({
  item,
  index,
  variant,
  isLast
}) {
  const [hover, setHover] = React.useState(false);
  const isCard = variant === "cards" || variant === "detailed";
  const isTimeline = variant === "timeline";
  return /*#__PURE__*/React.createElement("div", {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      position: "relative",
      display: "flex",
      alignItems: isCard ? "flex-start" : "center",
      gap: "0.9rem",
      padding: "0.85rem 1rem",
      paddingLeft: isTimeline ? "2rem" : "1.35rem",
      borderBottom: !isCard && !isLast ? "1px solid var(--color-border)" : "none",
      border: isCard ? "1px solid " + (hover ? "var(--color-brand-500)" : "var(--color-border)") : "none",
      borderRadius: isCard ? "var(--radius-card)" : 0,
      background: isCard ? "var(--color-surface-raised)" : "transparent",
      transition: "border-color var(--duration-fast) var(--ease-out)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      left: 0,
      top: 0,
      bottom: 0,
      width: 2,
      background: "var(--color-brand-500)",
      transform: hover ? "scaleY(1)" : "scaleY(0)",
      transformOrigin: "top",
      transition: "transform var(--duration-fast) var(--ease-out)"
    }
  }), isTimeline && /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      left: 12,
      top: "50%",
      transform: "translateY(-50%)",
      width: 8,
      height: 8,
      borderRadius: 9999,
      background: item.done ? "var(--color-brand-500)" : "transparent",
      boxShadow: "0 0 0 1.5px " + (item.done ? "var(--color-brand-500)" : "var(--color-border)")
    }
  }), !isTimeline && /*#__PURE__*/React.createElement("span", {
    style: {
      flexShrink: 0,
      width: "1.8rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.85rem",
      fontWeight: 700,
      color: "var(--color-label)",
      fontVariantNumeric: "tabular-nums"
    }
  }, String(index).padStart(2, "0")), /*#__PURE__*/React.createElement("span", {
    style: {
      flexShrink: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      height: variant === "detailed" ? "4rem" : "2.1rem",
      width: variant === "detailed" ? "6.5rem" : "2.1rem",
      borderRadius: "var(--radius-sm)",
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      color: "var(--color-brand-500)",
      fontSize: variant === "detailed" ? "1.5rem" : "1rem"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ph ${item.icon || (item.type === "video" ? "ph-play" : item.type === "quiz" ? "ph-exam" : item.type === "exercise" ? "ph-barbell" : "ph-file-text")}`
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      minWidth: 0,
      flex: 1,
      display: "flex",
      flexDirection: "column"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 600
    }
  }, item.title), (variant === "cards" || variant === "detailed") && item.type && /*#__PURE__*/React.createElement("span", {
    style: {
      marginTop: 2,
      fontFamily: "var(--font-mono)",
      fontSize: "0.65rem",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "0.08em",
      color: "var(--color-label)"
    }
  }, item.type), variant === "detailed" && item.desc && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "0.8125rem",
      color: "var(--color-muted)",
      marginTop: 3
    }
  }, item.desc)), /*#__PURE__*/React.createElement("span", {
    style: {
      flexShrink: 0,
      display: "flex",
      alignItems: "center",
      gap: "0.6rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.72rem",
      color: "var(--color-label)"
    }
  }, item.duration && /*#__PURE__*/React.createElement("span", null, item.duration.toUpperCase()), item.locked ? /*#__PURE__*/React.createElement("i", {
    className: "ph ph-lock-simple",
    style: {
      color: "var(--color-muted)",
      fontFamily: "initial"
    }
  }) : item.preview && /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--color-brand-600)",
      fontWeight: 700
    }
  }, "PREVIEW")));
}
Object.assign(__ds_scope, { CurriculumList });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/CurriculumList.jsx", error: String((e && e.message) || e) }); }

// components/course/LevelBadge.jsx
try { (() => {
/** Difficulty as a mono status tag with a color dot — matches Badge's language exactly. */
function LevelBadge({
  level = "beginner"
}) {
  const map = {
    beginner: ["var(--color-success)", "Beginner"],
    intermediate: ["var(--color-warning)", "Intermediate"],
    advanced: ["var(--color-brand-500)", "Advanced"]
  };
  const [color, label] = map[level] || map.beginner;
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: "0.4rem",
      borderRadius: "var(--radius-sm)",
      padding: "0.2rem 0.55rem",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: "var(--color-ink)",
      boxShadow: "inset 0 0 0 1px var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: 9999,
      background: color,
      flexShrink: 0
    }
  }), label);
}
Object.assign(__ds_scope, { LevelBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/LevelBadge.jsx", error: String((e && e.message) || e) }); }

// components/course/ResourceCard.jsx
try { (() => {
/** Downloadable/external resource card — icon, type tag, title, external-link cue. For a /resources/ page (cheat sheets, templates, tools). */
function ResourceCard({
  title,
  type = "PDF",
  icon = "ph-file-text",
  href = "#"
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("a", {
    href: href,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      textDecoration: "none",
      color: "inherit",
      display: "flex",
      alignItems: "center",
      gap: "0.9rem",
      padding: "1rem 1.1rem",
      border: "1px solid " + (hover ? "var(--color-brand-500)" : "var(--color-border)"),
      borderRadius: "var(--radius-card)",
      background: "var(--color-surface-raised)",
      transition: "border-color var(--duration-fast) var(--ease-out)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      flexShrink: 0,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      width: "2.75rem",
      height: "2.75rem",
      borderRadius: "var(--radius-sm)",
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      color: "var(--color-brand-500)",
      fontSize: "1.35rem"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1,
      minWidth: 0,
      display: "flex",
      flexDirection: "column"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 600
    }
  }, title), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "0.68rem",
      fontWeight: 700,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: "var(--color-label)"
    }
  }, type)), /*#__PURE__*/React.createElement("i", {
    className: "ph ph-arrow-up-right",
    style: {
      flexShrink: 0,
      color: hover ? "var(--color-brand-600)" : "var(--color-muted)",
      fontSize: "1.1rem"
    }
  }));
}
Object.assign(__ds_scope, { ResourceCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/ResourceCard.jsx", error: String((e && e.message) || e) }); }

// components/course/RoadmapCard.jsx
try { (() => {
/** Roadmap stop — mono index tile, hairline border, left accent bar on hover (no lift/shadow). */
function RoadmapCard({
  n,
  title,
  desc,
  icon = "ph-flag",
  duration,
  lessons,
  side = "left",
  href = "#"
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      maxWidth: 420,
      marginLeft: side === "right" ? "auto" : 0
    }
  }, /*#__PURE__*/React.createElement("a", {
    href: href,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      position: "relative",
      display: "flex",
      gap: "1.1rem",
      padding: "1.1rem 1.25rem",
      textDecoration: "none",
      minHeight: "9rem",
      border: "1px solid " + (hover ? "var(--color-brand-500)" : "var(--color-border)"),
      borderRadius: "var(--radius-card)",
      background: "var(--color-surface-raised)",
      color: "inherit",
      transition: "border-color var(--duration-fast) var(--ease-out)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      left: 0,
      top: 0,
      bottom: 0,
      width: 2,
      background: "var(--color-brand-500)",
      transform: hover ? "scaleY(1)" : "scaleY(0)",
      transformOrigin: "top",
      transition: "transform var(--duration-fast) var(--ease-out)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      flex: "none",
      width: "3.25rem",
      alignSelf: "flex-start",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: "0.5rem"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "0.7rem",
      fontWeight: 700,
      color: "var(--color-label)"
    }
  }, String(n).padStart(2, "0")), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      width: "2.75rem",
      height: "2.75rem",
      borderRadius: "var(--radius-sm)",
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      color: "var(--color-brand-500)",
      fontSize: "1.35rem"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`
  }))), /*#__PURE__*/React.createElement("span", {
    style: {
      minWidth: 0,
      flex: 1,
      display: "flex",
      flexDirection: "column"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-heading)",
      fontSize: "1.1rem",
      fontWeight: 800,
      lineHeight: 1.25,
      color: "var(--color-ink)"
    }
  }, title), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "-webkit-box",
      WebkitLineClamp: 3,
      WebkitBoxOrient: "vertical",
      overflow: "hidden",
      marginTop: "0.35rem",
      fontSize: "0.85rem",
      lineHeight: 1.55,
      color: "var(--color-muted)"
    }
  }, desc), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      gap: "0.8rem",
      marginTop: "0.65rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.68rem",
      fontWeight: 700,
      color: "var(--color-label)"
    }
  }, typeof lessons !== "undefined" && /*#__PURE__*/React.createElement("span", null, String(lessons).padStart(2, "0"), " LESSONS"), duration && /*#__PURE__*/React.createElement("span", null, duration.toUpperCase())))));
}
Object.assign(__ds_scope, { RoadmapCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/RoadmapCard.jsx", error: String((e && e.message) || e) }); }

// components/course/TrainingCard.jsx
try { (() => {
/** Training-section collection card — for a /training/ overview grid (distinct from RoadmapCard, which is the spine-connected version used on the roadmap page itself). */
function TrainingCard({
  n,
  title,
  desc,
  icon = "ph-flag",
  lessons,
  duration,
  progress,
  href = "#"
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("a", {
    href: href,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      textDecoration: "none",
      color: "inherit",
      position: "relative",
      display: "flex",
      flexDirection: "column",
      gap: "0.75rem",
      padding: "1.25rem",
      border: "1px solid " + (hover ? "var(--color-brand-500)" : "var(--color-border)"),
      borderRadius: "var(--radius-card)",
      background: "var(--color-surface-raised)",
      transition: "border-color var(--duration-base) var(--ease-out)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      width: "2.75rem",
      height: "2.75rem",
      borderRadius: "var(--radius-sm)",
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      color: "var(--color-brand-500)",
      fontSize: "1.35rem"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ph ${icon}`
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "0.7rem",
      fontWeight: 700,
      color: "var(--color-label)"
    }
  }, String(n).padStart(2, "0"))), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 800,
      fontSize: "1.05rem"
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "0.85rem",
      color: "var(--color-muted)",
      lineHeight: 1.55,
      margin: 0
    }
  }, desc), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "0.8rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.68rem",
      fontWeight: 700,
      color: "var(--color-label)"
    }
  }, typeof lessons !== "undefined" && /*#__PURE__*/React.createElement("span", null, String(lessons).padStart(2, "0"), " LESSONS"), duration && /*#__PURE__*/React.createElement("span", null, duration.toUpperCase())), typeof progress === "number" && /*#__PURE__*/React.createElement("div", {
    style: {
      height: 3,
      borderRadius: 2,
      background: "var(--color-surface-sunken)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: "100%",
      width: `${progress}%`,
      background: "var(--color-brand-500)"
    }
  })));
}
Object.assign(__ds_scope, { TrainingCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/TrainingCard.jsx", error: String((e && e.message) || e) }); }

// components/course/VideoPoster.jsx
try { (() => {
/** 4:3 video poster — hairline ring play button (not a soft drop shadow), sharp corners. */
function VideoPoster({
  image,
  onPlay
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    onClick: onPlay,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      all: "unset",
      cursor: "pointer",
      position: "relative",
      display: "block",
      width: "100%",
      borderRadius: "var(--radius-card)",
      overflow: "hidden",
      boxShadow: "inset 0 0 0 1px var(--color-border)"
    }
  }, image ? /*#__PURE__*/React.createElement("img", {
    src: image,
    alt: "",
    style: {
      display: "block",
      width: "100%",
      aspectRatio: "4/3",
      objectFit: "cover",
      transform: hover ? "scale(1.03)" : "none",
      transition: "transform var(--duration-base) var(--ease-out)"
    }
  }) : /*#__PURE__*/React.createElement("div", {
    style: {
      width: "100%",
      aspectRatio: "4/3",
      background: "var(--color-brand-800)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      inset: 0,
      background: "linear-gradient(to top, rgb(0 0 0 / 0.5), transparent 55%)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      left: "1rem",
      bottom: "1rem",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      height: "3.25rem",
      width: "3.25rem",
      borderRadius: "9999px",
      background: "rgb(255 255 255 / 0.95)",
      color: "var(--color-brand-700)",
      fontSize: "1.2rem",
      boxShadow: hover ? "0 0 0 4px rgb(255 255 255 / 0.25)" : "0 0 0 0px rgb(255 255 255 / 0)",
      transition: "box-shadow var(--duration-base) var(--ease-out)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ph-fill ph-play"
  })));
}
Object.assign(__ds_scope, { VideoPoster });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/course/VideoPoster.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/App.jsx
try { (() => {
function App() {
  const [screen, setScreen] = window.React.useState("home");
  const [dark, setDark] = window.React.useState(false);
  window.React.useEffect(() => {
    document.documentElement.setAttribute("data-theme", dark ? "dark" : "light");
  }, [dark]);
  const Screen = {
    home: window.HomeScreen,
    courses: window.CoursesScreen,
    course: window.CourseDetailScreen,
    player: window.PlayerScreen,
    training: window.TrainingScreen,
    blog: window.BlogScreen,
    resources: window.ResourcesScreen,
    docs: window.DocsScreen
  }[screen];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      minHeight: "100vh",
      background: "var(--color-surface)"
    }
  }, /*#__PURE__*/React.createElement(window.Nav, {
    dark: dark,
    onToggleDark: () => setDark(d => !d),
    screen: screen,
    setScreen: setScreen
  }), /*#__PURE__*/React.createElement(Screen, {
    goCourse: () => setScreen("course")
  }));
}
window.App = App;
ReactDOM.createRoot(document.getElementById("root")).render(/*#__PURE__*/React.createElement(App, null));
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/App.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/BlogScreen.jsx
try { (() => {
const {
  Hero,
  BlogCard,
  Kicker
} = window.NamasteUIDesignSystem_e97b71;
const POSTS = [{
  title: "Why We Rebuilt the Training Roadmap",
  excerpt: "A look at the dashed-spine layout and why it beats a Netflix-style hover card that only reveals its blurb on hover.",
  tag: "Engineering",
  author: "Priya Sharma",
  date: "Jul 12",
  read: "6 min"
}, {
  title: "Flash-Free Dark Mode, Explained",
  excerpt: "How a pre-paint inline script and one data-theme attribute avoid the white flash entirely.",
  tag: "Engineering",
  author: "Namaste UI",
  date: "Jul 02",
  read: "4 min"
}, {
  title: "Grading Your First Trigger",
  excerpt: "A handler-pattern checklist for bulk-safety before you ship your first Apex trigger.",
  tag: "Apex",
  author: "Namaste UI",
  date: "Jun 24",
  read: "8 min"
}, {
  title: "Five Sections, One Trail",
  excerpt: "How the training roadmap's tag conventions keep five course sections in perfect order.",
  tag: "Product",
  author: "Priya Sharma",
  date: "Jun 10",
  read: "5 min"
}];
function BlogScreen() {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Hero, {
    variant: "compact",
    kicker: "Blog",
    title: "Notes on building & learning Salesforce"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1120,
      margin: "0 auto",
      padding: "2.5rem 1.5rem",
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill,minmax(260px,1fr))",
      gap: "1.25rem"
    }
  }, POSTS.map((p, i) => /*#__PURE__*/React.createElement(BlogCard, {
    key: p.title,
    index: i + 1,
    title: p.title,
    excerpt: p.excerpt,
    tag: p.tag,
    authorName: p.author,
    date: p.date,
    readTime: p.read
  }))));
}
window.BlogScreen = BlogScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/BlogScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/CourseDetailScreen.jsx
try { (() => {
const {
  Kicker,
  Button,
  LevelBadge,
  CourseStats,
  CurriculumList,
  AuthorBox,
  AdSlot
} = window.NamasteUIDesignSystem_e97b71;
const LESSONS = [{
  title: "What is Salesforce & the Ecosystem",
  type: "article",
  desc: "A plain-English tour of what Salesforce is, the products that make up the platform, and the roles in its ecosystem.",
  done: true
}, {
  title: "Editions, Orgs & Signing Up for a Dev Org",
  type: "article",
  desc: "Understand orgs and editions, then sign up for a free Developer Edition org.",
  preview: true
}, {
  title: "Navigating Lightning Experience",
  type: "article",
  desc: "The App Launcher, tabs, list views, record pages, and global search."
}, {
  title: "Objects, Records, Fields & Relationships",
  type: "article",
  desc: "The heart of the data model: objects as tables, records as rows, fields as columns."
}, {
  title: "Reports & Dashboards Basics",
  type: "article",
  desc: "Report types, filters, groupings, chart types, and assembling a dashboard."
}, {
  title: "Your First Automation with Flow",
  type: "exercise",
  desc: "Build your first no-code automation: triggers, elements, a record-triggered flow."
}, {
  title: "Where to Go Next: Admin, Dev, Architect",
  type: "quiz",
  desc: "Map the career paths — Admin, Developer, Architect — with a concrete next step."
}];
function CourseDetailScreen() {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("section", {
    style: {
      background: "var(--color-brand-900)",
      color: "#fff",
      padding: "3.5rem 1.5rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1120,
      margin: "0 auto",
      display: "grid",
      gridTemplateColumns: "1.3fr 1fr",
      gap: "3rem",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "1rem"
    }
  }, /*#__PURE__*/React.createElement(Kicker, {
    light: true
  }, "Zero to Hero / Foundations"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 800,
      fontSize: "2.25rem",
      lineHeight: 1.15
    }
  }, "Salesforce \u2014 Zero to Hero"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: "rgb(255 255 255 / 0.72)",
      fontSize: "1.05rem",
      lineHeight: 1.6
    }
  }, "Go from total beginner to job-ready Salesforce professional \u2014 the platform, admin basics, automation, and your first steps into development."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "0.6rem"
    }
  }, /*#__PURE__*/React.createElement(LevelBadge, {
    level: "beginner"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      borderTop: "1px solid rgb(255 255 255 / 0.12)",
      paddingTop: "1rem"
    }
  }, /*#__PURE__*/React.createElement(CourseStats, {
    stats: [{
      icon: "ph-books",
      value: "07",
      label: "lessons"
    }, {
      icon: "ph-clock",
      value: "1h 10m",
      label: "content"
    }, {
      icon: "ph-users-three",
      value: "8,200",
      label: "enrolled"
    }]
  })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Button, {
    variant: "white"
  }, "Start course \u2014 Free"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      aspectRatio: "4/3",
      borderRadius: "var(--radius-card)",
      background: "rgb(255 255 255 / 0.04)",
      boxShadow: "inset 0 0 0 1px rgb(255 255 255 / 0.14)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ph ph-graduation-cap",
    style: {
      fontSize: "4rem",
      color: "var(--color-brand-300)"
    }
  })))), /*#__PURE__*/React.createElement("section", {
    style: {
      maxWidth: 1120,
      margin: "0 auto",
      padding: "3rem 1.5rem",
      display: "grid",
      gridTemplateColumns: "1fr 320px",
      gap: "3rem",
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "1.5rem"
    }
  }, /*#__PURE__*/React.createElement(Kicker, null, "Curriculum"), /*#__PURE__*/React.createElement(CurriculumList, {
    variant: "detailed",
    items: LESSONS
  }), /*#__PURE__*/React.createElement(AdSlot, null)), /*#__PURE__*/React.createElement("aside", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "1.25rem",
      position: "sticky",
      top: "5rem"
    }
  }, /*#__PURE__*/React.createElement(AuthorBox, {
    name: "Namaste UI",
    bio: "Community-run Salesforce learning project \u2014 courses written and maintained by working admins & developers."
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: "1.1rem 1.25rem",
      borderRadius: "var(--radius-card)",
      boxShadow: "inset 0 0 0 1px var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontWeight: 700,
      marginBottom: "0.4rem"
    }
  }, "Need help?"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "0.85rem",
      color: "var(--color-muted)",
      marginBottom: "0.75rem"
    }
  }, "Ask in the community forum or open an issue on GitHub."), /*#__PURE__*/React.createElement(Button, {
    size: "sm",
    variant: "outline"
  }, "Get support")))));
}
window.CourseDetailScreen = CourseDetailScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/CourseDetailScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/CoursesScreen.jsx
try { (() => {
const {
  CourseCard,
  Kicker,
  Input,
  CourseStats
} = window.NamasteUIDesignSystem_e97b71;
const COURSES = [{
  title: "Salesforce — Zero to Hero",
  excerpt: "Go from total beginner to job-ready Salesforce professional — platform, admin basics, automation, and your first steps into development.",
  level: "beginner",
  price: "free",
  lessons: 7,
  duration: "1h 10m",
  author: "Namaste UI",
  featured: true
}, {
  title: "Apex Masterclass",
  excerpt: "Master server-side Salesforce development: Apex language, SOQL, triggers, bulkification, async Apex, and testing to 75%+ coverage.",
  level: "advanced",
  price: "paid",
  priceLabel: "$49",
  lessons: 12,
  duration: "6h 40m",
  author: "Namaste UI"
}, {
  title: "CRM Analytics",
  excerpt: "Build analytics apps in CRM Analytics: datasets, recipes & dataflows, lenses, dashboards, SAQL, and bindings.",
  level: "intermediate",
  price: "paid",
  priceLabel: "$39",
  lessons: 10,
  duration: "4h 20m",
  author: "Namaste UI"
}, {
  title: "Conga CPQ",
  excerpt: "Understand Conga CPQ end to end: product catalog, bundles, pricing, constraint rules, approvals, quotes and documents.",
  level: "intermediate",
  price: "paid",
  priceLabel: "$59",
  lessons: 9,
  duration: "5h 05m",
  author: "Namaste UI",
  sponsored: true
}, {
  title: "LWC A-Z",
  excerpt: "Build modern Salesforce UIs with Lightning Web Components: templates, reactivity, events, Apex wiring, LDS, and deployment.",
  level: "advanced",
  price: "paid",
  priceLabel: "$45",
  lessons: 14,
  duration: "7h 15m",
  author: "Namaste UI"
}];
function CoursesScreen({
  goCourse
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto",
      padding: "3rem 1.5rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "center",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: "1rem",
      marginBottom: "2.5rem"
    }
  }, /*#__PURE__*/React.createElement(Kicker, {
    align: "center"
  }, "Courses"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 800,
      fontSize: "2rem"
    }
  }, "Every Salesforce course, in one catalog"), /*#__PURE__*/React.createElement("div", {
    style: {
      width: "100%",
      maxWidth: 480
    }
  }, /*#__PURE__*/React.createElement(Input, {
    icon: "ph-magnifying-glass",
    placeholder: "Search courses, topics, tags...",
    hint: "\u2318K"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      paddingTop: "0.5rem"
    }
  }, /*#__PURE__*/React.createElement(CourseStats, {
    onDark: false,
    stats: [{
      icon: "ph-books",
      value: "05",
      label: "courses"
    }, {
      icon: "ph-play",
      value: "52",
      label: "lessons"
    }, {
      icon: "ph-clock",
      value: "24h",
      label: "content"
    }]
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "220px 1fr",
      gap: "2rem",
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement("aside", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "1.25rem"
    }
  }, /*#__PURE__*/React.createElement("fieldset", {
    style: {
      border: 0,
      padding: 0,
      margin: 0
    }
  }, /*#__PURE__*/React.createElement("legend", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "var(--color-label)",
      marginBottom: "0.5rem"
    }
  }, "Level"), ["Beginner", "Intermediate", "Advanced"].map(l => /*#__PURE__*/React.createElement("label", {
    key: l,
    style: {
      display: "flex",
      alignItems: "center",
      gap: "0.55rem",
      padding: "0.3rem 0",
      fontSize: "0.875rem",
      cursor: "pointer"
    }
  }, /*#__PURE__*/React.createElement("input", {
    type: "checkbox",
    style: {
      accentColor: "var(--color-brand-500)"
    }
  }), " ", l))), /*#__PURE__*/React.createElement("fieldset", {
    style: {
      border: 0,
      padding: 0,
      margin: 0
    }
  }, /*#__PURE__*/React.createElement("legend", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "var(--color-label)",
      marginBottom: "0.5rem"
    }
  }, "Price"), ["Free", "Paid"].map(l => /*#__PURE__*/React.createElement("label", {
    key: l,
    style: {
      display: "flex",
      alignItems: "center",
      gap: "0.55rem",
      padding: "0.3rem 0",
      fontSize: "0.875rem",
      cursor: "pointer"
    }
  }, /*#__PURE__*/React.createElement("input", {
    type: "radio",
    name: "price",
    style: {
      accentColor: "var(--color-brand-500)"
    }
  }), " ", l)))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill,minmax(280px,1fr))",
      gap: "1.25rem"
    }
  }, COURSES.map((c, i) => /*#__PURE__*/React.createElement(CourseCard, {
    key: c.title,
    index: i + 1,
    title: c.title,
    excerpt: c.excerpt,
    level: c.level,
    price: c.price,
    priceLabel: c.priceLabel,
    lessons: c.lessons,
    duration: c.duration,
    authorName: c.author,
    featured: c.featured,
    sponsored: c.sponsored,
    href: "#",
    onClick: e => {
      e.preventDefault();
      goCourse();
    }
  })))));
}
window.CoursesScreen = CoursesScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/CoursesScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/DocsScreen.jsx
try { (() => {
const {
  Kicker,
  Input,
  Badge
} = window.NamasteUIDesignSystem_e97b71;
const SECTIONS = [{
  title: "Getting Started",
  items: ["Installing the theme", "Local Ghost setup", "Theme settings"]
}, {
  title: "Guides",
  items: ["Adding a course", "Adding a training section", "Configuring ads & sponsors"]
}, {
  title: "Reference",
  items: ["Handlebars helpers", "Tag conventions", "routes.yaml"]
}];
function DocsScreen() {
  const [active, setActive] = window.React.useState("Adding a course");
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1120,
      margin: "0 auto",
      padding: "3rem 1.5rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "center",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: "1rem",
      marginBottom: "2.5rem"
    }
  }, /*#__PURE__*/React.createElement(Kicker, {
    align: "center"
  }, "Documentation"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 800,
      fontSize: "2rem"
    }
  }, "Everything to run this theme"), /*#__PURE__*/React.createElement("div", {
    style: {
      width: "100%",
      maxWidth: 480
    }
  }, /*#__PURE__*/React.createElement(Input, {
    icon: "ph-magnifying-glass",
    placeholder: "Search the docs...",
    hint: "\u2318K"
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "240px 1fr",
      gap: "2.5rem"
    }
  }, /*#__PURE__*/React.createElement("aside", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "1.5rem"
    }
  }, SECTIONS.map(sec => /*#__PURE__*/React.createElement("div", {
    key: sec.title
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "var(--tracking-label)",
      color: "var(--color-label)",
      marginBottom: "0.5rem"
    }
  }, sec.title), sec.items.map(it => /*#__PURE__*/React.createElement("a", {
    key: it,
    onClick: e => {
      e.preventDefault();
      setActive(it);
    },
    href: "#",
    style: {
      display: "block",
      padding: "0.4rem 0.6rem",
      borderRadius: "var(--radius-sm)",
      fontSize: "0.875rem",
      textDecoration: "none",
      color: active === it ? "var(--color-brand-600)" : "var(--color-ink)",
      boxShadow: active === it ? "inset 2px 0 0 var(--color-brand-500)" : "none",
      fontWeight: active === it ? 600 : 400
    }
  }, it))))), /*#__PURE__*/React.createElement("article", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "1rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "0.5rem"
    }
  }, /*#__PURE__*/React.createElement(Badge, null, "Guide"), /*#__PURE__*/React.createElement(Badge, {
    variant: "accent"
  }, "v1")), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 800,
      fontSize: "1.5rem"
    }
  }, active), /*#__PURE__*/React.createElement("p", {
    style: {
      color: "var(--color-muted)",
      lineHeight: 1.7
    }
  }, "A course's primary public tag is the course tag; its slug must equal that tag. Lessons carry the course tag as their primary tag plus the internal ", /*#__PURE__*/React.createElement("code", {
    style: {
      fontFamily: "var(--font-mono)",
      background: "var(--color-surface-sunken)",
      padding: "0.1rem 0.4rem",
      borderRadius: "var(--radius-sm)"
    }
  }, "#lesson"), " marker, so the router nests them at ", /*#__PURE__*/React.createElement("code", {
    style: {
      fontFamily: "var(--font-mono)"
    }
  }, "/courses/", "{tag}", "/", "{slug}", "/"), "."), /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: "var(--radius-sm)",
      overflow: "hidden",
      boxShadow: "inset 0 0 0 1px var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: "var(--color-brand-900)",
      padding: "8px 12px 0"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      background: "#fff",
      color: "var(--color-brand-600)",
      fontFamily: "var(--font-mono)",
      fontSize: 12,
      fontWeight: 700,
      borderRadius: "4px 4px 0 0",
      padding: "6px 12px",
      display: "inline-block"
    }
  }, "routes.yaml")), /*#__PURE__*/React.createElement("pre", {
    style: {
      margin: 0,
      background: "var(--color-surface)",
      padding: 14,
      fontFamily: "var(--font-mono)",
      fontSize: 13,
      color: "var(--color-ink)",
      overflowX: "auto"
    }
  }, "  /courses/apex-masterclass/:\n    data: tag.apex-masterclass\n    template: course")))));
}
window.DocsScreen = DocsScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/DocsScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/HomeScreen.jsx
try { (() => {
const {
  Button,
  Kicker,
  Chip,
  CourseStats
} = window.NamasteUIDesignSystem_e97b71;
function HomeScreen({
  goCourse
}) {
  const features = [["ph-lightning", "Learn by doing", "Every lesson runs inside your own free Developer org — no sandboxes, no waiting."], ["ph-books", "Structured tracks", "Courses and an eight-part training roadmap take you from zero to certified."], ["ph-chart-bar", "See it click", "Reports, dashboards and Flow automations you build are real, working artifacts."]];
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("section", {
    style: {
      position: "relative",
      overflow: "hidden",
      background: "var(--color-brand-900)",
      color: "#fff",
      padding: "5rem 1.5rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      backgroundImage: "linear-gradient(to right, rgb(255 255 255 / 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgb(255 255 255 / 0.05) 1px, transparent 1px)",
      backgroundSize: "44px 44px",
      WebkitMaskImage: "radial-gradient(ellipse 100% 100% at 50% 20%, #000 20%, transparent 72%)",
      maskImage: "radial-gradient(ellipse 100% 100% at 50% 20%, #000 20%, transparent 72%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      maxWidth: 760,
      margin: "0 auto",
      textAlign: "center",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: "1.25rem"
    }
  }, /*#__PURE__*/React.createElement(Kicker, {
    align: "center",
    light: true
  }, "Open-source Salesforce learning"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "var(--font-heading)",
      fontSize: "var(--size-display)",
      fontWeight: 800,
      lineHeight: 1.1
    }
  }, "Go from zero to job-ready Salesforce professional"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: "1.125rem",
      color: "rgb(255 255 255 / 0.72)",
      maxWidth: 560
    }
  }, "Courses, an eight-part training roadmap, and developer documentation \u2014 one calm, fast platform built for learning the platform, not fighting the UI."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "0.75rem"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "white",
    icon: "ph-arrow-right",
    iconPosition: "right",
    onClick: goCourse
  }, "Start Zero to Hero"), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost"
  }, "Browse courses")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "1.5rem",
      borderTop: "1px solid rgb(255 255 255 / 0.12)",
      paddingTop: "1.25rem"
    }
  }, /*#__PURE__*/React.createElement(CourseStats, {
    stats: [{
      icon: "ph-users-three",
      value: "12,400",
      label: "learners"
    }, {
      icon: "ph-books",
      value: "05",
      label: "courses"
    }, {
      icon: "ph-star",
      value: "4.9",
      label: "avg rating"
    }]
  })))), /*#__PURE__*/React.createElement("section", {
    style: {
      maxWidth: 1120,
      margin: "0 auto",
      padding: "4rem 1.5rem",
      display: "flex",
      flexDirection: "column",
      gap: "2rem"
    }
  }, /*#__PURE__*/React.createElement(Kicker, {
    align: "center"
  }, "Why Namaste Salesforce"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
      gap: "1.25rem"
    }
  }, features.map(([icon, title, body]) => /*#__PURE__*/React.createElement("div", {
    key: title,
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "0.75rem",
      padding: "1.4rem",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-card)",
      background: "var(--color-surface-raised)"
    }
  }, /*#__PURE__*/React.createElement(Chip, {
    icon: icon
  }), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 700,
      fontSize: "1.05rem"
    }
  }, title), /*#__PURE__*/React.createElement("p", {
    style: {
      color: "var(--color-muted)",
      fontSize: "0.9rem",
      lineHeight: 1.6
    }
  }, body))))));
}
window.HomeScreen = HomeScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/HomeScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/Nav.jsx
try { (() => {
const {
  Navbar,
  Logo
} = window.NamasteUIDesignSystem_e97b71;
function Nav({
  dark,
  onToggleDark,
  screen,
  setScreen
}) {
  const links = [["home", "Home", "ph-house"], ["courses", "Courses", "ph-graduation-cap"], ["course", "Course", "ph-book-bookmark"], ["player", "Player", "ph-play-circle"], ["training", "Training", "ph-flag-checkered"], ["blog", "Blog", "ph-article"], ["resources", "Resources", "ph-folders"], ["docs", "Docs", "ph-book-open-text"]].map(([id, label, icon]) => ({
    id,
    label,
    icon
  }));
  return /*#__PURE__*/React.createElement(Navbar, {
    logo: /*#__PURE__*/React.createElement(Logo, {
      iconSrc: "../../assets/logo/favicon.svg"
    }),
    links: links,
    activeId: screen,
    onNavigate: setScreen,
    dark: dark,
    onToggleDark: onToggleDark
  });
}
window.Nav = Nav;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/Nav.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/PlayerScreen.jsx
try { (() => {
const {
  TableOfContents,
  TimelineStepper,
  VideoPoster,
  CodeBlock,
  CurriculumList,
  Kicker,
  Button
} = window.NamasteUIDesignSystem_e97b71;
const LESSONS = [{
  title: "What is Salesforce & the Ecosystem",
  type: "article",
  done: true
}, {
  title: "Editions, Orgs & Signing Up",
  type: "article",
  done: true
}, {
  title: "Navigating Lightning Experience",
  type: "article"
}, {
  title: "Objects, Records & Fields",
  type: "article"
}, {
  title: "Your First Automation with Flow",
  type: "exercise"
}];
const TOC = [{
  id: "intro",
  label: "Introduction"
}, {
  id: "editions",
  label: "Editions & orgs"
}, {
  id: "devorg",
  label: "Signing up for a Dev org",
  level: 3
}, {
  id: "habits",
  label: "Habits worth forming"
}];
function PlayerScreen() {
  const [active, setActive] = window.React.useState("editions");
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 1280,
      margin: "0 auto",
      padding: "2rem 1.5rem",
      display: "grid",
      gridTemplateColumns: "240px 1fr 200px",
      gap: "2rem",
      alignItems: "start"
    }
  }, /*#__PURE__*/React.createElement("aside", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--size-label)",
      fontWeight: 700,
      letterSpacing: "var(--tracking-label)",
      textTransform: "uppercase",
      color: "var(--color-label)",
      marginBottom: "0.6rem"
    }
  }, "Course Player"), /*#__PURE__*/React.createElement(CurriculumList, {
    variant: "timeline",
    items: LESSONS
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "1.5rem"
    }
  }, /*#__PURE__*/React.createElement(TimelineStepper, {
    steps: ["Watch", "Read", "Exercise", "Done"],
    activeIndex: 1
  }), /*#__PURE__*/React.createElement(VideoPoster, null), /*#__PURE__*/React.createElement(Kicker, null, "Editions, Orgs & Signing Up for a Dev Org"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: "var(--color-muted)",
      lineHeight: 1.7
    }
  }, "An ", /*#__PURE__*/React.createElement("b", {
    id: "intro"
  }, "org"), " is a single instance of Salesforce with its own users, data, and configuration. ", /*#__PURE__*/React.createElement("b", {
    id: "editions"
  }, "Editions"), " are the packaging tiers that decide which features and limits you get."), /*#__PURE__*/React.createElement(CodeBlock, {
    filename: "apex",
    code: "public class OrgUtil {\n  // returns the current org's namespace\n  public static String namespace() {\n    return UserInfo.getOrganizationId();\n  }\n}"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "outline",
    icon: "ph-arrow-left"
  }, "Previous"), /*#__PURE__*/React.createElement(Button, {
    icon: "ph-arrow-right",
    iconPosition: "right"
  }, "Next lesson"))), /*#__PURE__*/React.createElement(TableOfContents, {
    activeId: active,
    onNavigate: setActive,
    items: TOC
  }));
}
window.PlayerScreen = PlayerScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/PlayerScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/ResourcesScreen.jsx
try { (() => {
const {
  Hero,
  ResourceCard,
  Kicker
} = window.NamasteUIDesignSystem_e97b71;
const GROUPS = [{
  title: "Study Guides",
  items: [["Admin Cert Study Guide", "PDF", "ph-file-text"], ["Platform Developer I Guide", "PDF", "ph-file-text"]]
}, {
  title: "Templates",
  items: [["Flow Naming Conventions", "Template", "ph-flow-arrow"], ["Trigger Handler Boilerplate", "Template", "ph-code"]]
}, {
  title: "Tools",
  items: [["VS Code Apex Snippets", "Tool", "ph-terminal-window"], ["Data Loader Cheat Sheet", "PDF", "ph-database"]]
}];
function ResourcesScreen() {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Hero, {
    variant: "compact",
    kicker: "Resources",
    title: "Cheat sheets, templates & tools"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 900,
      margin: "0 auto",
      padding: "2.5rem 1.5rem",
      display: "flex",
      flexDirection: "column",
      gap: "2rem"
    }
  }, GROUPS.map(g => /*#__PURE__*/React.createElement("div", {
    key: g.title
  }, /*#__PURE__*/React.createElement(Kicker, null, g.title), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "0.9rem",
      display: "flex",
      flexDirection: "column",
      gap: "0.6rem"
    }
  }, g.items.map(([title, type, icon]) => /*#__PURE__*/React.createElement(ResourceCard, {
    key: title,
    title: title,
    type: type,
    icon: icon
  })))))));
}
window.ResourcesScreen = ResourcesScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/ResourcesScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/lms/TrainingScreen.jsx
try { (() => {
const {
  Kicker,
  RoadmapCard,
  Button
} = window.NamasteUIDesignSystem_e97b71;
const SECTIONS = [{
  n: 1,
  title: "Foundations",
  desc: "What Salesforce is, the ecosystem, and your first Developer org.",
  icon: "ph-flag",
  lessons: 7,
  duration: "1h 10m"
}, {
  n: 2,
  title: "Org Setup",
  desc: "Editions, licenses, and configuring your org's baseline settings.",
  icon: "ph-gear-six",
  lessons: 5,
  duration: "55m"
}, {
  n: 3,
  title: "Navigation",
  desc: "The App Launcher, list views, record pages, and global search.",
  icon: "ph-compass",
  lessons: 4,
  duration: "40m"
}, {
  n: 4,
  title: "Data Model",
  desc: "Objects, fields, and the relationships that connect them.",
  icon: "ph-database",
  lessons: 6,
  duration: "1h 05m"
}, {
  n: 5,
  title: "Security",
  desc: "Profiles, permission sets, sharing rules, and field-level security.",
  icon: "ph-shield-check",
  lessons: 6,
  duration: "1h 15m"
}, {
  n: 6,
  title: "Automation",
  desc: "Flow Builder: record-triggered flows, decisions, and best practices.",
  icon: "ph-flow-arrow",
  lessons: 5,
  duration: "1h 00m"
}, {
  n: 7,
  title: "Reports & Dashboards",
  desc: "Report types, groupings, chart components, and a working dashboard.",
  icon: "ph-chart-bar",
  lessons: 4,
  duration: "45m"
}, {
  n: 8,
  title: "Apex / Code",
  desc: "Your first steps from clicks to code, and where to go next.",
  icon: "ph-code",
  lessons: 7,
  duration: "1h 20m"
}];
function TrainingScreen() {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 900,
      margin: "0 auto",
      padding: "3.5rem 1.5rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "center",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: "1rem",
      marginBottom: "3rem"
    }
  }, /*#__PURE__*/React.createElement(Kicker, {
    align: "center"
  }, "Training Roadmap"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 800,
      fontSize: "2rem"
    }
  }, "The path from zero to certified"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: "var(--color-muted)",
      maxWidth: 560
    }
  }, "Eight sections, one dashed trail. Work through them in order, or jump to the one you need.")), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: "50%",
      top: "0.5rem",
      bottom: "2.5rem",
      width: 2,
      marginLeft: -1,
      background: "repeating-linear-gradient(to bottom, var(--color-border) 0 8px, transparent 8px 15px)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      textAlign: "center",
      marginBottom: "2rem"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: 16,
      height: 16,
      borderRadius: 9999,
      background: "var(--color-brand-500)",
      boxShadow: "0 0 0 5px color-mix(in srgb, var(--color-brand-500) 14%, transparent)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "0.6rem",
      fontFamily: "var(--font-mono)",
      fontSize: "0.7rem",
      fontWeight: 700,
      letterSpacing: "0.14em",
      textTransform: "uppercase",
      color: "var(--color-brand-600)"
    }
  }, "Start")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: "1.5rem"
    }
  }, SECTIONS.map((s, i) => /*#__PURE__*/React.createElement("div", {
    key: s.n,
    style: {
      width: "calc(50% - 2rem)",
      marginLeft: i % 2 === 0 ? 0 : "auto"
    }
  }, /*#__PURE__*/React.createElement(RoadmapCard, {
    n: s.n,
    title: s.title,
    desc: s.desc,
    icon: s.icon,
    lessons: s.lessons,
    duration: s.duration
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      textAlign: "center",
      marginTop: "3rem",
      maxWidth: 480,
      marginInline: "auto"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      left: "50%",
      top: "-2.3rem",
      transform: "translateX(-50%)",
      display: "inline-flex",
      width: 16,
      height: 16,
      borderRadius: 9999,
      background: "var(--color-brand-500)",
      boxShadow: "0 0 0 5px color-mix(in srgb, var(--color-brand-500) 14%, transparent)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: "var(--radius-card)",
      background: "var(--color-surface-sunken)",
      boxShadow: "inset 0 0 0 1px var(--color-border)",
      padding: "1.5rem"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "0.65rem",
      fontWeight: 700,
      letterSpacing: "0.12em",
      textTransform: "uppercase",
      color: "var(--color-brand-600)"
    }
  }, "Finish"), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontFamily: "var(--font-heading)",
      fontWeight: 800,
      marginTop: "0.5rem"
    }
  }, "You've gone from zero."), /*#__PURE__*/React.createElement("p", {
    style: {
      color: "var(--color-muted)",
      fontSize: "0.9rem",
      marginTop: "0.4rem"
    }
  }, "Pick your certification track and keep practising in your Developer org."), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "1rem"
    }
  }, /*#__PURE__*/React.createElement(Button, {
    size: "sm"
  }, "Get the newsletter"))))));
}
window.TrainingScreen = TrainingScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/lms/TrainingScreen.jsx", error: String((e && e.message) || e) }); }

__ds_ns.AvatarRing = __ds_scope.AvatarRing;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Chip = __ds_scope.Chip;

__ds_ns.CodeBlock = __ds_scope.CodeBlock;

__ds_ns.CodePanel = __ds_scope.CodePanel;

__ds_ns.Footer = __ds_scope.Footer;

__ds_ns.Hero = __ds_scope.Hero;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Kicker = __ds_scope.Kicker;

__ds_ns.Logo = __ds_scope.Logo;

__ds_ns.Navbar = __ds_scope.Navbar;

__ds_ns.TableOfContents = __ds_scope.TableOfContents;

__ds_ns.TimelineStepper = __ds_scope.TimelineStepper;

__ds_ns.AdSlot = __ds_scope.AdSlot;

__ds_ns.AuthorBox = __ds_scope.AuthorBox;

__ds_ns.BlogCard = __ds_scope.BlogCard;

__ds_ns.CourseCard = __ds_scope.CourseCard;

__ds_ns.CourseStats = __ds_scope.CourseStats;

__ds_ns.CurriculumList = __ds_scope.CurriculumList;

__ds_ns.LevelBadge = __ds_scope.LevelBadge;

__ds_ns.ResourceCard = __ds_scope.ResourceCard;

__ds_ns.RoadmapCard = __ds_scope.RoadmapCard;

__ds_ns.TrainingCard = __ds_scope.TrainingCard;

__ds_ns.VideoPoster = __ds_scope.VideoPoster;

})();
