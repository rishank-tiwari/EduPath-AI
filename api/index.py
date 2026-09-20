import os
import sys

# Add project root and backend directory to sys.path so modules like app and ai can be imported cleanly
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, "backend")

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from backend.app.main import app
from backend.app.core.database import connect_to_mongo

# Initialize DB connection for serverless runtime
try:
    connect_to_mongo()
except Exception:
    pass

__all__ = ["app"]

