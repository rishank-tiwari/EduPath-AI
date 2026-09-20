import os
import sys
import traceback

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, "backend")

for p in [root_dir, backend_dir, os.getcwd(), os.path.join(os.getcwd(), "backend")]:
    if p and p not in sys.path:
        sys.path.insert(0, p)

try:
    from backend.app.main import app as _app
except Exception as e1:
    try:
        from app.main import app as _app
    except Exception as e2:
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse
        _app = FastAPI()

        @_app.all("/{full_path:path}")
        async def fallback_err(full_path: str):
            return JSONResponse(
                {
                    "error": "import_failed",
                    "e1": str(e1),
                    "e2": str(e2),
                    "trace": traceback.format_exc(),
                },
                status_code=500,
            )

app = _app
handler = app
