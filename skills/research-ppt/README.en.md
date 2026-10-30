# research-ppt

Create editable research PowerPoint decks for lab meetings, supervisor discussions, research progress, and a separate paper-reading mode. First offer background literature research, use `grill-me` to co-design the scientific argument, and agree on the slide plan before authoring.

## Workflow

Ask whether the user wants online literature research to supplement the background. If yes, search the accessible local knowledge base and primary literature online, then connect each background claim to a verified paper and the relevant original figure or panel. If online research is declined, use the provided and authorized local materials and identify evidence gaps.

In either branch, use the installed `grill-me` / `grilling` workflow to clarify background logic, the scientific question, competing explanations, and evidence limits before planning and authoring slides. Reuse conclusions already agreed for the same deck. Keep private research details out of public search queries.

Organize slides for understanding and logical reasoning rather than a fixed chapter count. Retain essential methods, data, reasoning, and substantive discussion in the main deck. Identify evidence gaps, conflicting results, and alternative explanations.

The paper-reading mode covers the research question, proof strategy, methods, data, limitations, relevance to the presenter's work, and the field-level value of the questions the paper resolves or raises.

Preserve source figures and their scientific meaning. Whitespace cropping, close-ups, and separate editable annotations are allowed. Redrawing requires source data and checks of units, coordinates, color scales, and numerical meaning.

The default design uses white backgrounds, dark text, light headers, and restrained blue/red emphasis. Chinese text uses Microsoft YaHei, Latin text uses Times New Roman, and equations may use a dedicated math font. Explicit task instructions take precedence.

Deliver an editable PPTX with short slide notes. Add concise source citations where appropriate on the slide and full sources in the notes. Project, acceptance, conference, and achievement reports use their applicable report/template workflow.

## Install

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo GuangyaoYin/skills --path skills/research-ppt
```

The interview workflow requires the `grilling` implementation. Also install its `grill-me` alias to use that explicit entry point. If neither is installed:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo mattpocock/skills --path skills/productivity/grilling skills/productivity/grill-me
```

If one is already installed, list only the missing path. The alias alone is insufficient. See [the upstream skills](https://github.com/mattpocock/skills/tree/main/skills/productivity), then restart Codex after installation.

## Use

```text
Use $research-ppt with these notes, result figures, and existing slides.
First ask whether I want local and online literature research for the background.
Use $grill-me to clarify the background and scientific question with me, agree on
the slide plan, then create an editable lab-meeting PPTX with essential method
details and substantive discussion.
```

## Dependencies and limits

The host needs presentation authoring, rendering, and editing tools; the skill coordinates with the available Presentations workflow. The inspection helper uses the Python standard library. Python 3.10+ is recommended; development tests used Python 3.11.16.

Equations must be native editable PowerPoint math objects. **Native equation generation and in-application PowerPoint editing have not been tested end to end.** Verify the authoring route for the actual deck. A PPTX export or detected math XML alone does not prove editability or correct visual output.

```bash
python skills/research-ppt/scripts/inspect_research_pptx.py /path/to/deck.pptx --require-notes
python -m unittest discover -s skills/research-ppt/tests -v
```

Use `--expected-slides N` and `--expected-equations N` when the planned counts are known. The helper performs read-only structural inspection; it does not create slides or replace visual, source, or PowerPoint editing checks.

The initial version passed structural validation, seven synthetic-package inspector tests, and a read-only review of three workflow scenarios. The background and interview update received two additional read-only scenario reviews. These checks do not establish end-to-end authoring or in-application editing of a deck based on real research materials.

## Contents

The skill includes `SKILL.md`, UI metadata in `agents/openai.yaml`, five focused references under `references/` (argument planning, background literature and source figures, background interviews, slide design, and native equations), the PPTX inspector under `scripts/`, and synthetic tests under `tests/`.

Only reusable instructions, code, and synthetic tests are included. Researchers provide their own source materials in the task environment; public examples contain no unpublished research or private documents.
