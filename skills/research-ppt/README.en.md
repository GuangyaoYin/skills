# research-ppt

Create editable research PowerPoint decks for lab meetings, supervisor discussions, research progress, and a separate paper-reading mode. Co-design the scientific argument and slide plan before authoring.

## Workflow

Organize slides for understanding and logical reasoning rather than a fixed chapter count. Retain essential methods, data, reasoning, and substantive discussion in the main deck. Identify evidence gaps, conflicting results, and alternative explanations.

The paper-reading mode covers the research question, proof strategy, methods, data, limitations, relevance to the presenter's work, and the field-level value of the questions the paper resolves or raises.

Preserve source figures and their scientific meaning. Whitespace cropping, close-ups, and separate editable annotations are allowed. Redrawing requires source data and checks of units, coordinates, color scales, and numerical meaning.

The default design uses white backgrounds, dark text, light headers, and restrained blue/red emphasis. Chinese text uses Microsoft YaHei, Latin text uses Times New Roman, and equations may use a dedicated math font. Explicit task instructions take precedence.

Deliver an editable PPTX with short slide notes. Add concise source citations where appropriate on the slide and full sources in the notes. Project, acceptance, conference, and achievement reports use their applicable report/template workflow.

## Install

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo GuangyaoYin/skills --path skills/research-ppt
```

## Use

```text
Use $research-ppt with these notes, result figures, and existing slides.
First work with me on the argument and slide plan, then create an editable
lab-meeting PPTX with essential method details and substantive discussion.
```

## Dependencies and limits

The host needs presentation authoring, rendering, and editing tools; the skill coordinates with the available Presentations workflow. The inspection helper uses the Python standard library. Python 3.10+ is recommended; development tests used Python 3.11.16.

Equations must be native editable PowerPoint math objects. **Native equation generation and in-application PowerPoint editing have not been tested end to end.** Verify the authoring route for the actual deck. A PPTX export or detected math XML alone does not prove editability or correct visual output.

```bash
python skills/research-ppt/scripts/inspect_research_pptx.py /path/to/deck.pptx --require-notes
python -m unittest discover -s skills/research-ppt/tests -v
```

Use `--expected-slides N` and `--expected-equations N` when the planned counts are known. The helper performs read-only structural inspection; it does not create slides or replace visual, source, or PowerPoint editing checks.

The skill passed structural validation, seven synthetic-package inspector tests, and a read-only review of three workflow scenarios. A complete deck based on real research materials has not yet been trialed.

## Contents

The skill includes `SKILL.md`, UI metadata in `agents/openai.yaml`, three focused references under `references/`, the PPTX inspector under `scripts/`, and synthetic tests under `tests/`.

Only reusable instructions, code, and synthetic tests are included. Researchers provide their own source materials in the task environment; public examples contain no unpublished research or private documents.
