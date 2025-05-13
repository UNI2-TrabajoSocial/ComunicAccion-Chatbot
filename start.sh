#!/usr/bin/env bash
set -eu
export PYTHONUNBUFFERED=true

python3 -m pip install -r requirements.txt

export FLASK_APP=app/server.py
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run --host=0.0.0.0 --port="${PORT:-3000}" --reload
