# Navigate to your project directory
cd befastapi/Moodle_VirtualAssistant_BE || exit 1  # Exit if the directory change fails

# Pull the latest code
if ! git pull origin main; then
  echo "Failed to pull the latest code"
  exit 1
fi
source venv/bin/activate
# Kill any existing Uvicorn process running on port 5001
if ! pkill -f "uvicorn.*--port 5001"; then
  echo "No existing Uvicorn process found to kill"
fi

# Wait for a moment to ensure the process is terminated
sleep 2

# Start Uvicorn in the background on port 5001
if ! nohup uvicorn app.main:app --host 0.0.0.0 --port 5001 & then
  echo "Failed to start Uvicorn"
  exit 1
fi

echo "Uvicorn started successfully"

