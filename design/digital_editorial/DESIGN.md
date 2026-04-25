---
name: Digital Editorial
colors:
  surface: '#fbf9f5'
  surface-dim: '#dbdad6'
  surface-bright: '#fbf9f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3ef'
  surface-container: '#efeeea'
  surface-container-high: '#eae8e4'
  surface-container-highest: '#e4e2de'
  on-surface: '#1b1c1a'
  on-surface-variant: '#4d453e'
  inverse-surface: '#30312e'
  inverse-on-surface: '#f2f0ed'
  outline: '#7f756d'
  outline-variant: '#d0c4bb'
  surface-tint: '#6a5c4f'
  primary: '#6a5c4f'
  on-primary: '#ffffff'
  primary-container: '#c8b6a6'
  on-primary-container: '#54473b'
  inverse-primary: '#d6c3b3'
  secondary: '#6c5c4a'
  on-secondary: '#ffffff'
  secondary-container: '#f5dfc8'
  on-secondary-container: '#726250'
  tertiary: '#625e54'
  on-tertiary: '#ffffff'
  tertiary-container: '#beb8ac'
  on-tertiary-container: '#4d493f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#f3dfce'
  primary-fixed-dim: '#d6c3b3'
  on-primary-fixed: '#231a0f'
  on-primary-fixed-variant: '#514438'
  secondary-fixed: '#f5dfc8'
  secondary-fixed-dim: '#d8c3ad'
  on-secondary-fixed: '#25190c'
  on-secondary-fixed-variant: '#534434'
  tertiary-fixed: '#e9e2d5'
  tertiary-fixed-dim: '#ccc6b9'
  on-tertiary-fixed: '#1e1b14'
  on-tertiary-fixed-variant: '#4a463d'
  background: '#fbf9f5'
  on-background: '#1b1c1a'
  surface-variant: '#e4e2de'
typography:
  headline-xl:
    fontFamily: Newsreader
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Newsreader
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Newsreader
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Work Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Work Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: Work Sans
    fontSize: 13px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1120px
  content-max: 720px
  gutter: 24px
  margin-mobile: 20px
  stack-sm: 16px
  stack-md: 32px
  stack-lg: 64px
---

## Brand & Style

This design system is anchored in the concept of "Quiet Luxury"—a digital interpretation of high-end independent magazines and tactile stationery. The brand personality is intellectual, serene, and intentional, aiming to evoke a sense of focused calm for readers and writers alike.

The design style follows a **Minimalist** movement with **Tonal Layering**. By eschewing heavy shadows and vibrant gradients, the system relies on subtle shifts in value and sophisticated typographic hierarchy to create structure. It avoids the coldness of traditional tech minimalism by embracing organic, warm hues and a "paper-on-paper" depth model.

## Colors

The palette is monochromatic and warm, designed to reduce eye strain and simulate a physical reading environment. 

- **Primary & Secondary:** These warm earth tones are used sparingly for interactive elements, active states, and subtle accents.
- **Tertiary:** A mid-tone beige used for structural dividers and secondary surfaces to create soft contrast against the background.
- **Neutral:** The foundational "Cream" (#FDFBF7) serves as the primary canvas, providing a softer, more elegant backdrop than pure white.
- **Text:** A deep charcoal (#2D2D2D) provides high legibility while maintaining the softness of the overall aesthetic, avoiding the harshness of true black.

## Typography

This design system utilizes a classic serif/sans-serif pairing to distinguish between narrative content and functional UI.

- **Newsreader** is the primary voice for storytelling. It should be used for all editorial content, titles, and pull quotes to provide a literary, authoritative feel.
- **Work Sans** provides a grounded, neutral balance. It is used for body copy, navigation, and metadata. Its cleanliness ensures the UI remains modern and accessible.
- **Line Heights:** Generous leading is applied to body text (1.6) to enhance long-form readability, ensuring the "simple blog" experience feels spacious and unhurried.

## Layout & Spacing

The layout philosophy uses a **Fixed Grid** for desktop to maintain editorial control, transitioning to a **Fluid Grid** for mobile devices. 

- **Content Centering:** Blog posts are constrained to a `content-max` of 720px to maintain an optimal line length (50-75 characters) for readability. 
- **Vertical Rhythm:** A strict 8px baseline grid is used. Sections should be separated by large `stack-lg` (64px) gaps to reinforce the minimalist aesthetic and give the content "room to breathe."
- **Mobile responsiveness:** Margins scale down to 20px, and the grid collapses to a single column. Horizontal padding on cards and containers is reduced to maximize the reading area on small screens.

## Elevation & Depth

Depth in this design system is achieved through **Tonal Layers** and **Low-Contrast Outlines** rather than traditional shadows. 

- **Surface Tiers:** The base layer is the Neutral Cream. Overlays or cards use a slightly darker Tertiary Beige to indicate elevation. 
- **Borders:** Instead of drop shadows, use 1px solid borders in a color just 5% darker than the surface it sits upon. This creates a "hairline" edge that feels sharp and sophisticated.
- **Interactive Depth:** On hover, elements may shift slightly in background color (e.g., from Cream to a light Beige) or utilize a very soft, diffused ambient shadow (0px 4px 20px, 5% opacity) to signify tactility.

## Shapes

The shape language is **Soft**, utilizing subtle corner radii to bridge the gap between organic paper and digital screens. 

- **Standard Elements:** Buttons and small cards use a 0.25rem (4px) radius.
- **Containers:** Larger blog boards or image wrappers use a `rounded-lg` (8px) radius to feel substantial but not overly "bubbly."
- **Imagery:** Photography should maintain sharp or minimally rounded edges to align with a classic editorial look.

## Components

- **Buttons:** Primary buttons are solid Beige with Dark Grey text. Secondary buttons use a fine 1px border with no fill. All buttons feature high horizontal padding (24px) for a wide, elegant footprint.
- **Chips/Tags:** Small, pill-shaped tags with a Tertiary Beige background and `label-sm` typography. Used for categorizing blog topics without drawing excessive attention.
- **Cards:** Blog post previews should be borderless. Use a subtle background color change on the entire card area for hover states. Title hierarchy is paramount; images should have a fixed aspect ratio (3:2 or 16:9).
- **Input Fields:** Minimalist underlines or 1px borders in Muted Brown. Focus states transition the border to the Primary Beige color.
- **Lists:** Clean, unstyled lists with ample vertical padding (16px) between items, separated by 1px "hairline" dividers in Tertiary Beige.
- **Article Progress Bar:** A thin, 2px progress bar at the top of the viewport in the Primary color to assist readers during long-form sessions.