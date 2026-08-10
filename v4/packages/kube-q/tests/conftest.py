"""Shared pytest fixtures for kube-q.

Pin terminal rendering env for the whole suite. Rich/console output otherwise
depends on the developer's COLUMNS, TERM, and NO_COLOR, which makes unrelated
tests fail on narrow or dumb terminals (see #106).

Import-time pinning ensures the global Rich console (created at import time in
renderer.py) sees deterministic values even when the outer process was launched
with NO_COLOR=1 or TERM=dumb. The autouse fixture keeps it pinned per-test.
"""

from __future__ import annotations

import os

# ── Import-time: fix the process env before any test imports renderer ────────
# conftest is loaded before test modules, so this runs before renderer.py
# creates its singleton Console(theme=get_theme()).
os.environ["COLUMNS"] = "120"
os.environ["TERM"] = "xterm-256color"
os.environ.pop("NO_COLOR", None)
os.environ.pop("FORCE_COLOR", None)

import pytest  # noqa: E402  (import after env pin on purpose)


@pytest.fixture(autouse=True)
def _pin_terminal_rendering_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COLUMNS", "120")
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
