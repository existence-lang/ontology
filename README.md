# Existence Lang -- Ontology

A domain ontology organized in concentric rings with 114 term files. Ring 0 is the universal kernel -- 14 terms that model Existence at the broadest scope. Ring 1 bridges the kernel to software engineering via Domain-Driven Design concepts. Ring 2 extends the ontology with 85 additional terms covering philosophy, spirituality, cognition, and other domains.

Terms are defined as interconnected nodes in `src/`. Each node follows the structure in [SPEC.md](SPEC.md): **Ontology** (what it is), **Axiology** (why it matters), **Epistemology** (how we know it).

## Ring Structure

```
Ring 0 (kernel)    -- 14 universal terms, always loaded
Ring 1 (software)  -- 17 terms bridging to DDD and software domains (2 pending)
Ring 2 (extended)  -- 85 terms across philosophy, spirituality, cognition, and more
```

Rings are additive. Ring 1 assumes Ring 0. Higher rings assume all lower rings. See [`existence.toml`](existence.toml) for the canonical ring definitions. (The `existence` CLI reads this file.)

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

## Ring 2 -- Extended (85 terms)

Broader ontological terms spanning philosophy, spirituality, cognition, linguistics, and more. These extend Ring 0 and Ring 1 into richer territory.

<details>
<summary>Click to expand Ring 2 term list</summary>

| Term | File |
|------|------|
| abstract | [src/abstract.md](src/abstract.md) |
| abstract-system | [src/abstract-system.md](src/abstract-system.md) |
| accuracy | [src/accuracy.md](src/accuracy.md) |
| aesthetics | [src/aesthetics.md](src/aesthetics.md) |
| agree | [src/agree.md](src/agree.md) |
| agreement | [src/agreement.md](src/agreement.md) |
| analogy | [src/analogy.md](src/analogy.md) |
| animism | [src/animism.md](src/animism.md) |
| anthropomorphism | [src/anthropomorphism.md](src/anthropomorphism.md) |
| art | [src/art.md](src/art.md) |
| attention-schema | [src/attention-schema.md](src/attention-schema.md) |
| awareness | [src/awareness.md](src/awareness.md) |
| axiology | [src/axiology.md](src/axiology.md) |
| being | [src/being.md](src/being.md) |
| belief | [src/belief.md](src/belief.md) |
| belief-system | [src/belief-system.md](src/belief-system.md) |
| category-theory | [src/category-theory.md](src/category-theory.md) |
| coercion | [src/coercion.md](src/coercion.md) |
| compassion | [src/compassion.md](src/compassion.md) |
| concept | [src/concept.md](src/concept.md) |
| conceptual-existence | [src/conceptual-existence.md](src/conceptual-existence.md) |
| conceptual-system | [src/conceptual-system.md](src/conceptual-system.md) |
| concrescence | [src/concrescence.md](src/concrescence.md) |
| contextual-systems | [src/contextual-systems.md](src/contextual-systems.md) |
| control-system | [src/control-system.md](src/control-system.md) |
| create | [src/create.md](src/create.md) |
| culture | [src/culture.md](src/culture.md) |
| disagree | [src/disagree.md](src/disagree.md) |
| domain-driven-design | [src/domain-driven-design.md](src/domain-driven-design.md) |
| ecosystem | [src/ecosystem.md](src/ecosystem.md) |
| emotion | [src/emotion.md](src/emotion.md) |
| energy | [src/energy.md](src/energy.md) |
| epistemology | [src/epistemology.md](src/epistemology.md) |
| ethics | [src/ethics.md](src/ethics.md) |
| evolutionary-linguistics | [src/evolutionary-linguistics.md](src/evolutionary-linguistics.md) |
| exist | [src/exist.md](src/exist.md) |
| expanding-consciousness | [src/expanding-consciousness.md](src/expanding-consciousness.md) |
| explicit-scope | [src/explicit-scope.md](src/explicit-scope.md) |
| faith | [src/faith.md](src/faith.md) |
| feeling | [src/feeling.md](src/feeling.md) |
| fractal | [src/fractal.md](src/fractal.md) |
| god | [src/god.md](src/god.md) |
| heuristic | [src/heuristic.md](src/heuristic.md) |
| history | [src/history.md](src/history.md) |
| human | [src/human.md](src/human.md) |
| humans | [src/humans.md](src/humans.md) |
| illusion | [src/illusion.md](src/illusion.md) |
| implicit-scope | [src/implicit-scope.md](src/implicit-scope.md) |
| inertia | [src/inertia.md](src/inertia.md) |
| intelligence | [src/intelligence.md](src/intelligence.md) |
| judgement | [src/judgement.md](src/judgement.md) |
| judicious | [src/judicious.md](src/judicious.md) |
| linguistics | [src/linguistics.md](src/linguistics.md) |
| love | [src/love.md](src/love.md) |
| natural-law | [src/natural-law.md](src/natural-law.md) |
| nature | [src/nature.md](src/nature.md) |
| novelty | [src/novelty.md](src/novelty.md) |
| ontology | [src/ontology.md](src/ontology.md) |
| paradox | [src/paradox.md](src/paradox.md) |
| philosophy | [src/philosophy.md](src/philosophy.md) |
| physical-existence | [src/physical-existence.md](src/physical-existence.md) |
| physical-system | [src/physical-system.md](src/physical-system.md) |
| precision | [src/precision.md](src/precision.md) |
| prejudice | [src/prejudice.md](src/prejudice.md) |
| presence | [src/presence.md](src/presence.md) |
| reality | [src/reality.md](src/reality.md) |
| redefine | [src/redefine.md](src/redefine.md) |
| redefinition | [src/redefinition.md](src/redefinition.md) |
| religion | [src/religion.md](src/religion.md) |
| respect | [src/respect.md](src/respect.md) |
| science | [src/science.md](src/science.md) |
| sexual-reproduction | [src/sexual-reproduction.md](src/sexual-reproduction.md) |
| signals | [src/signals.md](src/signals.md) |
| soul | [src/soul.md](src/soul.md) |
| spirit | [src/spirit.md](src/spirit.md) |
| spiritual-work | [src/spiritual-work.md](src/spiritual-work.md) |
| spirituality | [src/spirituality.md](src/spirituality.md) |
| technology | [src/technology.md](src/technology.md) |
| this-philosophy | [src/this-philosophy.md](src/this-philosophy.md) |
| tradition | [src/tradition.md](src/tradition.md) |
| transcendence | [src/transcendence.md](src/transcendence.md) |
| unconsciousness | [src/unconsciousness.md](src/unconsciousness.md) |
| unique | [src/unique.md](src/unique.md) |
| universal-set | [src/universal-set.md](src/universal-set.md) |
| violence | [src/violence.md](src/violence.md) |

</details>

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

## RDF / SKOS

Every term has a stable IRI, `https://existence-lang.github.io/ontology/<term>`
(for example `https://existence-lang.github.io/ontology/entity`), which is
also its page on this site. The [existence CLI](https://github.com/existence-lang/existence)
exports the whole ontology as SKOS:

```bash
existence export > ontology.ttl              # Turtle
existence export --format jsonld > ontology.jsonld
```

Identity comes from `meta.base_iri` in `existence.toml`; the `xl:` properties
that carry the Ontology / Axiology / Ethics / Epistemology sections are
documented in [vocab.md](vocab.md).

## License

[Apache-2.0](LICENSE)
