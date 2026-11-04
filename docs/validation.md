# Local release-candidate validation

2026-11-04 pre-publication refresh: all 12 Python unittest tests and the three Skill format checks passed again on Windows/Python 3.13. GitHub owner selected: GaoYishen. See the repository Actions tab for remote CI results; the original candidate record below is historical.

First remote CI exposed Git autocrlf normalization of the synthetic evidence on Linux: the working-tree bytes matched the manifests but the initial Git blobs did not. Added .gitattributes to preserve the exact bytes of examples/**/*.txt and re-staged those synthetic fixtures. Hash verification remains byte-exact; no normalization or relaxed comparison was added to the audit tool.

Date: 2026-11-01 (Asia/Shanghai)

- 12 Python unittest tests passed locally on Windows.
- All three Skill entrypoints passed the skill-creator quick validator.
- Tests cover evidence tampering, missing evidence, interrupted runs, empty checks, failed checks, malformed fields, units, path traversal, symlink escape, output overwrite prevention and all shipped examples.
- GitHub Actions is configured for Windows/Linux and Python 3.10/3.12; remote CI has not run yet.
- Release content was newly authored; examples are synthetic. No private solver files were copied.
- Record integrity and declared validation status remain distinct. This tool does not independently assess physical correctness.
- MIT license selected by the user and added on 2026-11-01.
- Pending publication: GitHub authentication and owner selection. Upload deferred at the user's request.
