# 🚀 Deployment Guide

This guide covers deploying GigProtect AI on **Render** (recommended) and **Vercel** (frontend only).

---

## 📋 Deployment Options

### Option 1: Render (Full-Stack) - RECOMMENDED ✅

Render supports both **Node.js (Next.js frontend)** and **Python (FastAPI backend)** with integrated MongoDB.

#### Steps:

1. **Connect Repository**
   - Go to [render.com](https://render.com)
   - Click **New Blueprint** or **Dashboard** → **Create** → **Blueprint**
   - Sign in with GitHub and authorize access
   - Select repository: `ayveHacks/QuickCommerce-InsuranceAI`

2. **Deploy**
   - Render auto-detects `render.yaml`
   - Review services:
     - `gigprotect-frontend` (Next.js on Node.js 18)
     - `gigprotect-backend` (FastAPI on Python 3.11)
     - `mongodb` (MongoDB database)
   - Click **Create Blueprint**

3. **Monitor Deployment**
   - Frontend: `https://gigprotect-frontend.onrender.com`
   - Backend: `https://gigprotect-backend.onrender.com`
   - Watch build logs for errors

4. **Access Application**
   ```
   Frontend: https://gigprotect-frontend.onrender.com
   Backend API: https://gigprotect-backend.onrender.com/api/v1
   Swagger Docs: https://gigprotect-backend.onrender.com/docs
   ```

#### Environment Variables (Auto-set in `render.yaml`):
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL
- `MONGODB_URI`: Auto-populated from MongoDB service
- `MONGODB_DB`: `gigprotect_ai`
- `ALLOWED_ORIGINS`: Frontend URL
- `SCHEDULER_ENABLED`: `true`

---

### Option 2: Vercel (Frontend Only)

If you want to deploy only the frontend on Vercel, deploy the backend separately on Render or another service.

#### Steps:

1. **Connect Repository**
   - Go to [vercel.com](https://vercel.com)
   - Click **Add New** → **Project**
   - Select `QuickCommerce-InsuranceAI` repository
   - Click **Import**

2. **Configure Settings**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

3. **Environment Variables**
   - Add `NEXT_PUBLIC_API_BASE_URL`: `https://gigprotect-backend.onrender.com/api/v1`

4. **Deploy Backend Separately**
   - Deploy backend to Render, Railway, or Heroku
   - Update `NEXT_PUBLIC_API_BASE_URL` to match your backend URL

---

## 🛠️ Local Development

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Run Locally

```bash
# Using Docker (easiest)
docker compose up --build

# Or manually:

# Terminal 1: Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## 📝 Configuration Files

### `render.yaml`
- Full-stack deployment for Render
- Defines frontend, backend, and MongoDB services
- Environment variables and build commands

### `vercel.json`
- Frontend-only deployment for Vercel
- Includes build and install commands
- Points to `frontend` directory

### `docker-compose.yml`
- Local development with MongoDB, FastAPI backend, and Next.js frontend
- Useful for testing before deployment

---

## 🔍 Troubleshooting

### "No Next.js version detected" (Vercel)
**Solution**: Make sure Root Directory is set to `frontend` in Vercel project settings.

### Backend API connection fails
**Solution**: Update `NEXT_PUBLIC_API_BASE_URL` environment variable to match your backend URL.

### MongoDB connection error
**Solution**: On Render, MongoDB URL is auto-populated. Locally, ensure MongoDB is running via Docker.

### Build fails on Render
**Solution**: Check build logs in Render dashboard. Ensure `render.yaml` syntax is correct.

---

## 📊 Recommended Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (Next.js)              │
│  https://gigprotect-frontend.onrender   │
└─────────────┬──────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│   Backend (FastAPI/Uvicorn)            │
│  https://gigprotect-backend.onrender    │
└─────────────┬──────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         MongoDB Database                │
│  (Managed by Render)                    │
└─────────────────────────────────────────┘
```

---

## ✅ Post-Deployment Checklist

- [ ] Frontend loads successfully
- [ ] Backend API responds to requests
- [ ] Swagger API docs accessible
- [ ] Database connection works
- [ ] Worker registration/login functions
- [ ] Admin dashboard accessible
- [ ] Demo data seeds properly
- [ ] Claims auto-generation works

---

## 📞 Support

For issues:
1. Check deployment logs (Render/Vercel dashboard)
2. Review environment variables
3. Verify database connectivity
4. Check API endpoint URLs match configuration

Good luck! 🚀
