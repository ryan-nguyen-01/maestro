# Design Standard (DS)

The house bar for every user interface Maestro designs, prototypes, builds, or reviews. It applies to the
static prototype at the Direction gate (R-019-0a-ui) and again to the built UI at QC. Levels and
precedence: [README.md](README.md). Stack idioms come from the matching skill (react, vue, angular,
tailwind, mobile, …) and the project's design system when one exists.

## A. Foundations

```text
DS-01 MUST   Tokens only. Color, type, spacing, radius, shadow, z-index, and motion values come from the
             design tokens (prototype styles.css / theme file). Components never hard-code hex, px
             spacing, or font sizes outside the token file.
DS-02 SHOULD Spacing on a 4/8-pt scale; elements align to a grid; related items sit closer together than
             unrelated ones (proximity carries grouping, not borders).
DS-03 SHOULD A type scale of <= 6 sizes. Web body text >= 16px (>= 14px only in dense data tools), body
             line-height 1.4-1.6, line length 45-90 characters.
DS-04 MUST (floor) Contrast meets WCAG 2.2 AA: text >= 4.5:1, large text and UI component boundaries,
             focus rings, and meaningful icons >= 3:1 — in every theme the product ships.
DS-05 SHOULD Color has semantic roles (primary, surface, text, muted, border, success, warning, danger,
             info). One primary action color. A dark theme is a token swap, never a forked stylesheet.
```

## B. Every state designed

```text
DS-06 MUST   Every data view specifies and implements: loading (skeleton when > 300 ms), empty (what this
             is + the next action), error (what happened + how to recover, with retry), success /
             partial, and offline or slow where the product can be used on mobile networks.
DS-07 MUST   Every form specifies: default, focus, filled, inline validation error next to the field with a
             specific message, disabled, submitting (double submit prevented), and success.
DS-08 SHOULD Stress content: very long names and words, 0 / 1 / many / thousands of items (pagination or
             virtualization), missing images, and +30% text expansion for localization.
```

## C. Interaction

```text
DS-09 SHOULD One primary action per screen or region. Destructive actions look different, sit apart, and
             are undoable (preferred) or confirmed with the consequence spelled out.
DS-10 MUST   Every action gives feedback within 100 ms (pressed state, inline spinner, optimistic update).
             Operations over ~1 s show progress; over ~10 s let the user keep working or cancel.
DS-11 SHOULD Never make the user re-do work: input survives errors and navigation, defaults are sensible,
             choices are recognized rather than recalled.
DS-12 SHOULD The same thing looks and behaves the same everywhere. Reuse an existing component before
             creating a new one; a new variant of an existing component needs a reason.
```

## D. Accessibility (floor)

```text
DS-13 MUST (floor) Fully operable by keyboard: visible focus indicator, logical tab order, no traps,
             Escape closes overlays, focus returns to the trigger.
DS-14 MUST (floor) Semantic HTML first — button for actions, a for navigation, label for every input,
             headings in order, landmarks. ARIA only fills real gaps and never contradicts native roles.
DS-15 MUST (floor) Images carry alt text (empty alt when decorative); icon-only controls have accessible
             names; color is never the only carrier of meaning (add text, icon, or pattern).
DS-16 MUST   Pointer targets >= 24 x 24 CSS px (WCAG 2.2); primary mobile actions >= 44 x 44.
DS-17 SHOULD Motion is purposeful and short (UI transitions <= 300 ms) and respects
             prefers-reduced-motion. Nothing flashes more than three times per second.
```

## E. Responsive layout and content

```text
DS-18 MUST   Works from 320 px wide to large desktop with no horizontal scrolling of content. The screen
             spec states the layout at each breakpoint.
DS-19 SHOULD Microcopy is plain and specific: buttons are verbs ("Save changes", not "OK"); errors say what
             went wrong and how to fix it, without blame, jargon, or raw codes.
DS-20 SHOULD Visual hierarchy matches importance: the most important information and the primary action
             are the most prominent; headings are scannable and state the point.
```

## F. Process

```text
DS-21 MUST   UI code starts only from an approved prototype and its tokens (R-019-0a-ui). A deviation found
             during build is proposed back to the design owner, not improvised in code.
DS-22 MUST   Design review runs this checklist on the prototype before it is presented for approval; QC
             re-runs DS-04, 06, 07, 13-18 on the built UI and logs failures as bugs.
DS-23 SHOULD Each screen spec states: the user's job on this screen, the primary action, every state
             (DS-06/07), the data shown, the components used, responsive rules, and accessibility notes.
```

## House direction — when the product has no brand yet

When the user brings no brand or design system, Maestro does not hand back a generic template. Its
default direction is **calm, precise, content-first**: the interface recedes and the user's content and
primary action lead. Start from this token baseline in the prototype's `styles.css`, then adapt it to
the product's personality in the Direction gate (and record the choice in the blueprint's `ui_ux`).

```css
:root {
  /* color — neutral surfaces, one confident accent, semantic roles */
  --color-bg: #fbfbfa;        --color-surface: #ffffff;   --color-border: #e6e4df;
  --color-text: #1c1b19;      --color-text-muted: #5f5c55;
  --color-primary: #2f5bea;   --color-primary-contrast: #ffffff;
  --color-success: #1f7a4d;   --color-warning: #9a6200;   --color-danger: #c2362b;
  /* type — system stack, restrained scale */
  --font-sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  --text-sm: 0.875rem; --text-md: 1rem; --text-lg: 1.25rem; --text-xl: 1.5rem; --text-2xl: 2rem;
  --leading-body: 1.5;
  /* space — 4-pt base, 8-pt rhythm */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-6: 24px; --space-8: 32px;
  /* shape and depth — quiet */
  --radius-sm: 6px; --radius-md: 10px;
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06); --shadow-md: 0 4px 12px rgb(0 0 0 / 0.08);
  /* motion — quick, eased out */
  --duration-fast: 120ms; --duration-base: 200ms; --ease-out: cubic-bezier(0.2, 0.8, 0.2, 1);
}
@media (prefers-reduced-motion: reduce) { :root { --duration-fast: 0ms; --duration-base: 0ms; } }
```

Signature habits that make a Maestro UI recognizable regardless of palette:

```text
- Generous whitespace over borders and boxes; one accent color used sparingly for the primary action.
- Real copy and realistic data in prototypes — never lorem ipsum in a screen the user approves.
- Empty states that teach and lead somewhere; error states that offer a way out.
- Numbers right-aligned in tables with units in headers; dates relative when recent, absolute on hover.
- Every interactive element has hover, focus-visible, active, and disabled styles defined in tokens.
```

## Design review checklist (run before presenting a prototype)

```text
[ ] Tokens only (DS-01) and contrast passes in every theme (DS-04)
[ ] Every screen shows loading / empty / error / success; every form shows its states (DS-06/07)
[ ] Stress content tried: long text, many items, missing data (DS-08)
[ ] One primary action per region; destructive actions guarded (DS-09)
[ ] Keyboard path works end to end; focus visible; semantic elements (DS-13/14)
[ ] 320 px and desktop layouts both checked (DS-18)
[ ] Copy is specific and human; no lorem ipsum (DS-19)
[ ] Screen specs complete (DS-23)
```
