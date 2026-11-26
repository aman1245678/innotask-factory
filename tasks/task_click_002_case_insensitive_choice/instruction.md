# Task: Add `case_sensitive=False` support to `click.Choice` parameter type

## Problem Description
Allow `click.Choice` to accept case-insensitive user input when `case_sensitive=False`. The parsed value returned to the command function should be normalized to the canonical choice spelling.

## Acceptance Criteria
- Support `case_sensitive: bool = True` on `click.Choice`.
- When `case_sensitive=False`, choices match case-insensitively (e.g., 'RED' matches 'red').
- The returned parameter value must match the original choice capitalization.
- Invalid options must still raise `click.BadParameter` error.
- Default behavior must preserve strict `case_sensitive=True` matching.


## Target Files
- `src/click/types.py`


## Baseline Environment
- **Repository:** `https://github.com/pallets/click`
- **Baseline Commit:** `7eb021a68430dc0702d1d0ad510617ad4ea9ad27`
- **Test Command:** `bash test.sh`
