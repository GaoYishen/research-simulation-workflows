---
name: research-session-handoff
description: Produce an evidence-linked handoff for continuing a simulation task, preserving incomplete checks and open decisions.
---

# research-session-handoff

Use the companion repository containing this file; the root workflow.py and docs are required. Python 3.10+ is sufficient. No solver or external service is needed.

Run `python workflow.py handoff MANIFEST --output NEW_REPORT.md` from the repository root for a factual starter. Read [the schema](../../docs/manifest.md) when fields are unclear.
Add the session's actual completed work, changed files, current structure, known issues and next action from available evidence. Mark unknown information rather than reconstructing it from guesses.
Separate accepted decisions from proposals and physical validation from execution status. Retain failed and stopped results.
Include exact relative evidence paths and a concrete resume step. Do not include secrets or unrelated private information.
The generated report is a starter, not proof that the evidence supports the recorded checks. Avoid overwriting a previous handoff; use a new filename.
