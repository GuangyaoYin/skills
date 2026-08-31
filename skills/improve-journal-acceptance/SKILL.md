---
name: improve-journal-acceptance
description: Review and improve an academic manuscript submission package to increase the chance of journal acceptance or external review. Use when the user asks for pre-submission checks, journal-fit advice, title/abstract/cover-letter polishing, figure-message review, editor/reviewer suggestions, resubmission after rejection, or transfer strategy, especially for Science Advances-style editorial screening.
---

# Improve Journal Acceptance

## Purpose

Use this skill to help an author make a manuscript easier for editors and reviewers to evaluate favorably. The skill is based on Warren S. Warren's 2022 *Science Advances* editorial, "Beating the odds for journal acceptance," and is meant for practical pre-submission or resubmission review.

Do not treat this as a promise of acceptance. The goal is to remove avoidable reasons for editorial rejection and make the real scientific contribution visible.

## Core Editorial Logic

Assume busy editors form early impressions from:

- The title.
- The abstract.
- The cover letter.
- The figures and captions.
- The comparison with the most relevant prior work.
- The fit between manuscript, journal scope, suggested editors, and suggested reviewers.

Editors at broad journals are curators. They look for work that matters beyond a narrow subfield and is more than incremental. Help the user show that clearly and honestly.

## Workflow

1. Identify the target journal and manuscript type.
2. Inspect the available package: title, abstract, cover letter, main figures, captions, manuscript text, suggested editors, suggested reviewers, prior reviews, or rejection letters.
3. Diagnose editorial risk before line editing.
4. Rewrite or advise only after the core message, novelty, journal fit, and evidence chain are clear.
5. Return concrete edits, not generic encouragement.

When files are provided, work from the actual files. Do not invent manuscript claims, results, citations, author lists, reviewer names, editor names, or journal policies.

## Ten-Point Check

### 1. Title And Abstract

Check whether the title and abstract are concise, accurate, and not overstated. Remove inflated adjectives and make the essential finding visible.

Ask:

- What is the one result the reader must remember?
- Is the claim proportional to the evidence?
- Can a broad scientific reader understand the abstract without decoding jargon?

### 2. Duplicate Or Near-Duplicate Resubmission

If this is a resubmission to the same journal, check whether an editor explicitly invited revision or whether there is substantial new data, analysis, or framing.

Require the cover letter to explain the reason for resubmission clearly. Otherwise, flag a high risk of desk rejection.

### 3. Prior Work Comparison

Check whether the manuscript fairly and prominently compares with the most relevant prior work, including work that could limit the novelty claim.

Do not allow the user to hide key papers in a late paragraph or minimize them vaguely. A strong manuscript should state exactly what prior work did and what this manuscript adds.

### 4. Cover Letter

Use the cover letter to support the editor's first impression. It should:

- State the core contribution in plain language.
- Explain why the work matters to the journal's audience.
- Place the work in the actual research landscape.
- Avoid a long list of high-profile but loosely related papers.
- Avoid generic praise for the journal.

### 5. Grammar And Clarity

Check the title, abstract opening, figure captions, and cover letter first. Small errors in these places signal weak attention to detail.

For non-native English writing, prioritize clarity and precision over ornate phrasing.

### 6. Main Message In Figures

Assume editors and reviewers may start with figures and captions. Check whether each main figure communicates a clear piece of the argument.

Flag:

- Figures placed far from their captions when the format allows embedding.
- Captions that describe only what is plotted, without the key interpretation.
- Simulation or calculation results described as if they were experimental observations.
- Main figures that require reading the full Methods before any message is visible.

### 7. Associate Editor Suggestions

If the journal allows suggested editors, recommend people who can actually evaluate the work and who match the journal's editor groups.

A poor editor suggestion can make the paper harder to route and may signal poor journal fit. Do not invent editor names; verify against the journal's current editorial board when needed.

### 8. Reviewer Suggestions

Suggest reviewers who are competent and plausibly unbiased. Avoid close collaborators, recent coworkers, recent coauthors, direct competitors with obvious conflict, or people with severe personal/professional conflicts.

In the cover letter, briefly explain why suggested reviewers are qualified when that helps the editor.

### 9. After Rejection Elsewhere

If submitting after rejection from another journal:

- Change the target journal name everywhere.
- Address prior reviewer comments seriously.
- Consider disclosing prior reviews when it strengthens the case and the journal allows it.
- Explain what changed and why the manuscript is now a better fit.

Never imply that ignoring prior reviews is acceptable.

### 10. Transfer Strategy

If asking for transfer to a sibling journal, check real scope fit. Do not assume journal families form a simple hierarchy.

Recommend transfer only when the receiving journal's audience and article type fit the content.

## Output Formats

For a quick review, return:

```text
Overall risk: low / medium / high
Main desk-rejection risks:
Top fixes before submission:
Journal-fit judgment:
Specific text edits:
```

For a full pre-submission audit, return:

```text
1. Editorial first impression
2. Title and abstract diagnosis
3. Novelty and prior-work comparison
4. Figure and caption message check
5. Cover letter plan or revision
6. Editor/reviewer suggestion strategy
7. Resubmission or transfer risks
8. Final submission checklist
```

For manuscript rewriting, preserve the user's scientific claims and mark uncertain claims as questions instead of inventing support.

## Good Final Checklist

Before telling the user a package is ready, confirm:

- The title and abstract state the main finding without exaggeration.
- The cover letter explains contribution, audience, and fit.
- The most relevant prior work is compared fairly.
- Figures and captions reveal the main message.
- Suggested editors and reviewers are appropriate and not conflicted.
- Any prior rejection has been addressed honestly.
- The target journal name is correct in all visible submission materials.
