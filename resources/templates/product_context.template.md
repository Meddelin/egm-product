---
schema_version: "1.0"
generated_at_commit: "<git-sha-or-UNCOMMITTED>"
generated_at_timestamp: "<YYYY-MM-DDTHH:MM:SSZ>"
---

# Product Context Contract (`PRODUCT_CONTEXT.md`)

> **Contract Cap**: Maximum 300 lines (~3,500 tokens). Re-running `/pm-discover` refreshes `## Machine-Discovered Context (Auto-Refreshed)` and the `.pm/` catalogs while preserving `## Human-Curated Strategy (Preserved Across Runs)`.

---

## Machine-Discovered Context (Auto-Refreshed)

### 1. Owned Capabilities & Service Surface
*   **Primary Entrypoints & Routes**:
    *   `[path/to/router_or_controller:line]` — `<HTTP/gRPC/CLI route summary>`
*   **Core Domain Modules & Background Workers**:
    *   `[path/to/service_module:symbol]` — `<Owned business logic and state mutation capabilities>`
*   **Storage & Index Layers**:
    *   `[path/to/db_or_index_config:line]` — `<Primary databases, vector/search indexes, caches>`

### 2. Upstream Producers & Downstream Consumers
*   **Upstream Data/Event Producers**:
    *   `<External service, ingestion pipeline, or webhook>` (`[file:symbol_or_line]`) — `<Payloads consumed and schema contract>`
*   **Downstream API/Event Consumers**:
    *   `<Internal clients, SDKs, or partner services>` (`[file:symbol_or_line]`) — `<Exported endpoints/events and compatibility guarantees>`

### 3. Tech Stack, Auth & Observability
*   **Runtime & Frameworks**: `<Language, web framework, UI framework, build toolchain>`
*   **Authentication & RBAC/ACL Model**: `<Auth middleware, tenant isolation key, retrieval-time or route-level permission checks>` (`[file:symbol_or_line]`)
*   **Feature Flags & Rollback Mechanism**: `<Flag provider, config env var, or routing toggle>` (`[file:symbol_or_line]`)
*   **Logging, Tracing & Analytics Client**: `<Telemetry SDK/wrapper and sink>` (`[file:symbol_or_line]`)

### 4. On-Demand Catalog Pointers
*   **Data & API Schema Index**: `.pm/schemas.md` (capped at 400 lines; flat table: `| Entity / Model Name | Source File & Line Range | Key Fields & Types | Relations / Notes |`)
*   **UI Design Token Catalog**: `.pm/ui_tokens.md` (capped at 200 lines; normalized `:root` CSS custom properties `--pm-surface-0..3`, `--pm-text-primary`, `--pm-text-secondary`, `--pm-accent`, `--pm-border`, `--pm-radius-*`, `--pm-space-*`, `--pm-font-*`)

---

## Human-Curated Strategy (Preserved Across Runs)

### 1. Product Identity & Strategic Archetype
*   **Product Summary**: `[NEEDS_PM_INPUT: 1–3 sentence description of the product and core value proposition]`
*   **Strategic Archetype**: `[NEEDS_PM_INPUT: Select one -> INTERNAL_TOOL | INTERNAL_PLATFORM_SERVICE | B2B_COMMERCIALIZATION_CANDIDATE]`
*   **Commercialization / Multi-Tenant Posture**: `[NEEDS_PM_INPUT: Strictly internal single-org OR must preserve tenant isolation, configurable branding, and bounded unit economics for future B2B spinout]`

### 2. Target Personas & Jobs-to-be-Done
*   **Primary Persona**: `[NEEDS_PM_INPUT: Role, workflow frequency, and primary pain point]`
*   **Secondary / Admin Persona**: `[NEEDS_PM_INPUT: Operational, support, or governance persona]`

### 3. Team & Cross-Functional Ownership Boundaries
*   **Directly Owned by This Team (`READY_NOW` / `ADAPT_NOW` Boundary)**: `[NEEDS_PM_INPUT: Services, tables, and UI surfaces this team can ship without external sprint dependencies]`
*   **External Team Dependencies (`BLOCKED_NOW` Boundary)**: `[NEEDS_PM_INPUT: Upstream data producers, platform infra, or security/legal approvals owned by other teams]`
