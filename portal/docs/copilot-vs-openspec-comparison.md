# Copilot vs OpenSpec -- Comparison and Recommendation

<!-- PUBLISH -->

This page compares GitHub Copilot's native customization system with OpenSpec, a third-party spec-driven workflow framework. Both aim to structure how AI coding agents work, but they approach the problem differently and serve different use cases.

For detailed reference on each system individually, see:

- [GitHub Copilot Customization Guide](github-copilot-customization-guide.md)
- [OpenSpec Customization Guide](openspec-customization-guide.md)

---

## Philosophy Comparison

| Aspect | GitHub Copilot Native | OpenSpec |
|--------|----------------------|---------|
| **Core model** | 6 customization primitives (instructions, prompts, agents, skills, hooks) | Folder-based artifact workflow with YAML schemas |
| **Design philosophy** | Tool-specific, deep integration with VS Code + GitHub | Tool-agnostic, portable across 20+ AI tools |
| **Enforcement model** | Layered: guidance (instructions/agents) + enforcement (hooks) | Guidance only (AI follows instructions, no runtime enforcement) |
| **Artifact structure** | Flexible -- any folder hierarchy, any document format | Fixed -- proposal/specs/design/tasks with dependency ordering |
| **Target workflow** | General purpose -- coding, architecture, documentation, DevOps | Change-driven -- propose, spec, design, implement |

---

## Feature-by-Feature Comparison

### Workflow Structure

| Capability | Copilot Native | OpenSpec |
|-----------|---------------|---------|
| Artifact templates | `.prompt.md` files with frontmatter | `config.yaml` rules with template references |
| Workflow ordering | Manual (instructions describe the process) | Schema-enforced dependency graph |
| Change lifecycle | No built-in lifecycle | Propose -> Spec -> Design -> Tasks -> Archive |
| Progress tracking | None built-in | `/opsx:status` shows current phase |
| Rollback | Git history | `/opsx:rollback` undoes a phase; `/opsx:revert` hard resets |
| Delta tracking | None built-in | ADDED/MODIFIED/REMOVED markers in delta specs |
| Archival | None built-in | `/opsx:archive` merges deltas, locks change |

**Verdict**: OpenSpec provides a more structured change lifecycle with built-in status tracking, rollback, and archival. Copilot relies on manual process and git history for these capabilities.

### AI Guidance Quality

| Capability | Copilot Native | OpenSpec |
|-----------|---------------|---------|
| Workspace-wide context | `copilot-instructions.md` (always loaded) | `config.yaml` context field |
| Task-specific guidance | `.instructions.md` with `applyTo` or `description` | Schema-driven artifact ordering |
| Reusable workflows | `.prompt.md` slash commands | `/opsx:template` + schema definitions |
| Multi-step procedures | Skills (`SKILL.md` with progressive loading) | Slash command sequence (propose -> continue -> archive) |
| Content format enforcement | Instruction prose ("use MADR format") | `config.yaml` rules (advisory, not enforced) |

**Verdict**: Comparable. Copilot's instructions are more flexible (any format, any structure). OpenSpec's schemas provide more structure but less expressiveness.

### Behavioral Specifications

| Capability | Copilot Native | OpenSpec |
|-----------|---------------|---------|
| Given/When/Then scenarios | Not built-in (can be requested in instructions) | Core feature with RFC 2119 keywords |
| Spec organization | Any structure | By domain, with entry points and integration sections |
| Delta specs | Not built-in | ADDED/MODIFIED/REMOVED tracking per field |
| Spec diffing | Git diff | `/opsx:diff` with domain-level granularity |

**Verdict**: OpenSpec is stronger here. Behavioral specs with delta tracking are a genuine differentiator. Copilot can produce Given/When/Then if instructed, but has no built-in delta or spec management.

### Security and Enforcement

| Capability | Copilot Native | OpenSpec |
|-----------|---------------|---------|
| Tool restrictions per agent | `tools` field in `.agent.md` (runtime-enforced per agent) | None |
| Hard enforcement hooks | `PreToolUse` / `PostToolUse` (deterministic shell commands) | None |
| User-level enforcement | `~/.claude/settings.json` (outside repo) | None |
| Org-level governance | GitHub organization admin settings | None |
| Content validation | Instruction compliance (non-deterministic) | Schema validation (file existence only) |
| Permission system | Agent `tools` field + hook `deny` | None |
| Audit trail | GitHub platform-level | None |
| Can developer bypass? | Hooks: NO. Agent restrictions: YES (switch agent) | Everything: YES (ignore instructions) |

