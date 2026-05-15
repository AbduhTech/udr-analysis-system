#!/usr/bin/env python3
"""
================================================================
SETUP VERIFICATION SCRIPT — UDR Analysis System
================================================================
Run this first to verify your environment is ready.

Usage:
    python setup_check.py
================================================================
"""

import sys
import subprocess

REQUIRED = ['matplotlib', 'numpy', 'pandas']
PYTHON_MIN = (3, 9)


def check_python():
    v = sys.version_info
    ok = v >= PYTHON_MIN
    status = "✓" if ok else "✗"
    print(f"  {status}  Python {v.major}.{v.minor}.{v.micro}  (required: ≥ {PYTHON_MIN[0]}.{PYTHON_MIN[1]})")
    return ok


def check_package(name):
    try:
        __import__(name)
        print(f"  ✓  {name}")
        return True
    except ImportError:
        print(f"  ✗  {name}  ← missing, run: pip install {name}")
        return False


def check_data():
    import os
    path = os.path.join('data', 'survey_data.csv')
    ok = os.path.exists(path)
    status = "✓" if ok else "✗"
    print(f"  {status}  data/survey_data.csv")
    return ok


def main():
    print()
    print("UDR Analysis System — Environment Check")
    print("=" * 45)

    print("\nPython version:")
    py_ok = check_python()

    print("\nRequired packages:")
    pkg_ok = all(check_package(p) for p in REQUIRED)

    print("\nData files:")
    data_ok = check_data()

    print()
    if py_ok and pkg_ok and data_ok:
        print("  All checks passed. Run: python main.py")
    else:
        print("  Some checks failed. Install missing items then re-run.")
        if not pkg_ok:
            print("  Quick fix: pip install -r requirements.txt")
    print()


if __name__ == '__main__':
    main()
