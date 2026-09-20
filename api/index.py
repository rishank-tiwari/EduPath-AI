import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, "backend")

for p in [root_dir, backend_dir, os.getcwd(), os.path.join(os.getcwd(), "backend")]:
    if p and os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from backend.app.main import app
