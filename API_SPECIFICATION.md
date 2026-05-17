# 🐍 Anaconda Setup Guide - IBM Bob Copilot

## Using Anaconda/Conda Environment

If you have Anaconda installed, follow these steps to run the application.

---

## Step 1: Open Anaconda Prompt

**Important**: You must use **Anaconda Prompt** (not regular PowerShell) for conda commands.

1. Press `Windows Key`
2. Type "Anaconda Prompt"
3. Click on "Anaconda Prompt" to open it

---

## Step 2: Navigate to Project Directory

```bash
cd "c:\Users\bau\Documents\IBM BOB"
```

---

## Step 3: Create Conda Environment

```bash
# Create a new conda environment named IBM with Python 3.11
conda create -n IBM python=3.11 -y

# Activate the environment
conda activate IBM
```

You should see `(IBM)` appear at the beginning of your prompt.

---

## Step 4: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- Streamlit
- And all other dependencies

---

## Step 5: Run the Application

### Option A: Manual Start (Recommended for Anaconda)

**Terminal 1 - Backend:**
```bash
# Make sure you're in the project directory
cd "c:\Users\bau\Documents\IBM BOB"

# Activate environment
conda activate IBM

# Start backend
uvicorn app.main:app --reload --port 8000
```

Keep this terminal open. The backend will run at http://localhost:8000

**Terminal 2 - Frontend:**
Open a NEW Anaconda Prompt window:
```bash
# Navigate to project
cd "c:\Users\bau\Documents\IBM BOB"

# Activate environment
conda activate IBM

# Start frontend
streamlit run frontend/streamlit_app.py
```

The frontend will open automatically in your browser at http://localhost:8501

---

### Option B: Using PowerShell Script (May Not Work)

The `start_app.ps1` script expects a standard Python venv, not a conda environment. If you want to use it:

1. Open **Anaconda PowerShell Prompt** (not regular Anaconda Prompt)
2. Navigate to project: `cd "c:\Users\bau\Documents\IBM BOB"`
3. Activate conda: `conda activate IBM`
4. Try running: `.\start_app.ps1`

**Note**: This may not work because the script looks for `.\IBM\Scripts\Activate.ps1` which doesn't exist in conda environments.

---

## Step 6: Access the Application

Once both services are running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend UI** | http://localhost:8501 | Main user interface |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |

---

## Troubleshooting

### "conda: command not found"

**Problem**: Conda is not in your PATH

**Solution**:
1. Use **Anaconda Prompt** instead of regular PowerShell
2. Or add Anaconda to PATH:
   - Open Anaconda Navigator
   - Go to Environments
   - Click on your environment
   - Open terminal from there

---

### "Module not found" errors

**Problem**: Dependencies not installed

**Solution**:
```bash
conda activate IBM
pip install -r requirements.txt
```

---

### Port already in use

**Problem**: Port 8000 or 8501 is already being used

**Solution**:
```bash
# For backend, use a different port
uvicorn app.main:app --reload --port 8001

# Streamlit will automatically use 8502 if 8501 is taken
```

---

### Cannot activate conda environment

**Problem**: Environment doesn't exist

**Solution**:
```bash
# List all environments
conda env list

# If IBM doesn't exist, create it
conda create -n IBM python=3.11 -y
conda activate IBM
```

---

## Quick Reference Commands

```bash
# Create environment
conda create -n IBM python=3.11 -y

# Activate environment
conda activate IBM

# Deactivate environment
conda deactivate

# List environments
conda env list

# Delete environment (if needed)
conda env remove -n IBM

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload --port 8000

# Start frontend
streamlit run frontend/streamlit_app.py

# Check what's installed
pip list
```

---

## Complete Workflow

### First Time Setup:
```bash
# 1. Open Anaconda Prompt
# 2. Navigate to project
cd "c:\Users\bau\Documents\IBM BOB"

# 3. Create and activate environment
conda create -n IBM python=3.11 -y
conda activate IBM

# 4. Install dependencies
pip install -r requirements.txt
```

### Every Time You Run:
```bash
# Terminal 1 - Backend
cd "c:\Users\bau\Documents\IBM BOB"
conda activate IBM
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend (new Anaconda Prompt)
cd "c:\Users\bau\Documents\IBM BOB"
conda activate IBM
streamlit run frontend/streamlit_app.py
```

---

## Why Use Anaconda?

✅ **Pros**:
- Easy environment management
- Includes many scientific packages
- Good for data science projects
- Isolated environments

❌ **Cons**:
- Larger installation size
- Some scripts expect standard Python venv
- Need to use Anaconda Prompt

---

## Alternative: Standard Python venv

If you prefer to use standard Python instead of Anaconda:

1. Install Python from python.org
2. Use the standard setup in `QUICK_START.md`
3. The `start_app.ps1` script will work perfectly

---

## Need Help?

- **Anaconda Documentation**: https://docs.anaconda.com/
- **Conda Cheat Sheet**: https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html
- **Project Quick Start**: See `QUICK_START.md`
- **Docker Alternative**: See `DOCKER_DEPLOYMENT.md`