---
name: simulation-case-manifest
description: Create a portable simulation manifest with explicit files, units and hashes when recording a new case.
---

# simulation-case-manifest

Use the companion repository containing this file; the root workflow.py and docs are required. Python 3.10+ is sufficient. No solver or external service is needed.

Ask which files belong to the case if the scope is unclear. Index only explicitly selected files; do not recursively inventory unrelated research folders.
Run `python workflow.py init CASE_DIR --id CASE_ID --files FILES --output CASE_DIR/manifest.json` from the repository root.
Replace the generated objective with the actual purpose; record parameters and units. Do not infer runtime success from filenames.
Read [the schema](../../docs/manifest.md) before editing fields. Keep paths relative. Distinguish user inputs from inferred values in the parameter names or accompanying notes.
Preserve old records when files change; an unexpected hash mismatch needs investigation before rebaselining.
Report created files, remaining missing evidence and the next action. Never run a solver merely to complete this manifest.
