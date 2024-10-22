cd befastapi/Moodle_VirtualAssistant_BE
git pull origin main
source venv/bin/activate
pkill -f "uvicorn.*--port 5001"
sleep 3
nohup uvicorn app.main:app --host 0.0.0.0 --port 5001 &
