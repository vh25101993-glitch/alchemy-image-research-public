# Alchemy Chemistry Image Research — Public Handoff Repo

This repository is a **public research-only handoff** for GLM and Qwen.

It intentionally contains **no private game source, no reaction database, no APK, no keystore, no API keys, and no signing material**.

## Goal
Resolve visual coverage for all **1261 runtime species** in Hóa Học Alchemy v2.5.644.

A task is resolved by one of:
- `FOUND`
- `REVIEW_EXISTING_ASSET`
- `NO_EXACT_REAL_PHOTO`

The goal is 100% honest visual resolution, **not 100% forced photographs**.

## Repository layout
```text
prompts/
  GLM_PUBLIC_RESEARCH.md
  QWEN_PUBLIC_RESEARCH.md
schema/
  submission.schema.json
queue/
  full_database_from_runtime_v2.5.644.json
batches/
  glm/
  qwen/
claims/
  glm/
  qwen/
submissions/
  pending/
    glm/
    qwen/
```

## Model workflow
1. Read the model prompt.
2. Open the assigned batch.
3. Claim each task.
4. Search Wikimedia Commons.
5. Verify exact chemical identity and license.
6. Write a structured submission JSON.
7. Commit only claim/submission JSON.

## Never put these in this public repo
- private source code
- `database/**`
- `updates/**`
- reaction definitions
- APK/AAB files
- JKS/keystore files
- passwords/tokens/API keys
- GitHub Actions secrets
- private internal reports
- proprietary assets

## Return path
Submissions from this public repo are copied into the private repository only after QC.

See `RETURN_TO_PRIVATE_REPO.md`.
