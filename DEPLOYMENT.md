# Deployment Guide

## Local Deployment

### Quick Start (Windows)
```powershell
.\start.ps1
```

### Quick Start (Linux/Mac)
```bash
chmod +x start.sh
./start.sh
```

### Manual Start
```bash
python run_local.py
# or
streamlit run live_dashboard.py
```

## GitHub Pages Deployment

### Option 1: Streamlit Cloud (Recommended)

Streamlit Cloud is the best way to deploy Streamlit applications:

1. **Go to Streamlit Cloud**: https://share.streamlit.io
2. **Sign in** with your GitHub account
3. **Deploy app**:
   - Repository: `KarimElhakim/gold-price-prediction`
   - Branch: `main`
   - Main file: `live_dashboard.py`
4. **Set environment variables**:
   - `KAGGLE_API_TOKEN`
   - `GOLDAPI_API_KEY`
5. **Deploy!**

Your app will be live at: `https://your-app-name.streamlit.app`

### Option 2: GitHub Actions (Automated)

The workflow in `.github/workflows/deploy.yml` automatically:
- Trains models on push
- Creates deployment packages
- Stores artifacts for 30 days

To use:
1. Set GitHub Secrets:
   - `KAGGLE_API_TOKEN`
   - `GOLDAPI_API_KEY`
2. Push to main branch
3. Check Actions tab for deployment status

### Option 3: Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "live_dashboard.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t gold-price-prediction .
docker run -p 8501:8501 gold-price-prediction
```

## Environment Variables

Set these for production deployment:

```bash
export KAGGLE_API_TOKEN="your-token"
export GOLDAPI_API_KEY="your-key"
```

Or use `.env` file (not committed to git):
```
KAGGLE_API_TOKEN=your-token
GOLDAPI_API_KEY=your-key
```

## Running the Application

### Dashboard Mode (Default)
```bash
python run_app.py dashboard
```

### Full Cycle (Train + Predict)
```bash
python main.py --mode full
```

### Train Models Only
```bash
python main.py --mode train
```

## Troubleshooting

### Models Not Found
If you see "Models not loaded", train them first:
```bash
python main.py --mode train
```

### Dependencies Issues
Install all dependencies:
```bash
pip install -r requirements.txt
```

### Port Already in Use
Change the port:
```bash
streamlit run live_dashboard.py --server.port 8502
```

