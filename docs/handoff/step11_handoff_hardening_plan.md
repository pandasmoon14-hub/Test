# Step 11 Handoff Hardening Plan

Step 11 turns the Step 10C findings into repo improvements. This is not another conversion pass.

## Step 11 goals

1. Make the conversion-intake scaffolder tolerate escaped numbered headings such as `1\.`
2. Detect under-parsed drafted results.
3. Preserve Colostle-like backmatter packets as valid negative-control cases.
4. Add documentation for the final Step 10B/10C findings.
5. Add tests so future handoff runs catch these issues automatically.
6. Keep extraction provenance, conversion readiness, and canon permission separate.

## Step 11B result

The richer scaffolder/parser behavior has been verified against the full Step 10 run:

- all 12 Markdown results re-scaffolded
- strict validation passed
- all 12 packets remain drafted
- no placeholders remain
- no under-parsed packets were detected by the current filter
- full pytest passed with 89 tests

## Remaining Step 11 work

Step 11C should add explicit quality-audit or under-parsed detection tooling so fallback-level parses do not require manual inspection.
