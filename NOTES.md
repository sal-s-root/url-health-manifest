# Engineering notes

## Problem

Review health-check URLs for schemes, embedded credentials, and duplicates.

## Input contract

The input is one JSON object. `examples/input.json` is the minimum supported
example, and `examples/expected.json` fixes the expected result. File input and
stdin use the same evaluation path. Required fields missing from the documented
shape and invalid values result in a nonzero command exit. Unused fields are not
schema-validated. Non-finite floating-point input is rejected.

## Implementation choices

The evaluation function is separate from argument parsing so callers can reason
about data transformations independently from file access. Sorting is explicit
where order is not otherwise part of the input contract. The command performs
no network or deployment operations.

## Verification

Four CLI checks pass: the documented example, equivalent stdin input, rejection
of a non-object input, and rejection of a non-finite input. These checks verify
those cases; they do not prove every input shape or production integration.

## Constraints and next steps

Does not make requests or resolve hosts. A syntactically valid URL is not necessarily reachable or trusted.

Before integrating this tool, define the upstream inventory format and freshness,
review sensitive fields, add representative boundary cases, and compare findings
with the relevant platform's authoritative tooling. A completed evaluation is not
a remediation approval.
