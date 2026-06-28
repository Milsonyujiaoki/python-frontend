"""
Shared Design System for Barbershop SaaS Frontends.

This module provides consistent design tokens, themes, and utilities
across all frontend frameworks (Solara, Streamlit, Flet, etc.).

Design References:
- Linear: Clean, minimal, developer-focused
- Vercel: Bold typography, subtle gradients
- Stripe: Professional data presentation
- Apple: Premium feel, smooth animations
- Nubank: Vibrant colors, friendly UX
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
import json


# =============================================================================
# DESIGN TOKENS
# =============================================================================

@dataclass
class ColorPalette:
    """Color system inspired by modern brands."""
    # Primary - Brand color (Nubank purple vibe)
    primary_50: str = "#ede9fe"
    primary_100: str = "#ddd6fe"
    primary_200: str = "#c4b5fd"
    primary_300: str = "#a78bfa"
    primary_400: str = "#8b5cf6"
    primary_500: str = "#7c3aed"  # Main primary
    primary_600: str = "#6d28d9"
    primary_700: str = "#5b21b6"
    primary_800: str = "#4c1d95"
    primary_900: str = "#43147a"

    # Secondary - Accent (Emerald like Stripe)
    secondary_50: str = "#ecfdf5"
    secondary_100: str = "#d1fae5"
    secondary_200: str = "#a7f3d0"
    secondary_300: str = "#6ee7b7"
    secondary_400: str = "#34d399"
    secondary_500: str = "#10b981"  # Main secondary
    secondary_600: str = "#059669"
    secondary_700: str = "#047857"

    # Neutral - Grays (Linear/Vercel style)
    neutral_0: str = "#ffffff"
    neutral_50: str = "#f8fafc"
    neutral_100: str = "#f1f5f9"
    neutral_200: str = "#e2e8f0"
    neutral_300: str = "#cbd5e1"
    neutral_400: str = "#94a3b8"
    neutral_500: str = "#64748b"
    neutral_600: str = "#475569"
    neutral_700: str = "#334155"
    neutral_800: str = "#1e293b"
    neutral_900: str = "#0f172a"

    # Semantic
    success: str = "#10b981"
    warning: str = "#f59e0b"
    error: str = "#ef4444"
    info: str = "#3b82f6"

    # Gradients
    gradient_primary: str = "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)"
    gradient_success: str = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
    gradient_dark: str = "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)"


@dataclass
class Typography:
    """Typography scale."""
    font_family: str = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    font_mono: str = "'JetBrains Mono', 'Fira Code', 'Consolas', monospace"

    # Font sizes (rem scale)
    xs: str = "0.75rem"      # 12px
    sm: str = "0.875rem"     # 14px
    base: str = "1rem"       # 16px
    lg: str = "1.125rem"     # 18px
    xl: str = "1.25rem"      # 20px
    "2xl": str = "1.5rem"    # 24px
    "3xl": str = "1.875rem"  # 30px
    "4xl": str = "2.25rem"   # 36px
    "5xl": str = "3rem"      # 48px

    # Font weights
    font_light: str = "300"
    font_normal: str = "400"
    font_medium: str = "500"
    font_semibold: str = "600"
    font_bold: str = "700"

    # Line heights
    tight: str = "1.25"
    normal: str = "1.5"
    relaxed: str = "1.75"


@dataclass
class Spacing:
    """Spacing scale (8px base)."""
    px: str = "1px"
    "0": str = "0"
    "1": str = "0.25rem"   # 4px
    "2": str = "0.5rem"    # 8px
    "3": str = "0.75rem"   # 12px
    "4": str = "1rem"      # 16px
    "5": str = "1.25rem"   # 20px
    "6": str = "1.5rem"    # 24px
    "8": str = "2rem"      # 32px
    "10": str = "2.5rem"   # 40px
    "12": str = "3rem"     # 48px
    "16": str = "4rem"     # 64px
    "20": str = "5rem"     # 80px
    "24": str = "6rem"     # 96px


@dataclass
class BorderRadius:
    """Border radius scale."""
    none: str = "0"
    sm: str = "0.25rem"    # 4px
    base: str = "0.5rem"   # 8px
    md: str = "0.625rem"   # 10px
    lg: str = "0.75rem"    # 12px
    xl: str = "1rem"       # 16px
    "2xl": str = "1.25rem" # 20px
    "3xl": str = "1.5rem"  # 24px
    full: str = "9999px"   # Pill/circle


@dataclass
class Shadow:
    """Shadow elevations."""
    none: str = "none"
    xs: str = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    sm: str = "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)"
    base: str = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)"
    md: str = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)"
    lg: str = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)"
    xl: str = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)"
    "2xl": str = "0 25px 50px -12px rgba(0, 0, 0, 0.25)"
    inner: str = "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)"


# =============================================================================
# THEMES
# =============================================================================

@dataclass
class Theme:
    """Complete theme configuration."""
    name: str
    colors: ColorPalette
    typography: Typography
    spacing: Spacing
    border_radius: BorderRadius
    shadow: Shadow

    # Brand customization
    brand_name: str = "BarberPro"
    brand_logo: str = "✂️"
    brand_tagline: str = "Professional Barbershop Management"


def get_light_theme(brand_name: str = "BarberPro") -> Theme:
    """Get light theme configuration."""
    return Theme(
        name="light",
        brand_name=brand_name,
        colors=ColorPalette(),
        typography=Typography(),
        spacing=Spacing(),
        border_radius=BorderRadius(),
        shadow=Shadow(),
    )


def get_dark_theme(brand_name: str = "BarberPro") -> Theme:
    """Get dark theme configuration (inverted colors)."""
    return Theme(
        name="dark",
        brand_name=brand_name,
        colors=ColorPalette(),
        typography=Typography(),
        spacing=Spacing(),
        border_radius=BorderRadius(),
        shadow=Shadow(),
    )


# =============================================================================
# CSS GENERATOR
# =============================================================================

def generate_css_variables(theme: Theme) -> str:
    """Generate CSS custom properties (variables) from theme."""
    colors = theme.colors

    return f"""
