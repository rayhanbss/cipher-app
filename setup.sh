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

# 3. Run Tailwind in watch mode (optional, comment out if not needed)
# if [ -f package.json ]; then
#     npm install
#     npx tailwindcss -i ./static/input.css -o ./static/output.css --watch
# fi

python ./app.py

echo "Setup complete! Activate your venv with: source .venv/bin/activate"
