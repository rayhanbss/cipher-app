#!/bin/bash
# Setup script for Flask + Tailwind project

set -e

# 1. Create and activate Python virtual environment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

# 2. Install Python requirements
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# 3. Install Node.js dependencies
if [ -f package.json ]; then
    npm install
fi

# 4. Run Tailwind in watch mode (optional, comment out if not needed)
npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch

echo "Setup complete! Activate your venv with: source .venv/bin/activate"
