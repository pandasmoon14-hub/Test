# Portable local execution and evidence

Python 3.11+ and Git are required. Python 3.12 matches current CI. Optional PDF
and schema dependencies remain optional; skips must be reported. Follow current
requirements and CI if versions change. These commands do not configure ChatGPT,
fetch owner approvals or prove platform certification.

## Set up once per checkout/environment

Linux/macOS/Termux (install Python/Git using the device's supported package system):

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python -m pip check
```

Windows PowerShell (activation is optional):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip check
```

Use the environment's Python in every command below. On Windows replace `python`
with `.\.venv\Scripts\python.exe` if not activated. Do not replace HOME or system
environment variables for task paths. Keep the directory passed to `--output`
new, empty and outside the checkout (the sibling examples below meet that rule).

## Reproducible commands

```sh
python scripts/myravant_dev.py context --output ../myravant-context.json
python scripts/myravant_dev.py verify --profile focused --test-path tests/test_myravant_portable_development.py --output ../myravant-focused-001
python scripts/myravant_dev.py verify --profile full --output ../myravant-full-001
python scripts/myravant_dev.py list-retained
python scripts/myravant_dev.py verify --profile retained --output ../myravant-retained-001
```

For actual runtime development, add each affected test file using another
`--test-path`; the portability test file alone cannot validate gameplay changes.
Full runs invoke the complete unfiltered `python -m pytest -q`. Retained runs
discover explicit report commands in current CI and fail closed on unsupported
syntax or a missing expected output. Review owning contracts for additional
checks not represented by those commands. The tool neither edits CI nor removes
required commands or platforms. Actual installed-client evidence still comes
from the package's existing report runners and tests.

Each run retains commands, exit status, timing, logs, source head, cached main,
tracked dirty fingerprint, environment and whether source changed during the run.
Untracked contents are not fingerprinted; use a clean published candidate for
certification. Reports explicitly set `certified: false`: local command success
cannot attest remote CI, independent review, blind or human acceptance. Do not
claim all retained reports ran when the first failure stopped execution.

## Read-only/no-shell chat fallback

1. Retrieve current AGENTS.md, development entry point, affected source and approval.
2. Produce an exact patch against an identified source, with changed paths and
   focused/full commands. Use `git apply --check` locally before applying it.
3. Apply only in an isolated branch after inspecting the patch; run verification
   locally or through authorized available CI. Do not assume workflow dispatch,
   GitHub writes or device control exists in the chat.
4. Return verification.json and relevant failing log excerpts to the chat; preserve
   raw logs and package evidence in the existing PR. Bind the final candidate to
   observed checks. Limit shared logs to relevant material; do not export credentials.

When only external CI remains, save a compact checkpoint with the run URL in the
owning PR and resume on the next turn. A continuously active model is unnecessary.
