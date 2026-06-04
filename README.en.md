# Guangyao Yin's Codex Skills

This repository is a central index for Codex skills maintained by Guangyao Yin. It follows the general idea of `lovstudio/skills`: individual skills live in separate repositories, while this repository provides a unified catalog, installation commands, and a machine-readable manifest.

## Quick Install

Choose a skill and run its install command:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo GuangyaoYin/<repo-name> \
  --path <skill-path>
```

Restart Codex after installation.

## Skills

| Skill | Purpose | Repository | Path |
| --- | --- | --- | --- |
| `nsfc-project-review` | Batch review NSFC proposal PDFs and generate formal Chinese communication-review comments, grades, and funding recommendations. | [`skill-nsfc-project-review`](https://github.com/GuangyaoYin/skill-nsfc-project-review) | `.` |
| `paper2pdf` | Format academic manuscripts into journal-style DOCX/PDF layouts using journal templates, publisher guidelines, sample PDFs, or SciSpace links. | [`skill-paper2pdf`](https://github.com/GuangyaoYin/skill-paper2pdf) | `paper2pdf` |
| `review-response-docx` | Draft point-by-point reviewer responses and create formatted response letters, marked revised manuscripts, and clean versions. | [`skill-review-response-docx`](https://github.com/GuangyaoYin/skill-review-response-docx) | `review-response-docx` |
| `skill-endnote-research` | Search a local EndNote library from a research idea, collect matching PDFs, and generate a literature-review folder. | [`skill-endnote-research`](https://github.com/GuangyaoYin/skill-endnote-research) | `.` |
| `skillscreator` | Turn task ideas, examples, workflows, documents, webpages, or repositories into reusable GitHub-ready Codex skills. | [`skill-skillscreator`](https://github.com/GuangyaoYin/skill-skillscreator) | `skillscreator` |

## Manifest

See [`skills.yaml`](skills.yaml) for a machine-readable catalog.

## Maintenance Notes

- Keep each skill in its own repository for independent installation and versioning.
- Ensure every `SKILL.md` has clear `name` and `description` frontmatter.
- Document local-path, private-data, or environment-specific assumptions clearly.
- Avoid personal manuscript details, real author lists, unpublished projects, or sensitive material in public examples.
- Do not fabricate references, line numbers, experiments, results, or journal requirements.
