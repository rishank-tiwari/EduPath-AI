# EduPath Backend Service

FastAPI-powered REST API server for EduPath.

## Setup & Running

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start dev server
uvicorn app.main:app --reload --port 8000
```

## API Verification

- **Health Endpoint**: `GET /api/v1/health`
- **Swagger Documentation**: `GET http://localhost:8000/docs`
