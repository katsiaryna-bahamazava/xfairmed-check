"""Deprecated alias of `evidence_checker.mutate`."""
import sys

import evidence_checker.mutate as _m

sys.modules[__name__] = _m
