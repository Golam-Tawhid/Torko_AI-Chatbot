#!/bin/bash

# Install frontend dependencies and build React app
echo "Building React frontend..."
cd frontend
npm install
npm run build
cd ..

# Install backend dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"
