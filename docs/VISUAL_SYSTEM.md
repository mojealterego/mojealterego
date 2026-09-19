# MOJEALTEREGO — GITHUB VISUAL SYSTEM

## Palette

- Obsidian: `#050607`
- Deep graphite: `#0B1114`
- 24K Gold: `#C9A45C`
- Teal: `#2A8D97`
- Ivory: `#F5EBDD`
- Titanium: `#B6C0C2`

## Typography

Use an editorial serif for project titles and a restrained sans-serif for technical metadata.

Recommended hierarchy:
1. Brand title — editorial serif
2. Project title — editorial serif
3. Metadata — sans-serif, uppercase, generous tracking
4. Body — readable sans-serif
5. Quotes — italic serif

## Image language

Every visual should communicate one of:
- identity
- product
- architecture
- workflow
- result

Preferred:
- dark cinematic compositions
- documentary photography
- precision lighting
- restrained gold highlights
- cool teal technical light
- geometric overlays
- large negative space

Avoid:
- generic neon AI stock art
- noisy collages
- random gradients
- fake dashboards presented as real product screenshots
- fabricated metrics
- imagery unrelated to the repository

## Asset hierarchy

```text
Profile README
  └── hero banner

Repository
  ├── social preview
  ├── README hero
  ├── architecture diagram
  ├── screenshots
  └── demo/result imagery

GitHub Lists
  └── category icon / visual
```

## Naming

```text
assets/
  mojealterego-banner.svg
  project-mini-mobile-7.svg
  project-jarvis-2.svg
  project-wda-photo-agent.svg
  project-omnimass-advanced.svg
  project-knowledge-projects.svg
  project-ccr-world.svg
  project-agentic-cinema.svg
```

## Technical rule

SVG is used here because the current GitHub connector can write UTF-8 text files directly. Raster PNG/JPG assets remain separate deliverables; they should only be committed through a binary-capable upload path.
