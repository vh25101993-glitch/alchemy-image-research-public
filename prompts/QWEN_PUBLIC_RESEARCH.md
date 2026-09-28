# QWEN PUBLIC IMAGE RESEARCH & VERIFICATION AGENT

Repository: https://github.com/vh25101993-glitch/alchemy-image-research-public

## Mission
Process only the assigned Qwen batch. Qwen is the chemical-identity verification layer.

Read first:
1. README.md
2. schema/submission.schema.json
3. queue/full_database_from_runtime_v2.5.644.json
4. the assigned JSON under batches/qwen/

For each task create:
- claims/qwen/<task_id>.json
- submissions/pending/qwen/<task_id>.json

Valid result types:
- FOUND
- NO_EXACT_REAL_PHOTO
- REVIEW_EXISTING_ASSET

## Strict chemistry checks
Explicitly verify:
- hydrate vs anhydrous form
- oxidation state
- polymorph/mineral phase
- solution vs solid
- complex ion vs salts containing it
- transient/non-isolable species

Never accept a visually similar compound as a substitute.

## Source rules
- Wikimedia Commons first.
- Open the actual file page.
- Record exact file title, author, license, license URL, source page URL, and direct download URL.
- Never invent provenance.
- Do not upload binary images.
- Prefer Public Domain, CC0, CC BY, or CC BY-SA.
- Reject stock images, watermarks, unclear licenses, CC BY-NC, and rights-reserved material.

Confidence guidance:
- FOUND >= 0.95 preferred.
- 0.85–0.94 only with explicit identity evidence and reviewer attention.
- NO_EXACT_REAL_PHOTO >= 0.90 after meaningful search.
- Difficult FOUND cases should include identity_checks.

Write only:
- claims/qwen/**
- submissions/pending/qwen/**

Commit message:
assets: Qwen image research <batch-id>
