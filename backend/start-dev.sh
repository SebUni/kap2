#!/bin/bash
cd /opt/lampp/htdocs/kap2/backend
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
