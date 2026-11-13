---
description: Generate and audit a zero-build standalone HTML/CSS/JS prototype from an approved PRD using product UI tokens and pm-ux-flows
---

Execute **Stage 4: Zero-Build Interactive HTML Prototyping (`pm-prototype`)**:

1. Read and follow [`../../skills/pm-prototype/SKILL.md`](../../skills/pm-prototype/SKILL.md) and [`../pm_execution_instructions.md`](../pm_execution_instructions.md).
2. Generate `docs/product/<feature-slug>/prototype.html` (max 400 lines, zero external network requests, 4 switchable UX states + conditional `Role` switcher when `>= 2` roles diverge) using `.pm/ui_tokens.md`, and verify craft via `pm-ux-flows` (`Mode: PROTOTYPE_AUDIT`).

Additional user arguments/context: `{{args}}`