**Verdict**: Copilot is substantially stronger. OpenSpec has zero enforcement capabilities. Copilot provides layered enforcement from opt-in guardrails (agent restrictions) to hard enforcement (hooks) to platform governance (org settings).

### Validation

| Capability | Copilot Native | OpenSpec |
|-----------|---------------|---------|
| Schema validation | None built-in | File existence and naming patterns |
| Internal content validation | Via instructions (non-deterministic) | None (schemas do not inspect file contents) |
| Cross-file consistency | None built-in | None |
| MADR format enforcement | Via instructions | Not possible through schemas |
| Cardinality rules | None | None |
| Custom validators | Hooks can run any shell script | Not built-in; requires external CI |

**Verdict**: Both are weak on validation. Copilot hooks CAN run arbitrary validation scripts, giving it an edge, but neither system provides rich content validation out of the box.

### Multi-Tool Portability

| Capability | Copilot Native | OpenSpec |
|-----------|---------------|---------|
| Works across AI tools | No (VS Code / GitHub Copilot only) | Yes (20+ tools: Claude Code, Cursor, Windsurf, etc.) |
| Workflow survives tool migration | No (must recreate customizations) | Yes (same folder structure, same commands) |
| Integration depth with primary tool | Deep (hooks, agent runtime, model selection) | Shallow (instructions-based integration for Copilot) |

**Verdict**: OpenSpec wins decisively on portability. This is its primary value proposition. If you use or plan to use multiple AI tools, OpenSpec provides genuine value here. If you use a single tool, this advantage is unused.

### Architecture-Specific Capabilities

| Capability | Copilot Native | OpenSpec |
|-----------|---------------|---------|
| MADR decision records | Via instructions and templates | No native support |
| Per-service impact assessments | Via instructions and folder conventions | No native support (flat artifact model) |
| Capability tracking (L1/L2/L3) | Via instructions + `capability-changelog.yaml` | No concept of capabilities |
| Risk registers (ISO 25010) | Via instructions | No native support |
| Assumptions register | Via instructions | No native support |
| User story tracking | Via instructions | No native support |
| Cross-service ownership model | In `copilot-instructions.md` | Not expressible in schemas |
| Metadata integration | Portal generators, capability changelog | None (manual post-archive work) |

**Verdict**: Copilot's instruction-based approach is far more flexible for architecture work. OpenSpec's fixed artifact model (proposal/specs/design/tasks) cannot represent the rich artifact set that architecture governance requires. Every architecture-specific need would have to be shoe-horned into OpenSpec's generic structure or handled outside it.

### Developer Experience

| Capability | Copilot Native | OpenSpec |
|-----------|---------------|---------|
| Setup complexity | Zero (files in `.github/`, no install) | npm install + schema definition + config |
| Learning curve | Learn 6 file types and their frontmatter | Learn folder structure, schema YAML, 20+ slash commands |
| IDE integration | Native VS Code (agent picker, `/` commands, context menu) | Via skill/instructions files (less native) |
| Debugging | VS Code Output panel for Copilot logs | Limited (schema validation errors, status command) |
| Dependency footprint | Zero (plain markdown files) | npm package dependency |

**Verdict**: Copilot is simpler. Zero dependencies, native IDE integration, plain markdown files. OpenSpec adds a build dependency and a layer of abstraction.

---

## Maturity Comparison

| Factor | Copilot Native | OpenSpec |
|--------|---------------|---------|
| Backing | GitHub / Microsoft | Fission AI (startup) |
| Governance | GitHub product team | No foundation governance |
| Stability | Evolving but backed by GitHub's platform commitments | v1.2.0, pre-v2.0, breaking changes possible |
| Community | GitHub Copilot's massive user base | 31.5k GitHub stars, growing |
| Sustainability | Tied to GitHub (high confidence) | Unknown (startup with undisclosed funding) |
| Documentation | Official VS Code docs, regularly maintained | Community-driven, evolving |

---

## When to Choose Each

### Choose Copilot Native When

- You are committed to **GitHub Copilot as your primary AI tool**
- You need **architecture-specific artifacts** (MADR, impacts, capabilities, risks)
- You need **enforcement** (tool restrictions, hooks, org-level governance)
- You want **zero dependencies** and plain markdown files
- Your workflow requires **deep IDE integration** (agent picker, model selection)
- You need **metadata integration** with generators, changelogs, and portals

### Choose OpenSpec When

