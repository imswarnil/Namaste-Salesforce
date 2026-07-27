import React from "react";
/** Sharp-radius text input with a command-palette hint slot on the right (⌘K-style), not just a plain pill. */
export function Input({ placeholder, icon, hint, type = "text", value, onChange, style }) {
  return (
    <span style={{ position: "relative", display: "block", width: "100%" }}>
      {icon && <i className={`ph ${icon}`} aria-hidden="true" style={{ position: "absolute", left: "0.9rem", top: "50%", transform: "translateY(-50%)", color: "var(--color-muted)" }} />}
      <input
        type={type} placeholder={placeholder} value={value} onChange={onChange}
        style={{ width: "100%", boxSizing: "border-box", borderRadius: "var(--radius-btn)", border: "1px solid var(--color-border)", background: "var(--color-surface)", color: "var(--color-ink)", padding: `0.65rem ${hint ? "3.5rem" : "1rem"} 0.65rem ${icon ? "2.4rem" : "1rem"}`, fontSize: "0.9375rem", fontFamily: "var(--font-sans)", outline: "none", transition: "border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out)", ...style }}
        onFocus={(e) => { e.target.style.borderColor = "var(--color-brand-500)"; e.target.style.boxShadow = "var(--shadow-focus)"; }}
        onBlur={(e) => { e.target.style.borderColor = "var(--color-border)"; e.target.style.boxShadow = "none"; }}
      />
      {hint && <kbd style={{ position: "absolute", right: "0.7rem", top: "50%", transform: "translateY(-50%)", fontFamily: "var(--font-mono)", fontSize: "0.7rem", color: "var(--color-muted)", border: "1px solid var(--color-border)", borderRadius: "var(--radius-sm)", padding: "0.15rem 0.4rem" }}>{hint}</kbd>}
    </span>
  );
}
