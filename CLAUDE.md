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

<!-- tsift:code-navigation v=0.1.62 -->
## Code Navigation

Run `tsift status` at session start from the owning repo root. If the task or file lives under a git submodule (for example `src/tsift/...`), switch to that submodule root first so the harness loads the narrower local instructions and repo state instead of the superproject root. If status prints a `run:` recommendation for stale or missing tsift state, run `tsift status --fix` before relying on tsift results; when the harness cannot perform write commands, ask the user to run the printed command instead. Codex projects can install a prompt-time auto-reindex hook with `tsift init --codex`; OpenCode projects can install per-project tsift command shortcuts with `tsift init --opencode`.

Use the commands listed in its `use:` output:
- `tsift --envelope search <query> --budget normal` — AST-aware hybrid search preview (prefer over grep/rg)
- `tsift --envelope explain <symbol> --budget normal` — callers, callees, community preview
- `tsift graph <symbol> --callers` / `--callees` — call graph navigation
- `tsift summarize <symbol>` — cached summary (only when listed in `use:`)
- `tsift workflow search` — ordered exact/search/explain/summarize/digest recipe that preserves result handles across expansions

When a search envelope includes `report.scale_guard`, run one of its `narrow_commands` before dispatching parallel agents. The guard means the original result set or corpus is broad enough that fan-out should start from a narrower cited handle, path, or exact query.

Prefer bounded digest commands over raw transcript, diff, and verbose-log reads:
- `tsift --envelope session-review <path> --next-context --budget normal` or `tsift --envelope context-pack <path> --budget normal` instead of replaying long session docs, JSONL transcripts, or agent-doc runtime logs with `cat`, `tail`, or `sed`.
- `tsift diff-digest [path]` (`--cached`, `--revision <rev>`) instead of `git diff`, `git show`, or patch-style `git log`.
- `tsift --envelope __digest-runner --kind test --path . --shell-command '<test command>'` / `tsift --envelope __digest-runner --kind log --path . --shell-command '<build command>'` for noisy test/build/install output, or let the rewrite/hooks create those artifact-backed envelopes for `cargo test`, `pytest`, and verbose cargo commands.
- If RTK is installed, digest-runner delegates supported generic command families through `rtk rewrite` and records the chosen compact filter in `report.filter` while preserving tsift artifact handles.
- Codex, OpenCode, and other harnesses without Claude-style `PreToolUse` hooks should run `tsift rewrite --run '<command>'` before broad `rg`/recursive grep, raw transcript/session/log reads, `git diff`/`git show`/single-patch `git log`, `cargo test`/`pytest`, and cargo build/check/clippy/install commands so the same search, session-digest, diff-digest, and digest-runner rewrites apply manually. OpenCode can install this path as `/tsift-rewrite-run` with `tsift init --opencode`.

For local verification, run `make check` before committing. After local changes, check the latest GitHub Actions CI run with `gh run list --workflow CI --limit 1` and fix any failing tests before calling the work complete.

Only read full source files when tsift results are insufficient.
<!-- /tsift:code-navigation -->
