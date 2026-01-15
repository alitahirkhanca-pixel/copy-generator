# Psychic Copy Generator - Railway Deployment

This project has two services that need separate Railway deployments:

## Service 1: Backend API (Python/Flask)
- **Directory**: `backend/`
- **Port**: `5001`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Environment Variables**: 
  - `GEMINI_API_KEY` (required)

## Service 2: Frontend (React/Vite)
- **Directory**: Root (`/`)
- **Port**: `3000` or `$PORT`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `VITE_API_URL` = your backend Railway URL

## Setup Steps:

1. In Railway, create TWO services:
   - Service 1: "backend" → point to `backend/` folder
   - Service 2: "frontend" → point to root folder

2. For backend service:
   - Set root directory to `backend`
   - Add env var: `GEMINI_API_KEY`
   - Generate domain

3. For frontend service:
   - Set root directory to `.` (root)  
   - Add env var: `VITE_API_URL=https://your-backend.up.railway.app`
   - Generate domain

4. Update frontend to use `VITE_API_URL` instead of localhost
