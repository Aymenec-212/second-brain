---
created_at: '2026-05-30T20:30:00Z'
entities:
- GitHub
- Poetry
- GitHub Actions
- PyPI
- tinygrid
id: 01KSX98KA03CFBVRE9FVEBW936
language: en
source:
  end_turn: 6
  session_id: seed-ceb7fcbdee356a98
  start_turn: 0
tags:
- repo
- ci
- packaging
- pypi
title: Repository layout, packaging, and CI requirements
type: task
---

Planned repository structure and CI/publishing policy: create a GitHub repository named tinygrid under MIT license. Top-level layout: tinygrid/__init__.py (expose __version__), tinygrid/envs/grid_env.py (single-file env impl first), tinygrid/wrappers.py, examples/ (ppo_sb3.py and ppo_pytorch_simple.py), tests/*.py, benchmarks/steps_per_sec.py, pyproject.toml (Poetry), README.md, LICENSE, CODE_OF_CONDUCT.md, CONTRIBUTING.md, and .github/workflows/ with ci.yml and release.yml. CI: GitHub Actions testing on Python 3.11 and 3.12. The CI matrix must run lint (black, flake8), pytest, and measure coverage with a minimum threshold 80%. Main branch will be protected; merges via PR. Release policy: auto-publish to PyPI when I push a tag v0.1.0 (release job triggers on tag push). Publishing uses Poetry and twine with PyPI credentials from GitHub Secrets. The release job should only run on tag events; merging to main should run the full test suite but must not auto-publish unless a tag is created.