import React from "react";

/* Principle: no spring/bounce — press states are instant border/opacity
   shifts, never a translateY bounce. Radius is --radius-btn (sharp), not a
   pill; pill shape is reserved for tags. Primary is the only variant with a
   solid brand fill — everything else is a hairline border, so the one solid
   button on a screen reads as the one thing to click. */
const sizes = {
  sm: { padding: "0.4rem 0.85rem", fontSize: "0.8125rem" },
  md: { padding: "0.6rem 1.25rem", fontSize: "0.9rem" },
  lg: { padding: "0.75rem 1.5rem", fontSize: "1rem" },
};

const variants = {
  primary: { color: "#fff", background: "var(--color-brand-500)", border: "1px solid var(--color-brand-500)" },
  accent: { color: "#fff", background: "var(--color-accent-600)", border: "1px solid var(--color-accent-600)" },
  outline: { color: "var(--color-ink)", background: "transparent", border: "1px solid var(--color-border)" },
  white: { color: "var(--color-brand-800)", background: "#fff", border: "1px solid #fff" },
  ghost: { color: "#fff", background: "transparent", border: "1px solid rgb(255 255 255 / 0.3)" },
};

const hoverStyle = {
  primary: { background: "var(--color-brand-600)", borderColor: "var(--color-brand-600)" },
  accent: { background: "var(--color-accent-700)", borderColor: "var(--color-accent-700)" },
  outline: { borderColor: "var(--color-brand-500)", color: "var(--color-brand-600)" },
  white: { background: "var(--color-brand-50)" },
  ghost: { background: "rgb(255 255 255 / 0.1)", borderColor: "rgb(255 255 255 / 0.5)" },
};

/** Namaste UI's action button — sharp corners, hairline border by default, solid fill reserved for `primary`. Press is instant (no bounce, no lift). */
export function Button({ variant = "primary", size = "md", icon, iconPosition = "left", disabled, children, onClick, style }) {
  const [hover, setHover] = React.useState(false);
  const [active, setActive] = React.useState(false);
  const v = variants[variant] || variants.primary;
  const s = sizes[size] || sizes.md;
  const hv = hover && !disabled ? hoverStyle[variant] : {};
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => { setHover(false); setActive(false); }}
      onMouseDown={() => setActive(true)}
      onMouseUp={() => setActive(false)}
      style={{
        display: "inline-flex", alignItems: "center", justifyContent: "center", gap: "0.5rem",
        borderRadius: "var(--radius-btn)", fontWeight: 700, fontFamily: "var(--font-sans)",
        cursor: disabled ? "not-allowed" : "pointer", opacity: disabled ? 0.45 : active ? 0.85 : 1,
        transition: `background-color var(--duration-fast) var(--ease-out), border-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out), opacity var(--duration-fast) linear`,
        ...s, ...v, ...hv, ...style,
      }}
    >
      {icon && iconPosition === "left" && <i className={`ph ${icon}`} aria-hidden="true" />}
      {children}
      {icon && iconPosition === "right" && <i className={`ph ${icon}`} aria-hidden="true" />}
    </button>
  );
}
