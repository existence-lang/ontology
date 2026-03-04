# Existential Kernel -- Ontology

Canonical domain ontology. Defines terms in `src/`, each following the structure in [SPEC.md](SPEC.md).

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
