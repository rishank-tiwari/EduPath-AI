# EduPath — Vercel-Only Production Deployment Guide

This document provides step-by-step instructions for deploying the **EduPath** application to production using **Vercel ONLY** as a single unified project hosting both the React + Vite frontend and the FastAPI backend serverless functions.

---

## Architecture Overview

```mermaid
graph TD
    Client[Browser / User] -->|HTTPS| VercelDomain[https://edupath-*.vercel.app]
    subgraph Vercel Single Project Deployment
        VercelDomain -->|/(.*) SPA Routes| ReactApp[React + Vite Static Bundle]
        VercelDomain -->|/api/v1/* API Routes| ServerlessPy[api/index.py - FastAPI Serverless Function]
    end
    ServerlessPy -->|Motor / PyMongo| Atlas[(MongoDB Atlas Cloud Database)]
    ServerlessPy -->|HTTPS API Key Protected| Gemini[Google Gemini API - gemini-3.6-flash]
```

---

## 1. Repository Structure for Vercel

```text
edupath/
├── api/
│   └── index.py            # Vercel Python entrypoint importing backend.app.main:app
├── backend/
│   ├── app/                # FastAPI application code
│   └── requirements.txt    # Backend Python dependencies
├── ai/                     # Agentic AI agents (Mentor, SkillGap, etc.)
├── frontend/
│   ├── src/                # React + Vite application
│   ├── package.json        # Frontend scripts & dependencies
│   └── vite.config.js      # Vite build configuration
├── requirements.txt        # Root Python dependencies for Vercel Python Runtime
├── vercel.json             # Vercel build & route rewrite configuration
└── .env.example            # Environment variable placeholders
```

---

## 2. Vercel Single Project Configuration (`vercel.json`)

The project root [vercel.json](file:///e:/Agentic%20AI%20ptoject/vercel.json) configures dual builds:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "handle": "filesystem"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/index.html"
    }
  ]
}
```

---

## 3. Environment Variables Setup (Vercel Project Settings)

Add the following environment variables in **Vercel -> Project Settings -> Environment Variables**:

### Backend Secrets (Serverless Runtime Only)
| Variable | Value / Format |
|---|---|
| `MONGODB_URI` | `mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority` |
| `MONGODB_DATABASE` | `edupath` |
| `JWT_SECRET` | Production secret key (e.g., generated via `openssl rand -hex 32`) |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |
| `LLM_PROVIDER` | `gemini` |
| `GEMINI_API_KEY` | Your secret Google Gemini API key |
| `GEMINI_MODEL` | `gemini-3.6-flash` |
| `ENVIRONMENT` | `production` |

### Frontend Variable (Exposed to Browser)
| Variable | Value |
|---|---|
| `VITE_API_BASE_URL` | `/api/v1` |

> [!IMPORTANT]
> Never set `GEMINI_API_KEY`, `MONGODB_URI`, or `JWT_SECRET` as `VITE_*` variables. They are strictly backend serverless environment variables.

---

## 4. MongoDB Atlas Setup Requirement

1. Create a Cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Under **Network Access**, add IP `0.0.0.0/0` to allow access from Vercel Serverless Functions.
3. Under **Database Access**, create a database user with read/write access.
4. Copy the connection string to `MONGODB_URI`.

---

## 5. Local Vercel Testing

Run local emulation before pushing to production:

```bash
# Log in to Vercel
npx vercel login

# Link project
npx vercel link

# Run local Vercel server (serves frontend + FastAPI on single origin)
npx vercel dev
```

---

## 6. Deployment Command

Deploy to Vercel Production using Vercel CLI or GitHub integration:

```bash
npx vercel deploy --prod
```

---

## 7. Production Health & Smoke Test

1. **API Health Check**:
   ```bash
   curl https://<YOUR-VERCEL-DOMAIN>.vercel.app/api/v1/health
   ```
   Expected output:
   ```json
   {
     "status": "ok",
     "database": "connected"
   }
   ```

2. **Frontend SPA Verification**:
   - Access `https://<YOUR-VERCEL-DOMAIN>.vercel.app/`
   - Test Direct Links: `/login`, `/my-path`, `/practice`, `/mentor`, `/profile`

3. **End-to-End User Flow**:
   - Register new user -> Login -> Choose Target Role -> Upload Resume -> Assess Skill Gaps -> Generate Learning Path -> Complete Practice Tasks -> Chat with Gemini AI Mentor.

---

## 8. File Upload & Storage Behavior

- Uploaded PDF/DOCX resumes are processed in-memory using byte streams (`io.BytesIO`).
- Parsed skills, experiences, and evidence records are saved directly in MongoDB Atlas.
- Uploaded files are **not stored on disk**, ensuring 100% compatibility with Vercel Serverless Functions.

---

## 9. Troubleshooting

- **404 on API Routes**: Verify `vercel.json` maps `/api/(.*)` to `api/index.py`.
- **404 on Refreshing React Pages**: Verify `vercel.json` includes SPA rewrite to `frontend/index.html`.
- **MongoDB Connection Timeout**: Ensure `0.0.0.0/0` is added to Atlas Network Access whitelist.
