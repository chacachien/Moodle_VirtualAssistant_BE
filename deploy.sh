# Navigate to your project directory
cd befastapi/Moodle_VirtualAssistant_BE || exit 1  # Exit if the directory change fails

# Pull the latest code
if ! git pull origin main; then
  echo "Failed to pull the latest code"
  exit 1
fi
source venv/bin/activate

# Check if the PM2 process is already running
pm2 describe my-fastapi-app > /dev/null
RUNNING=$?

if [ "$RUNNING" -ne 0 ]; then
  # Process not found, start it
  pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 5001" --name my-fastapi-app
else
  # Process found, restart it
  pm2 restart my-fastapi-app
fi

echo "Uvicorn application is now running under PM2"
