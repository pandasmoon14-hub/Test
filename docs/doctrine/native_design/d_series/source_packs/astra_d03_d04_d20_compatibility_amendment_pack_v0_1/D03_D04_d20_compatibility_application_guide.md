# D03/D04 D20 Compatibility Application Guide

Version: v0.1  
Status: Application guide  
Purpose: Explain how to use this amendment pack without regenerating D03 or D04.

## Use model

This pack is an amendment layer.

It does not replace the full D03 or D04 doctrine packs. It supersedes only incompatible references to old D02 outcome labels and margin bands.

## Application order

When reading D03 or D04:

1. Use the original D03/D04 doctrine text.
2. If the text references old D02 outcome labels, apply this amendment.
3. If the text references old D02 margin breakpoints, apply this amendment.
4. Preserve all unaffected D03/D04 doctrine.
5. Preserve all D03/D04 owner boundaries.
6. Continue to use locked D02 d20-first resolution.

## Superseded labels

The following older labels are superseded:

- Critical Success;
- Exceptional Success;
- Clean Success;
- Partial Result;
- Mixed Result;
- Failure with Consequence;
- Severe Failure;
- Critical Failure.

Use the locked D02 states instead:

- Ascendant;
- Clear;
- Fractured;
- Receded;
- Sundered.

## Superseded margin breakpoints

The following older margin breakpoints are superseded:

- +5;
- 0 to +4;
- -4 to -7;
- -8 or worse.

Use the locked D02 margin bands instead:

- Ascendant: +10 or higher;
- Clear: 0 to +9;
- Fractured: -1 to -4;
- Receded: -5 to -9;
- Sundered: -10 or lower.

## Repo integration note

When D03 and D04 are eventually incorporated into the repo, either:

1. apply these amendments directly to the affected source files; or
2. include this amendment pack as an explicit compatibility override and add registry metadata marking D03/D04 as amended.

Direct patching is cleaner long-term. A compatibility override is acceptable short-term while D11 is being generated.
