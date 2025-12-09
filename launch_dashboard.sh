#!/bin/bash

# Launch script for Bike-Sharing Station Planner Dashboard

echo "🚴 Starting Bike-Sharing Station Planner Dashboard..."
echo ""
echo "Opening your browser to http://localhost:8501"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""

cd "$(dirname "$0")"
streamlit run app.py
