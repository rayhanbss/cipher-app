#!/bin/bash
# Setup script for Flask + Tailwind project

set -e

# 1. Create and activate Python virtual environment
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# 2. Install Python requirements
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# 3. Install Node.js dependencies
if [ -f package.json ]; then
    npm install
fi

# 4. Run Tailwind in watch mode (optional, comment out if not needed)
npx tailwindcss -i ./static/input.css -o ./static/output.css --watch

echo "Setup complete! Activate your venv with: source .venv/bin/activate"
