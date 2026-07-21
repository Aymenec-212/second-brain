---
created_at: '2026-05-30T20:30:00Z'
entities:
- GitHub Actions
- Poetry
- twine
- v0.1.0
id: 01KSX98KA0VNCCJYJCPKRF57R1
language: en
source:
  end_turn: 8
  session_id: seed-ceb7fcbdee356a98
  start_turn: 5
tags:
- release
- ci
- github-actions
- pypi
title: 'Release workflow specifics: auto-publish on tag push and branch protection'
type: decision
---

Release workflow decisions and CI gating rules: main will be a protected branch. Merges must go through PRs (forks or branches). On merge to main the CI pipeline runs the full test suite, but publishing to PyPI only occurs when I push a release tag. I will use an automated release workflow that triggers on tag pushes matching v0.1.0. The release job will use Poetry to build and twine to publish to PyPI, using credentials stored in GitHub Secrets. The CI config will include two workflows: .github/workflows/ci.yml (lint, pytest, coverage for Python 3.11 and 3.12) and .github/workflows/release.yml (triggered by tag push, builds and publishes). This keeps the main branch tested but prevents accidental publishes; only a tag push under my control triggers the PyPI upload. Ensure the release job is idempotent and fails fast if packaging metadata is invalid.