---
description: Map product strategy, company context, empirical user roles, UI design tokens, and product metric tree (PRODUCT_CONTEXT.md & METRICS.md)
---

Execute **Stage 1: Product, Role & Metric Discovery (`pm-discover`)**:

1. Read and follow [`../../skills/pm-discover/SKILL.md`](../../skills/pm-discover/SKILL.md) and [`../pm_execution_instructions.md`](../pm_execution_instructions.md) (inside the `egm-product` extension/plugin directory).
2. Delegate the light read-only user-surface & CSS-token overview to `pm-product-scanner` (honoring optional `--scope <subdir>` and `--context <path>` / `COMPANY_CONTEXT.md`) without scanning DB schemas or backend internals, then write `.pm/ui_tokens.md` (max 150 lines).
3. Interview the Product Manager one open-ended question at a time (`Zero Assumed Personas`) and write `PRODUCT_CONTEXT.md` (max 250 lines) and `METRICS.md` (max 200 lines) conforming to [`../templates/product_context.template.md`](../templates/product_context.template.md) and [`../templates/metrics.template.md`](../templates/metrics.template.md).

Additional user arguments/context: `{{args}}`
