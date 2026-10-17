# ticket-001: Fix CLI help test and adopt Wellmanifest standards

- **Status**: IN_PROGRESS
- **Workflow state**: VERIFIED

SESSION_EXECUTION_AUTHORIZATION: user requested implementation and publication across Semcod and Subactor.

## Acceptance Criteria
- [x] AC-01: Place docstring at start of `main(ctx)` in `heal/cli.py` so `heal --help` includes `"Heal - LLM-powered shell error fixing."` and `tests/test_cli.py::test_main_help` passes (`72 passed`).
- [x] AC-02: Adopt Wellmanifest `baseline` profile standards in `.governance/`.
