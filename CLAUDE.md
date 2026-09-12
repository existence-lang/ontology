# Existence Lang -- Ontology

Canonical domain ontology with 114 term files across 3 rings. Defines terms in `src/`, each following the structure in [SPEC.md](SPEC.md).

## Ring 0 -- Kernel (always loaded)

These 14 terms define the existential scope. Apply these definitions whenever these terms appear in conversation.

**Ontology chain:** Existence -> Entity -> System -> Domain -> Scope -> Context -> Resolution -> Focus

| Term | Definition |
|------|------------|
| **Existence** | Everything that 'is'; the universal set containing all entities. |
| **Entity** | Any information in Existence -- abstractions, persons, systems, objects. |
| **Abstraction** | A concept modeling something else without its complexity; enables perspective. |
| **Scope** | Breadth, depth, or reach of a perspective; bounds what's relevant. |
| **Context** | Scope applied to abstractions; limits information needed for coherent systems. |
| **Resolution** | Level of detail and granularity; zoom in/out to observe patterns. |
| **Pattern** | Elements that repeat in a predictable manner; transferable across domains. |
| **System** | A collection of organized things; a whole of relationships among its members. |
| **Domain** | The system of interest within an entity, with associated language. |
| **Focus** | Finite attention applied to a scope; enables efficient energy use. |
| **Perspective** | A viewpoint on a system; influences reality; all entities have one. |
| **Consciousness** | An entity's ability to interpret relevant signals; being present. |
| **Evolution** | How an entity alters in response to context; the universal pattern of change. |
| **Story** | A sequence of events holding state that creates context; how meaning is communicated. |

## Ring 1 -- Software

The DDD bridge -- 17 terms immediately useful for software projects.

| Term | Definition |
|------|------------|
| **Project** | A scoped endeavor within a domain to achieve a specific outcome. |
| **Model** | An entity used to exemplify or simulate the workings of a subject system. |
| **Algorithm** | A precise step-by-step plan for a procedure with input and output. |
| **State** | The condition of the Entity and its members. |
| **Type** | A grouping based on shared characteristics; a class. |
| **Definition** | A statement of the meaning of an Abstraction. |
| **Information** | That which can distinguish one thing from another. An Entity. |
| **Signal** | Useful information, as opposed to noise. Transmits between entities. |
| **Language** | The system used by an entity to communicate abstractions via signals. |
| **Tool** | Conceptual or physical system used to create a desired effect. |
| **Environment** | The surroundings of, and influences on, a particular Entity. |
| **Coherence** | Entities acting in unison and agreement with themselves and each other. |
| **Communication** | An Entity using signals and language to affect another entity. |
| **Collective** | A group of Entities. The Collective is an entity. |
| **Integrity** | Ability of an Entity to adhere to a chosen philosophy. |
| **Qualitative** | *(pending)* |
| **Quantitative** | *(pending)* |

## Ring 2 -- Extended (85 terms)

Broader ontological terms spanning philosophy, spirituality, cognition, linguistics, and more. These files exist in `src/` but are not assigned to Ring 0 or Ring 1. Examples include: `ontology`, `epistemology`, `axiology`, `ethics`, `philosophy`, `god`, `soul`, `consciousness` derivatives (`awareness`, `attention-schema`, `expanding-consciousness`, `unconsciousness`), system variants (`abstract-system`, `conceptual-system`, `physical-system`, `control-system`), and many others.

See [README.md](README.md) for the full Ring 2 term list.

## DDD Mapping

| DDD Concept | Kernel Terms | How it derives |
|-------------|-------------|----------------|
| Ubiquitous Language | language + domain | Scoped vocabulary grounded in the domain model |
| Bounded Context | scope + context | Limits information for a coherent system |
| Entity | entity | Identity-bearing object (DDD narrows kernel's broader definition) |
| Aggregate | system | A whole of relationships, internally consistent |
| Domain Event | evolution + signal | State change that triggers responses |
| Model | model | Abstraction of a domain |
| Value Object | state + type | Defined by attributes, not identity |

## Usage

When these terms appear in conversation, apply the canonical definitions above. Definitions start broad (Existence scope) and narrow by context. For full node definitions, read `src/{term}.md`.

**Domain overlays:** Downstream repos extend this base ontology in their own `CLAUDE.md` with a `## Domain Ontology` section. Overlay terms reference base concepts they extend.

<!-- tsift:code-navigation v=0.1.96 -->
## Code Navigation

Run `tsift status` at session start from the owning repo root. If the task or file lives under a git submodule (for example `src/tsift/...`), switch to that submodule root first so the harness loads the narrower local instructions and repo state instead of the superproject root. `tsift status` repairs the `.tsift/` index state it owns and never rewrites tracked files (`--no-fix` skips even that). If status reports stale or missing instructions, run `tsift init` to refresh the tracked Code Navigation block and runbook; it names every tracked file it rewrites or moves. When the harness cannot perform write commands, ask the user to run the printed `run:` command instead.

Prefer tsift envelopes over raw reads:
- `tsift --envelope search <query>` instead of `grep`/`rg`
- `tsift --envelope source-read <file>` / `tsift --envelope symbol-read <symbol>` instead of raw `cat`/`head`/`tail`/`sed`/`less` source reads
- `tsift --envelope explain <symbol>` and `tsift graph <symbol> --callers` / `--callees` for call graphs
- `tsift diff-digest [path]` (`--pathspec <pathspec>` to preserve scoped reviews) instead of `git diff`, commit-form `git show`, or patch-style `git log`; blob-form `git show <rev>:<path>` stays a raw object read
- `tsift --envelope session-review <path>` / `tsift --envelope context-pack <path>` instead of replaying long session docs or transcripts
- raw-read rewrites route recognized session docs/transcripts to `tsift session-digest --input <path>` and captured logs to `tsift log-digest --input <path>`
- `tsift --envelope digest-runner --kind test|log --path . --shell-command '<command>'` instead of raw test/build output

Command detail lives in [`.agent/runbooks/code-navigation.md`](.agent/runbooks/code-navigation.md) — budgets, `tsift workflow search`, `report.scale_guard` handling, the harness rewrite path for `PreToolUse`-less harnesses, and Codex/OpenCode integration. `tsift init` writes and versions that runbook alongside this block, so it is present in every initialized checkout; read it before broad exploration instead of expanding this block. A repository that also ships a current `.claude/skills/tsift/SKILL.md` should use that skill as the deeper source.

After local changes, check the latest GitHub Actions CI run with `gh run list --limit 1` and fix any failing tests before calling the work complete.

Only read full source files when tsift results are insufficient.
<!-- /tsift:code-navigation -->
