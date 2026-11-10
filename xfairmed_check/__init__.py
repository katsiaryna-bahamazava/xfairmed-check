"""Deprecated name. The package is now `evidence_checker`; this alias keeps old imports working."""
from evidence_checker import run_checks  # noqa: F401
from evidence_checker.adapters.xfairmed_v1 import build_bundle  # noqa: F401

__all__ = ["build_bundle", "run_checks"]
