import os
import sys

import pytest

__PACKAGE_ROOT: str = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
sys.path.append(os.path.join(__PACKAGE_ROOT, "src"))

if __name__ == '__main__':
    sys.exit(pytest.main())
