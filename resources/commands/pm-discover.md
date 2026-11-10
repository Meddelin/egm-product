---
description: Discover repository capabilities, data schemas, UI tokens, and product metrics (PRODUCT_CONTEXT.md & METRICS.md)
---

Execute the **Stage 1: Assisted Product & Metric Discovery (`pm-discover`)** workflow:

1. Read and follow [`../../skills/pm-discover/SKILL.md`](../../skills/pm-discover/SKILL.md) and [`../execution_instructions.md`](../execution_instructions.md) (located inside the `egm-product` extension/plugin directory).
2. Perform the single-pass read-only repository scan to generate/refresh `.pm/schemas.md` (max 400 lines) and `.pm/ui_tokens.md` (max 200 lines).
3. Interview the Product Manager one question at a time for any `[NEEDS_PM_INPUT]` fields and write `PRODUCT_CONTEXT.md` (max 300 lines) and `METRICS.md` (max 300 lines) conforming to [`../templates/product_context.template.md`](../templates/product_context.template.md) and [`../templates/metrics.template.md`](../templates/metrics.template.md).

Additional user arguments/context: `{{args}}`