- Your team **uses multiple AI coding tools** (Cursor, Claude Code, Copilot, Windsurf)
- You are doing **feature development** where proposal/spec/design/tasks maps cleanly
- You value **behavioral specs** (Given/When/Then) as a primary deliverable
- You want **delta tracking** for spec evolution
- **Multi-tool portability** is a genuine requirement, not a theoretical one
- Your workflow is **relatively flat** (no deep artifact hierarchies)

### Choose Both When

In theory, OpenSpec and Copilot customizations can coexist -- OpenSpec manages the artifact workflow while Copilot customizations provide enforcement and architecture-specific guidance. In practice, this creates two overlapping systems:

- OpenSpec's `config.yaml` context competes with `copilot-instructions.md`
- OpenSpec's schema-driven ordering competes with instruction-driven process
- OpenSpec's slash commands compete with Copilot's prompt files
- Developers must learn and maintain both systems

The "both" approach is only justified when multi-tool portability is a hard requirement AND architecture-specific enforcement is also needed. For most teams, one system is simpler.

---

## Recommendation

**For this workspace: GitHub Copilot Native customization is recommended. OpenSpec is not adopted.**

OpenSpec solves a problem we do not have. Its primary value proposition is multi-tool portability -- a single customization layer that works across 20+ AI coding platforms. We are not looking to adopt multiple platforms. This workspace uses GitHub Copilot exclusively, and there is no plan or business driver to change that. Adopting OpenSpec would mean taking on a framework dependency, a learning curve, and ongoing maintenance cost to gain portability we will never use.

### Justification

**1. OpenSpec's core differentiator -- multi-tool portability -- provides zero value here.**

OpenSpec exists so that teams using Cursor, Claude Code, Windsurf, Copilot, and other tools can share one set of workflow definitions across all of them. That is a real problem for multi-tool teams. It is not our problem. We use GitHub Copilot. Portability only matters on the day you actually switch tools, and introducing framework complexity today for a theoretical future migration is not a sound trade-off.

**2. Architecture governance requires artifact types OpenSpec cannot represent.**

This workspace produces MADR decision records, per-service impact assessments, capability tracking with L3 emergence, risk registers against ISO 25010, assumption registers, guidance documents, and user stories. OpenSpec's proposal/specs/design/tasks model has no place for these. Every architecture-specific artifact would need to be built as custom tooling on top of OpenSpec, negating the benefit of using a framework.

**3. Content enforcement is a requirement, not a nice-to-have.**

OpenSpec schemas validate file existence only. This workspace needs content structure enforcement: MADR format with 2+ options, impact assessments that stay separate from implementation guidance, capability changelog entries in a specific YAML format. Copilot's instruction-based approach (non-deterministic but effective) combined with hooks (deterministic) provides this. OpenSpec provides neither.

**4. OpenSpec adds a dependency without proportional value.**

OpenSpec requires an npm package, a schema definition, and a configuration file. The workspace currently operates with zero dependencies (plain markdown files in `.github/`). Every feature OpenSpec provides is either unnecessary (portability), insufficient (validation), or already achievable more directly (workflow guidance via instructions).

**5. Maturity risk is unacceptable for architecture infrastructure.**

OpenSpec is v1.2.0, backed by a startup (Fission AI) with no foundation governance. Breaking changes are possible. The workspace's architecture customization system is foundational infrastructure -- it should not depend on a pre-v2.0 framework from an entity with unknown sustainability.

### When to Revisit

This recommendation should be revisited if any of these conditions become true:

1. **The team adopts a second AI coding tool** -- multi-tool portability becomes a real requirement
2. **OpenSpec adds architecture-specific features** -- MADR templates, capability tracking, metadata hooks
3. **OpenSpec achieves foundation governance** -- joins FINOS, Linux Foundation, or equivalent
4. **Workflow enforcement becomes a persistent pain point** despite instruction improvements

Until then, the native Copilot customization system (`.instructions.md` + `.prompt.md` + `.agent.md` + hooks) provides a simpler, more capable, and more maintainable approach for this workspace's architecture governance needs.

---

## Further Reading

- [GitHub Copilot Customization Guide](github-copilot-customization-guide.md) -- complete reference for all 6 Copilot customization primitives
- [OpenSpec Customization Guide](openspec-customization-guide.md) -- complete reference for OpenSpec's file structure, schemas, and commands
- [OpenSpec Analysis and Decision](research/OPENSPEC-ANALYSIS.md) -- full research findings
- [OpenSpec Evaluation Plan](research/OPENSPEC-EVALUATION-PLAN.md) -- PoC evaluation criteria (not executed)
