# Returning research results to the private Alchemy repository

Only copy these result files back:

```text
claims/glm/*.json
claims/qwen/*.json
submissions/pending/glm/*.json
submissions/pending/qwen/*.json
```

Do **not** copy arbitrary model-created files.

In the private repository:

1. Run schema validation.
2. Run final QC.
3. Review WARN findings.
4. Approve.
5. Run deterministic importer.
6. Archive processed submissions.

The private repository remains the source of truth for chemistry and final binary assets.
