---
name: frontend-design-system
description: Apply the user's theme-first frontend design system to UI work. Use whenever a task creates, edits, restyles, reviews, or diagnoses HTML/CSS, React/Vue UI, dashboards, workspaces, visual reports, components, color palettes, typography, spacing, responsive layout, or screenshot-based visual references. Use for both small visual fixes and full redesigns; preserve existing project language for small changes and perform theme extraction before new-page or redesign work.
---

# Frontend Design System

Use `references/design-playbook.md` as the canonical global design guidance. Read the full reference for a new page, a redesign, a multi-page system, or when the user supplies screenshots or visual references. For a local color, spacing, typography, or component change, read the relevant sections and first inspect the existing project UI, token files, and component styles.

## Task Scale

- Local adjustment: preserve the project's visual language and make the narrowest change that fixes the request. Do not redefine the palette or restructure the page.
- Component adjustment: preserve the page, complete the component's spacing, states, accessibility, and responsive behavior.
- New page or redesign: complete internal product understanding, theme extraction, 2-3 visual directions, a chosen direction, token decisions, implementation, and visual QA before delivery.
- Multi-page system: use the four layers in the reference: Tokens, Layout Primitives, Components, and Templates. Fix consistency problems at the highest affected layer.

## Workflow

1. Read project-local `AGENTS.md`, `DESIGN.md`, brand rules, screenshots, existing UI, tokens, and component styles before changing UI. Project-local rules override this skill.
2. Determine the product type, audience, density, task scale, and whether the request is local or systemic.
3. Derive visual choices from the product's theme and evidence. Do not reuse a familiar palette or layout as a default answer.
4. Reuse existing tokens and components when they exist. If a new semantic visual value is necessary, define it at the correct system layer instead of hard-coding it in a page.
5. Preserve real content and interaction behavior. Give interactive elements complete states and meet accessibility, responsive, and overflow requirements.
6. Render or preview when the environment permits. Check the first viewport, actual content overflow, mobile layout, visible focus, and state changes.
7. Keep the user-facing response brief unless they request the design rationale.

## Visual Evaluation Artifacts

Choose the comparison artifact that matches the question. Keep every compared output at the same viewport and preserve the screenshots beside the delivered HTML.

### Design-evolution comparator

When the user is evaluating a new `DESIGN.md`, design Skill, visual prompt, or design-system rule set, compare the **same task** across the rule versions. This is not a before/after page diff.

1. Render `Original common output`: the task without the new design guidance.
2. Render `Old DESIGN.md output`: the task using the preceding rule set, if one exists.
3. Render `New DESIGN.md output`: the task using the current rule set.
4. Build one self-contained `design-evolution.html` that directly renders and switches between those complete live UI outputs. Its tabs must name the rule variants, not individual page names.

- The comparison surface must render actual DOM and remain interactive. Do not use screenshots, raster images, iframes, or separate HTML documents as the comparison content; use screenshots only for internal visual QA.
- Implement the variants in the same document through a `mode` state, shared scenario data, and explicit render functions or framework routes. This preserves offline `file://` behavior and lets the user inspect typography, spacing, controls, focus, and state changes directly.
- Keep the product content, data, viewport, and test scenario identical across variants. Change only the design guidance being evaluated.
- Use the three variants above whenever an old rule set exists. If there is no old rule set, compare the baseline and current rules and state that the middle historical variant is unavailable.
- Do not relabel a page-by-page before/after diff as a design-evolution comparison.

### Before-and-after comparator

For a redesign, multi-page system migration, or explicit visual-update request that is about implementation changes rather than a rule-set evaluation, capture the original state before editing and the final state after editing. Generate a clickable `comparison.html` with `scripts/create_visual_comparator.py`.

```powershell
python <skill-dir>/scripts/create_visual_comparator.py `
  --output <output-dir>/comparison.html `
  --title "Updated UI comparison" `
  --pair "Workspace|<before.png>|<after.png>"
```

- Repeat `--pair` for multiple pages, or use `--manifest` with a JSON `pairs` array.
- Do not generate either comparison artifact for a trivial isolated change unless the user explicitly requests it.

## Cross-Page Integrity Gate

When a task belongs to an existing product with two or more related UI pages, treat the product as one rendered system before editing an individual page.

1. Inspect representative sibling pages and identify the shared token file, AppShell, navigation, PageHeader, primary Button, and type scale.
2. Require every related page to use the same shared system. A page that uses an alternate top navigation, an alternate sidebar, a page-local palette, a page-local H1 size, or a page-local primary button is outside the system.
3. Keep PageHeader slots consistent: eyebrow, H1, lead, and actions. Do not insert page-local KPI blocks, filter callouts, or alternate navigation into the header unless the shared component explicitly supports that variant.
4. Keep H1 on the product's `--fs-h1`, `--lh-h1`, and letter-spacing tokens. Do not override these values in page CSS. Scan non-token CSS for `font-size` pixel literals before delivery; token-definition and third-party files are the only permitted exceptions.
5. Keep the primary action visually identical across related pages. Use ghost or secondary buttons only for subordinate actions, never as a substitute for the page's primary CTA.
6. Choose one content-container grammar per section: a true card grid with shared padding and gaps, or a true list with shared row height. Do not mix list separators with card framing.
7. If a page cannot be brought into compliance through shared tokens and components, rebuild it from the product's template instead of adding visual overrides.
8. Before delivery, render the related pages side by side at the same viewport. Compare AppShell geometry, H1 computed size, PageHeader order, primary-button computed colors, and primary accent token. Treat any unintended difference as a system-layer defect.

## Guardrails

- Do not turn a local adjustment into a redesign.
- Do not make every product look like the same warm-neutral, dark-terminal, gradient, glass-card, or three-column template.
- Do not use color as decoration: accent and chip colors must retain semantic roles.
- Do not leave empty states, loading states, error states, or keyboard focus as afterthoughts when the UI needs them.
- Do not copy proprietary assets or layouts from a visual reference. Extract its visual language and recombine it for the current product.
