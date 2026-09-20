"""EduPath Backend Package."""

import sys
from pathlib import Path

# Ensure backend directory and project root directory are in sys.path
_backend_dir = Path(__file__).resolve().parent.parent
_root_dir = _backend_dir.parent

if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

if str(_root_dir) not in sys.path:
    sys.path.insert(0, str(_root_dir))
