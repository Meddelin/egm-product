# Claude Code & Cowork Integration (`egm-product`)

Use Claude Code `2.1.271` or later for `omitClaudeMd: true` support on Product Goldfish subagent adapters.

## 1. Installation & Namespaced Commands

```sh
claude plugin marketplace add Meddelin/egm-product
claude plugin install egm-product@egm-product
claude plugin enable egm-product@egm-product
```

Invoke the 4-stage product pipeline using the plugin namespace:
* `/egm-product:pm-discover`
* `/egm-product:pm-brainstorm`
* `/egm-product:pm-prd` *(drafting + built-in 4+1 Product Goldfish review)*
* `/egm-product:pm-prototype`

All skills set `disable-model-invocation: true`. Claude Code's `Skill` tool refuses skills with `disable-model-invocation: true`, so whenever one `pm-*` skill transitions to another (for example, `pm-brainstorm` handing off to `pm-prd`, or `pm-prd` handing off to `pm-prototype`), read `${CLAUDE_PLUGIN_ROOT}/skills/<target>/SKILL.md` directly and follow it in the main thread instead of calling `Skill`.

## 2. Plugin Cache Resource Resolution & Read Permissions

Claude substitutes `${CLAUDE_PLUGIN_ROOT}` inside skill and adapter bodies. Always use `${CLAUDE_PLUGIN_ROOT}` to resolve `agents/`, `resources/`, `docs/`, and sibling `skills/`, while resolving `PRODUCT_CONTEXT.md`, `METRICS.md`, optional `COMPANY_CONTEXT.md`, `.pm/ui_tokens.md`, and `docs/product/<feature-slug>/` against the user's workspace. Pass resolved absolute paths to every spawned Goldfish subagent.

Grant read-only access to the plugin's resource directories in `/permissions` for uninterrupted background Goldfish runs:

```text
Read(//absolute/plugin/path/agents/**)
Read(//absolute/plugin/path/docs/**)
Read(//absolute/plugin/path/resources/**)
Read(//absolute/plugin/path/skills/**)
```

On Windows, use either a leading `//` with a lowercase drive letter (no colon) or native backslashes, replacing the version segment with `*`:

```text
Read(//c/Users/<you>/.claude/plugins/cache/egm-product/egm-product/*/agents/**)
Read(//c/Users/<you>/.claude/plugins/cache/egm-product/egm-product/*/docs/**)
Read(//c/Users/<you>/.claude/plugins/cache/egm-product/egm-product/*/resources/**)
Read(//c/Users/<you>/.claude/plugins/cache/egm-product/egm-product/*/skills/**)
```

## 3. Expected Advisory Notice (`Default agents/ folder is ignored`)

In `/plugin` > Errors, Claude Code reports:

```text
Default agents/ folder is ignored because the manifest sets "agents"
```

This advisory is expected. `agents/` holds harness-agnostic personas, while `.claude-plugin/agents/` holds thin Claude adapters declaring `tools: [Read, Grep, Glob]` and `omitClaudeMd: true`.

## 4. Subagent Isolation & Artifact Directory Override

* **Claude Code & Cowork Dispatch**: Dispatch the 4 Phase 1 product critics (`egm-product:pm-value-strategy`, `egm-product:pm-ux-flows`, `egm-product:pm-metrics-experiment`, `egm-product:pm-business-logic`) directly from the main Elephant context in parallel, then dispatch `egm-product:pm-synthesizer` sequentially in Phase 2.
* **Scratch Override**: If the prompt, `CLAUDE.md`, or `AGENTS.md` contains `EGM artifact directory: <path>`, write working review reports (`pm_review_report.md` and scratch files) to `<path>` (resolved relative to the workspace root).
