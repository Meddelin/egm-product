---
description: Map product strategy, company context, empirical user roles, Jobs-to-be-Done, UI App Shell & design tokens, and product metric tree
---

Execute **Stage 1: Product, Role, UI Shell & Metric Discovery (`pm-discover`)**:

1. Read and follow [`../../skills/pm-discover/SKILL.md`](../../skills/pm-discover/SKILL.md) and [`../pm_execution_instructions.md`](../pm_execution_instructions.md) (inside the `egm-product` extension/plugin directory).
2. Delegate the read-only user-surface, App Shell & CSS-token scan to `pm-product-scanner` (honoring optional `--scope <subdir>` and `--context <path>` / `COMPANY_CONTEXT.md`) without scanning DB schemas or backend internals, then write `.pm/ui_tokens.md`.
3. Interview the Product Manager one open-ended question at a time (`Zero Assumed Personas`) and write `PRODUCT_CONTEXT.md` and `METRICS.md` conforming to [`../templates/product_context.template.md`](../templates/product_context.template.md) and [`../templates/metrics.template.md`](../templates/metrics.template.md).

Additional user arguments/context: `{{args}}`
