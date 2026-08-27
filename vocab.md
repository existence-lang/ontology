# Existence Lang -- RDF Vocabulary

Namespace: `https://existence-lang.github.io/ontology/vocab#` (prefix `xl:`).

`existence export` publishes this ontology as [SKOS](https://www.w3.org/TR/skos-reference/):
every node in `src/` is a `skos:Concept` in the scheme
`https://existence-lang.github.io/ontology/`, identified by
`https://existence-lang.github.io/ontology/<term>`, and every ring is a
`skos:Collection` at `https://existence-lang.github.io/ontology/ring/<n>`.
The node template has structure SKOS does not, so the properties below carry
it. They are annotation properties: they attach prose to a concept and imply
no logical axioms.

## ring

`xl:ring` -- the ring level (`xsd:integer`) a concept or collection belongs
to, from `existence.toml`. Ring 0 concepts are also `skos:hasTopConcept` of
the scheme.

## ontology

`xl:ontology` -- the node's **Ontology** section (what the term IS), verbatim
markdown. Its first line is the lay definition and is also emitted as
`skos:definition`.

## axiology

`xl:axiology` -- the node's **Axiology** section (why it MATTERS).

## ethics

`xl:ethics` -- the node's optional **Ethics** section (what SHOULD be
considered).

## epistemology

`xl:epistemology` -- the node's **Epistemology** section (how we KNOW it:
cultural definitions and pattern expressions).

## Standard properties used

| Property | Source |
|----------|--------|
| `skos:prefLabel` | the `# Title` line |
| `skos:definition` | first line of the Ontology section |
| `skos:related` | `[term](./term.md)` links (untyped in the source, so no broader/narrower) |
| `rdfs:seeAlso` | external `href` and `[text](https://...)` references |
| `skos:inScheme`, `skos:hasTopConcept`, `skos:member` | scheme and ring structure |

See the [existence CLI](https://github.com/existence-lang/existence#export-as-rdf-skos)
for the export command and the [SPEC](SPEC.md) for the node template.
