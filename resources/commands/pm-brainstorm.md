---
description: Stress-test a feature idea with the 4+1 PM Goldfish swarm and write docs/product/<slug>/opportunity_brief.md
---

Execute the **Stage 2: Opportunity Brainstorming & 4+1 Reality Check (`pm-brainstorm`)** workflow:

1. Read and follow [`../../skills/pm-brainstorm/SKILL.md`](../../skills/pm-brainstorm/SKILL.md), [`../execution_instructions.md`](../execution_instructions.md), and [`../../docs/harnesses.md`](../../docs/harnesses.md) (located inside the `egm-product` extension/plugin directory).
2. Preserve the user's initial feature request (`{{args}}`), verify `PRODUCT_CONTEXT.md` and `METRICS.md` (triggering the Inline Bootstrap Recovery Gate via `pm-discover` if missing), clarify the problem statement and metric causal chain, and dispatch the 4 + 1 PM Goldfish swarm (`pm-value-metrics`, `pm-tech-lead`, `pm-data-eval`, `pm-ux-risk` -> `pm-scope-slicer`).
3. Write `docs/product/<feature-slug>/opportunity_brief.md` conforming to [`../templates/opportunity_brief.template.md`](../templates/opportunity_brief.template.md) and present the Scope Triage Gate.

Feature request / arguments: `{{args}}`
