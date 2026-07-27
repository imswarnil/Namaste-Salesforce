export interface ButtonProps {
  /** primary = the ONE solid-fill action per screen; outline = default secondary (hairline border); accent, white, ghost = context variants for dark/photo surfaces. */
  variant?: "primary" | "accent" | "outline" | "white" | "ghost";
  size?: "sm" | "md" | "lg";
  /** Phosphor icon class, e.g. "ph-arrow-right" */
  icon?: string;
  iconPosition?: "left" | "right";
  disabled?: boolean;
  children?: React.ReactNode;
  onClick?: () => void;
  style?: React.CSSProperties;
}
