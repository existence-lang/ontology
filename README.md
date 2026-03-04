# Existential Kernel -- Ontology

A domain ontology organized in concentric rings. Ring 0 is the universal kernel -- 14 terms that model Existence at the broadest scope. Ring 1 bridges the kernel to software engineering via Domain-Driven Design concepts.

Terms are defined as interconnected nodes in `src/`. Each node follows the structure in [SPEC.md](SPEC.md): **Ontology** (what it is), **Axiology** (why it matters), **Epistemology** (how we know it).

## Ring Structure

```
Ring 0 (kernel)    -- 14 universal terms, always loaded
Ring 1 (software)  -- 17 terms bridging to DDD and software domains
Ring 2+ (future)   -- domain-specific extensions
```

Rings are additive. Ring 1 assumes Ring 0. Higher rings assume all lower rings. See [`ring.toml`](ring.toml) for the canonical ring definitions.

## Ring 0 -- Kernel (14 terms)

The existential scope. These terms apply universally across all domains.

| Term | Definition |
|------|------------|
| [existence](src/existence.md) | Everything that 'is', or more simply, everything. A scoped Existence represents an Entity's perspective on Existence. |
| [entity](src/entity.md) | Any information in Existence. Entities can be abstractions, concepts, persons, systems, objects, collectives, or Existence itself. |
| [abstraction](src/abstraction.md) | A concept that models something else, allowing expression without its complexity and ambiguity. A word or phrase is an abstraction. |
| [scope](src/scope.md) | The breadth, depth, or reach of an Entity; a domain. |
| [context](src/context.md) | Context adds scope to abstractions. Limits the amount of information needed to create a coherent system. |
| [resolution](src/resolution.md) | The detail and scope of the perspective. Detail is increased with evolution. |
| [pattern](src/pattern.md) | The elements of a pattern repeat in a predictable or regular manner. |
| [system](src/system.md) | A collection of organized things; a whole composed of relationships among its members. |
| [domain](src/domain.md) | The system of interest within an entity. A domain has a language that refers to its field and actions. |
| [focus](src/focus.md) | Selectively concentrating on one system of Existence while ignoring other things. |
| [perspective](src/perspective.md) | The relations that an Entity has to the containing entity (Existence is the assumed context). |
| [consciousness](src/consciousness.md) | The Entity's ability to interpret relevant signals, or the ability of being present within an Entity. |
| [evolution](src/evolution.md) | The altering of an Entity or lineage of Entities as a learned response to the environment. |
| [story](src/story.md) | A sequence of events; or, an account of such a sequence. Stories hold state that can be used for context. |

### Ontology Chain

```
Existence -> Entity -> System -> Domain -> Scope -> Context -> Resolution -> Focus
```

## Ring 1 -- Software (17 terms)

The DDD bridge -- immediately useful for software projects. These terms extend Ring 0 into the software engineering domain.

| Term | Definition |
|------|------------|
| [project](src/project.md) | A scoped endeavor within a domain to achieve a specific outcome. A system with temporal boundaries. |
| [model](src/model.md) | An entity used to exemplify or simulate the workings of the subject system. |
| [algorithm](src/algorithm.md) | A precise step-by-step plan for a procedure that possibly begins with an input value and yields an output value in a finite number of steps. |
| [state](src/state.md) | The condition of the Entity and its members. |
| [type](src/type.md) | A grouping based on shared characteristics; a class. In type theory, every term has a type. |
| [definition](src/definition.md) | A statement of the meaning of an Abstraction. |
| [information](src/information.md) | That which can distinguish one thing from another. An Entity. |
| [signal](src/signal.md) | Useful information, as opposed to noise. A signal transmits information from one entity to another. |
| [language](src/language.md) | The system used by an entity to communicate abstractions by using signals. |
| [tool](src/tool.md) | Conceptual or Physical System used to create a desired effect on another System or itself. |
| [environment](src/environment.md) | The surroundings of, and influences on, a particular Entity. The Environment is also an Entity. |
| [coherence](src/coherence.md) | A set of one to many Entities acting in unison and agreement with themselves and each other. |
| [communication](src/communication.md) | An Entity using signals and language to affect another entity. |
| [collective](src/collective.md) | A group of Entities. The Collective is an entity. |
| [integrity](src/integrity.md) | Ability of an Entity to adhere to a chosen philosophy. Promotes trust and predictability. |
| qualitative | *(pending -- not yet defined)* |
| quantitative | *(pending -- not yet defined)* |

## DDD Mapping

How Domain-Driven Design concepts derive from kernel and software ring terms:

| DDD Concept | Kernel Terms | How it derives |
|-------------|-------------|----------------|
| Ubiquitous Language | language + domain | Scoped vocabulary grounded in the domain model |
| Bounded Context | scope + context | Limits information for a coherent system |
| Entity | entity | Identity-bearing object (DDD narrows kernel's broader definition) |
| Aggregate | system | A whole of relationships, internally consistent |
| Domain Event | evolution + signal | State change that triggers responses |
| Model | model | Abstraction of a domain |
| Value Object | state + type | Defined by attributes, not identity |

## Node Specification

Each `src/*.md` file follows the template in [SPEC.md](SPEC.md):

| Section | Question | Maps To |
|---------|----------|---------|
| Ontology | What IS it? | Definition, identity |
| Axiology | Why does it MATTER? | Value, purpose, significance |
| Ethics | What SHOULD we consider? | Moral implications (optional) |
| Epistemology | How do we KNOW it? | Evidence, sources, patterns |

## License

[Apache-2.0](LICENSE)
