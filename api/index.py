import os
import sys

# Dynamically resolve paths for Vercel serverless environment
cwd = os.getcwd()
file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(file_dir)

for path in [cwd, file_dir, parent_dir, os.path.join(cwd, "backend"), os.path.join(parent_dir, "backend")]:
    if path and os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

try:
    from backend.app.main import app as _fastapi_app
except ImportError:
    from app.main import app as _fastapi_app

# Warm up database connection if configured
try:
    from app.core.database import connect_to_mongo
    connect_to_mongo()
except Exception:
    pass

# Expose top-level variables required by Vercel Python runtime AST inspection
app = _fastapi_app
handler = app
application = app
