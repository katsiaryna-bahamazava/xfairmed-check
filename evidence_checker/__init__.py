"""Evidence Checker: evidence-to-review checks over the outputs of fairness audits."""
from .engine import run_checks
from .profiles import resolve_profile

__all__ = ["run_checks", "resolve_profile"]
__version__ = "0.2.0"
