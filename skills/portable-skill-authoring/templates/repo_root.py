"""Locate the repo root from inside a skill script so shared modules under
`<repo>/shared` can be imported without any hardcoded path.

Copy this file into your skill's `scripts/` folder. It is stdlib-only, so a
no-base agent can use it as-is. The repo root is the nearest ancestor
directory that contains both `skills/` and `shared/`.

Usage:
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))   # so this module is importable
    from repo_root import shared_path
    sys.path.insert(0, shared_path(__file__))
    import opc            # a module living in <repo>/shared/opc.py
"""
import os


def find_repo_root(start=None):
    d = os.path.abspath(start if start else os.path.dirname(__file__))
    if os.path.isfile(d):
        d = os.path.dirname(d)
    while True:
        if os.path.isdir(os.path.join(d, "skills")) and \
           os.path.isdir(os.path.join(d, "shared")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise RuntimeError(
                "repo root not found: no ancestor of {} has both "
                "skills/ and shared/".format(start or __file__))
        d = parent


def shared_path(start=None):
    return os.path.join(find_repo_root(start), "shared")