/* Design System - {theme.name} theme */
:root {{
  /* Brand */
  --brand-name: {theme.brand_name};
  --brand-logo: "{theme.brand_logo}";

  /* Primary Colors */
  --color-primary-50: {colors.primary_50};
  --color-primary-100: {colors.primary_100};
  --color-primary-200: {colors.primary_200};
  --color-primary-300: {colors.primary_300};
  --color-primary-400: {colors.primary_400};
  --color-primary-500: {colors.primary_500};
  --color-primary-600: {colors.primary_600};
  --color-primary-700: {colors.primary_700};
  --color-primary-800: {colors.primary_800};
  --color-primary-900: {colors.primary_900};

  /* Secondary Colors */
  --color-secondary-50: {colors.secondary_50};
  --color-secondary-100: {colors.secondary_100};
  --color-secondary-200: {colors.secondary_200};
  --color-secondary-300: {colors.secondary_300};
  --color-secondary-400: {colors.secondary_400};
  --color-secondary-500: {colors.secondary_500};
  --color-secondary-600: {colors.secondary_600};
  --color-secondary-700: {colors.secondary_700};

  /* Neutral Colors */
  --color-neutral-0: {colors.neutral_0};
  --color-neutral-50: {colors.neutral_50};
  --color-neutral-100: {colors.neutral_100};
  --color-neutral-200: {colors.neutral_200};
  --color-neutral-300: {colors.neutral_300};
  --color-neutral-400: {colors.neutral_400};
  --color-neutral-500: {colors.neutral_500};
  --color-neutral-600: {colors.neutral_600};
  --color-neutral-700: {colors.neutral_700};
  --color-neutral-800: {colors.neutral_800};
  --color-neutral-900: {colors.neutral_900};

  /* Semantic */
  --color-success: {colors.success};
  --color-warning: {colors.warning};
  --color-error: {colors.error};
  --color-info: {colors.info};

  /* Gradients */
  --gradient-primary: {colors.gradient_primary};
  --gradient-success: {colors.gradient_success};
  --gradient-dark: {colors.gradient_dark};

  /* Typography */
  --font-family: {theme.typography.font_family};
  --font-mono: {theme.typography.font_mono};

  /* Spacing */
  --spacing-1: {theme.spacing['1']};
  --spacing-2: {theme.spacing['2']};
  --spacing-3: {theme.spacing['3']};
  --spacing-4: {theme.spacing['4']};
  --spacing-5: {theme.spacing['5']};
  --spacing-6: {theme.spacing['6']};
  --spacing-8: {theme.spacing['8']};
  --spacing-10: {theme.spacing['10']};
  --spacing-12: {theme.spacing['12']};
  --spacing-16: {theme.spacing['16']};

  /* Border Radius */
  --radius-sm: {theme.border_radius.sm};
  --radius-base: {theme.border_radius.base};
  --radius-md: {theme.border_radius.md};
  --radius-lg: {theme.border_radius.lg};
  --radius-xl: {theme.border_radius.xl};
  --radius-2xl: {theme.border_radius['2xl']};
  --radius-full: {theme.border_radius.full};

  /* Shadows */
  --shadow-sm: {theme.shadow.sm};
  --shadow-base: {theme.shadow.base};
  --shadow-md: {theme.shadow.md};
  --shadow-lg: {theme.shadow.lg};
  --shadow-xl: {theme.shadow.xl};
}}

/* Base Styles */
* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: var(--font-family);
  background-color: var(--color-neutral-50);
  color: var(--color-neutral-900);
  line-height: var(--line-height-normal, 1.5);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}

