---
name: academic-discussion-polisher
description: Translate, polish, draft, restructure, or diagnose academic-paper Discussion sections, with emphasis on evidence-to-mechanism reasoning, alternative explanations, limitations, claim-strength calibration, and journal-ready English. Use for Chinese-to-English or English-to-English Discussion work; do not use for Introductions, Methods, Results, abstracts, or general document formatting unless the user explicitly includes them.
---

# Academic Discussion Polisher

Improve only the Discussion unless the user explicitly expands the scope. Preserve the author's scientific meaning, evidence strength, citations, terminology, numerical values, uncertainty, and causal boundaries. Do not invent results, mechanisms, literature, parameter tests, limitations, novelty, or practical implications.

## Choose the mode

- **Diagnose:** identify repeated Results, missing reasoning steps, unsupported mechanisms, unaddressed alternatives, vague limitations, and overclaimed implications.
- **Translate:** produce idiomatic academic English from Chinese while preserving logical relationships and uncertainty; do not translate word for word.
- **Polish:** improve reasoning visibility, paragraph unity, cohesion, concision, syntax, and academic tone without changing substantive meaning.
- **Restructure:** reorder or rebuild paragraphs around findings, mechanisms, evidence, alternatives, boundaries, and implications.
- **Draft:** write a Discussion from the user's results, figures, literature, model tests, and stated interpretations; flag missing support instead of filling gaps with invented content.

When modes are combined, diagnose the logic first, then restructure, translate, or polish. For short sentence-level edits, preserve the local paragraph's intended function and avoid expanding scope.

## Core workflow

1. Identify the one to three findings that genuinely require interpretation. Separate direct observations or model outputs from mechanism inference and causal attribution.
2. Map each paragraph to one primary function: key finding, mechanism, literature comparison, alternative explanation, robustness/limitation, theoretical significance, hazard/management implication, or testable future work.
3. Repair reasoning before wording. Make the path from evidence to interpretation explicit, and ensure every `however`, `therefore`, `although`, and `consistent with` represents a real logical relation.
4. Calibrate claim verbs to the support available. Use stronger verbs only for direct and robust evidence; use `suggest`, `may`, `is consistent with`, or `likely` for inference.
5. Test each important interpretation against an independent constraint, a plausible alternative, or a stated applicability boundary. If none is supplied, flag the gap.
6. For models, distinguish robust spatial or temporal patterns from parameter-dependent absolute magnitudes. Do not present model output as direct observation.
7. For induced/triggered-event attribution, require converging temporal, spatial, mechanical, and independent evidence. Temporal proximity alone does not establish causation.
8. End at the evidence-supported level of theory, hazard, management, or a specific testable prediction. Avoid generic claims of importance or generic calls for more research.
9. Check terminology, tense, subject continuity, modifier attachment, parallelism, equation/figure references, citation placement, and consistency of abbreviations.
10. Return the revised text first unless the user asked only for diagnosis. Add only consequential notes, alternatives, or author-verification items.

## Non-negotiable writing rules

- Do not turn the Discussion into a second Results section. Repeat only the result needed to support the current interpretation.
- Do not collapse correlation, mechanism support, and causation into one claim.
- Do not use `prove`, `clearly`, `obviously`, `very`, or unsupported `significantly` to manufacture certainty.
- Use `show` for directly supported results, `indicate` or `support` for converging evidence, and `suggest` or `may reflect` for mechanism inference.
- Treat `demonstrate` as stronger than `show`; reserve it for evidence that directly rules in the stated relationship within the tested scope.
- A limitation should state what is limited, which inference it affects, and whether the main conclusion remains intact.
- Future work should identify the object, method or observation, and discriminating prediction—not merely say that more studies are needed.
- Treat “top-journal style” as compression, logical force, evidential precision, and controlled generalization—not ornate vocabulary or exaggerated novelty.
- Preserve hedging that carries scientific meaning. Remove only empty or repetitive hedging.
- Preserve citation ownership: do not make the user's study appear to establish a result that belongs to cited work.

## References

- For full-section architecture, paragraph roles, and logic diagnostics, read [references/logic-and-paragraphs.md](references/logic-and-paragraphs.md).
- For claim verbs, transitions, sentence patterns, and reusable English constructions, read [references/language-and-sentences.md](references/language-and-sentences.md).
- For Chinese-to-English translation and sentence-level polishing decisions, read [references/translation-and-polishing.md](references/translation-and-polishing.md).
- For geoscience, induced seismicity, pore-pressure/stress modeling, and forward-model–observation discussions, read [references/geoscience-and-induced-seismicity.md](references/geoscience-and-induced-seismicity.md).
- For the local 20-paper corpus, journal scope, and provenance of these rules, read [references/source-corpus.md](references/source-corpus.md) only when auditing or extending the skill.

Read only the references relevant to the request. A short English edit usually needs no supporting reference; a full Chinese Discussion about induced seismicity normally needs the logic, translation, and geoscience references.

## Default output

For a full Discussion, provide:

1. the revised or translated English Discussion;
2. a concise paragraph-by-paragraph logic map;
3. a short list of consequential changes and claims, terminology, citations, or causal steps requiring author verification.

For translation-only requests, return the translation first and omit commentary unless the source is ambiguous or scientifically overstrong. For diagnosis-only requests, do not rewrite the full text unless requested; give prioritized problems and representative revisions. When useful, provide one conservative and one stronger-but-still-supported alternative for a pivotal sentence.

