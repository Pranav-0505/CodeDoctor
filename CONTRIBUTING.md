# Contributing to Code Doctor

Thank you for contributing to the Code Doctor ecosystem!

## Development Guidelines

1. Maintain platform independence for `app/core/`.
2. All new analyzer rules must produce standard `DiagnosticItem` objects adhering to the Universal Error Model.
3. Every Code Surgery repair must support diff preview and safe verification.
4. Run `python -m pytest tests/` before submitting pull requests.