/* Utility Classes */
.btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-base);
  font-weight: var(--font-medium);
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
}}

.btn-primary {{
  background: var(--gradient-primary);
  color: white;
}}

.btn-primary:hover {{
  opacity: 0.9;
  transform: translateY(-1px);
}}

.card {{
  background: var(--color-neutral-0);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-6);
}}

.input {{
  width: 100%;
  padding: var(--spacing-2) var(--spacing-3);
  border: 1px solid var(--color-neutral-300);
  border-radius: var(--radius-base);
  font-family: var(--font-family);
  font-size: var(--text-base);
  transition: border-color 0.2s ease;
}}

.input:focus {{
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px var(--color-primary-100);
}}
"""


# =============================================================================
# FRONTEND-SPECIFIC STYLES
# =============================================================================

def get_solara_css() -> str:
    """CSS optimized for Solara/Vuetify."""
    return """
/* Solara Custom Styles */
.v-card.solar-card {
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.v-card.solar-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.solara-metric {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    color: white;
    padding: 24px;
    border-radius: 16px;
}

.solara-nav-item {
    padding: 12px 16px;
    border-radius: 8px;
    transition: background-color 0.2s ease;
}

.solara-nav-item:hover {
    background-color: rgba(124, 58, 237, 0.1);
}

.solara-nav-item.active {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    color: white;
}
"""


def get_streamlit_css() -> str:
    """CSS optimized for Streamlit."""
    return """
/* Streamlit Custom Styles */
.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
}

.stMetric {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stButton > button {
    border-radius: 8px;
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    color: white;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}
"""


def get_flet_css() -> str:
    """CSS optimized for Flet (mobile-first)."""
    return """
/* Flet Custom Styles */
.flet-app-bar {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    color: white;
    border-radius: 0 0 16px 16px;
}

.flet-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin: 8px;
    padding: 16px;
}

.flet-button {
    border-radius: 12px;
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    padding: 14px 28px;
    font-weight: 600;
}

.flet-nav-rail {
    background: #1e293b;
    border-radius: 16px;
}

.flet-nav-item {
    padding: 12px;
    border-radius: 12px;
    margin: 4px;
}

.flet-nav-item.selected {
    background: rgba(124, 58, 237, 0.3);
}
"""


# =============================================================================
# EXPORT UTILITIES
# =============================================================================

def export_theme_json(theme: Theme, output_path: str) -> None:
    """Export theme to JSON file for frontend consumption."""
    theme_data = {
        "name": theme.name,
        "brand": {
            "name": theme.brand_name,
            "logo": theme.brand_logo,
            "tagline": theme.brand_tagline,
        },
        "colors": {
            "primary": {
                "50": theme.colors.primary_50,
                "100": theme.colors.primary_100,
                "200": theme.colors.primary_200,
                "300": theme.colors.primary_300,
                "400": theme.colors.primary_400,
                "500": theme.colors.primary_500,
                "600": theme.colors.primary_600,
                "700": theme.colors.primary_700,
                "800": theme.colors.primary_800,
                "900": theme.colors.primary_900,
            },
            "secondary": {
                "500": theme.colors.secondary_500,
                "600": theme.colors.secondary_600,
                "700": theme.colors.secondary_700,
            },
            "neutral": {
                "50": theme.colors.neutral_50,
                "100": theme.colors.neutral_100,
                "200": theme.colors.neutral_200,
                "300": theme.colors.neutral_300,
                "400": theme.colors.neutral_400,
                "500": theme.colors.neutral_500,
                "600": theme.colors.neutral_600,
                "700": theme.colors.neutral_700,
                "800": theme.colors.neutral_800,
                "900": theme.colors.neutral_900,
            },
            "semantic": {
                "success": theme.colors.success,
                "warning": theme.colors.warning,
                "error": theme.colors.error,
                "info": theme.colors.info,
            },
        },
        "typography": {
            "fontFamily": theme.typography.font_family,
            "fontMono": theme.typography.font_mono,
        },
        "spacing": {
            "4": theme.spacing["4"],
            "6": theme.spacing["6"],
            "8": theme.spacing["8"],
            "12": theme.spacing["12"],
        },
        "borderRadius": {
            "base": theme.border_radius.base,
            "lg": theme.border_radius.lg,
            "xl": theme.border_radius.xl,
        },
    }

    with open(output_path, 'w') as f:
        json.dump(theme_data, f, indent=2)

    return output_path


# Convenience exports
__all__ = [
    "ColorPalette",
    "Typography",
    "Spacing",
    "BorderRadius",
    "Shadow",
    "Theme",
    "get_light_theme",
    "get_dark_theme",
    "generate_css_variables",
    "get_solara_css",
    "get_streamlit_css",
    "get_flet_css",
    "export_theme_json",
]