cd befastapi/Moodle_VirtualAssistant_BE
git pull origin main
source venv/bin/activate
pkill -f uvicorn
nohup uvicorn app.main:app --host 0.0.0.0 --reload --port 5001 &