# Changelog

All notable changes to this project are documented in this file.

## 2026-07-07
- Date: 2026-07-07
- Summary: Added GitHub Actions CI checks for linting, formatting, and tests.
- Added:
  - Added CI workflow at `.github/workflows/ci.yml`.
  - Added two CI jobs: Ruff lint/format check and pytest.
- Changed:
  - N/A
- Fixed:
  - N/A
- Docs:
  - Documented CI behavior and expected checks in `README.md`.
- Tests:
  - CI now runs `pytest` on pushes and pull requests.
- Lint/Format:
  - CI now enforces `ruff format . --check` and `ruff check .`.
