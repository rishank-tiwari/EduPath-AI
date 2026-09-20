# EduPath Developer Setup Guide

This document guides you through establishing your local development environment for **EduPath**.

---

## 💻 Prerequisites

Ensure you have the following installed on your system:

- **Node.js**: v18.0.0 or higher ([Download Node](https://nodejs.org/))
- **Python**: v3.10 or higher ([Download Python](https://www.python.org/))
- **Git**: Latest release
- **MongoDB**: Local MongoDB community edition or a MongoDB Atlas connection string.

---

## 🛠️ Installation & Setup

### Step 1: Clone and Configure Environment

1. Ensure you are in the project root directory.
2. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

3. Update `.env` with your desired configuration parameters. Note: The application will start cleanly even if `MONGODB_URI` or `LLM_API_KEY` are not set during initial frontend development.

---

### Step 2: Setup and Launch Backend (`backend/`)

1. Change directory to `backend`:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   - **Windows**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. Verify backend operation:
   - Open `http://localhost:8000/api/v1/health` in your browser.
   - You should receive `{"status": "ok", "service": "EduPath API"}`.

---

### Step 3: Setup and Launch Frontend (`frontend/`)

1. Open a new terminal session and navigate to `frontend`:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Launch the Vite development server:
   ```bash
   npm run dev
   ```

4. Open `http://localhost:5173` in your browser.

---

## 🧪 Verification & Troubleshooting

- **Backend Health Check**:
  - `GET http://localhost:8000/api/v1/health`
- **Interactive API Documentation (Swagger)**:
  - `http://localhost:8000/docs`
- **Frontend Proxy Check**:
  - The Vite dev server proxies `/api/v1` requests to `http://localhost:8000`. The frontend navbar includes an active system health indicator pill showing real-time connectivity status.
