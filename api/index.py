"""
Vercel Serverless Function Entry Point for EduPath FastAPI Backend.
"""

import sys
import os

# Insert root and backend paths into Python module search path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, "backend")

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.core.database import connect_to_mongo
from app.main import app

# Ensure Mongo / mongomock is connected on serverless instance initialization
connect_to_mongo()
