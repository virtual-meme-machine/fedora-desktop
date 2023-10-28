import os
import sys

import pytest

__PACKAGE_ROOT: str = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
sys.path.append(os.path.join(__PACKAGE_ROOT, "src"))

GITHUB_IGNORED_FILES: list[str] = [
    "tst/data/test_OptionStore.py"  # gi imports cause crash: https://github.com/actions/runner-images/issues/4534
]

if __name__ == '__main__':
    args: list[str] = []
    if "--github_ignore" in sys.argv:
        for file in GITHUB_IGNORED_FILES:
            print(f"Skipping tests in file: '{file}'")
            args.append(f"--ignore={file}")

    sys.exit(pytest.main(args=args))
