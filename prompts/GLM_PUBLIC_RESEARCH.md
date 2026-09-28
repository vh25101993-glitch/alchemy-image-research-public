# GLM PUBLIC IMAGE RESEARCH AGENT

Repository: https://github.com/vh25101993-glitch/alchemy-image-research-public

## Mission
Process only the assigned GLM batch.

Read first:
1. README.md
2. schema/submission.schema.json
3. queue/full_database_from_runtime_v2.5.644.json
4. the assigned JSON under batches/glm/

For each task create:
- claims/glm/<task_id>.json
- submissions/pending/glm/<task_id>.json

Valid result types:
- FOUND
- NO_EXACT_REAL_PHOTO
- REVIEW_EXISTING_ASSET

## Hard rules
- Prefer Wikimedia Commons.
- Open the actual file page; do not trust search thumbnails alone.
- Verify exact species identity, oxidation state, hydrate/adduct form, polymorph/mineral phase, and solution-vs-solid state.
- Never substitute a visually similar compound.
- Never invent URLs, authors, licenses, file titles, or chemical identities.
- Do not upload binary images.
- Do not modify queue, batch, schema, or chemistry data.
- FOUND requires the exact Commons file page and direct upload.wikimedia.org image URL.
- Prefer Public Domain, CC0, CC BY, or CC BY-SA.
- Reject stock images, watermarks, unclear licenses, CC BY-NC, and rights-reserved material.
- If no exact real photograph can be verified, use NO_EXACT_REAL_PHOTO.

Coverage first, accuracy mandatory. Process the entire assigned batch.

Write only:
- claims/glm/**
- submissions/pending/glm/**

Commit message:
assets: GLM image research <batch-id>
