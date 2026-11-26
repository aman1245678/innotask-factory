# Task: Add `deprecated` parameter and warning to `click.Option`

## Problem Description
Extend Click's option decorator and Option class to support a `deprecated` flag. When users invoke a CLI command providing a deprecated option, Click should output a formatted deprecation warning to stderr without aborting command execution.

## Acceptance Criteria
- Support `deprecated=True` on `click.Option`, emitting warning: 'Option "<name>" is deprecated.'
- Support `deprecated="Custom message"`, emitting the custom explanation string.
- Warnings must be emitted to sys.stderr via Click's echo or standard warnings.
- Command execution must succeed normally (exit code 0) after warning.
- All existing Click option tests and parameters must remain 100% backward-compatible.


## Target Files
- `src/click/core.py`


## Baseline Environment
- **Repository:** `https://github.com/pallets/click`
- **Baseline Commit:** `7eb021a68430dc0702d1d0ad510617ad4ea9ad27`
- **Test Command:** `bash test.sh`
