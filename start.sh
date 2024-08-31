#!/usr/bin/env bash
python -m venv /data/venv
source /data/venv/bin/activate
pip install -r requirements.txt

flask --app nightbot-web.py run -h 0.0.0.0 --debug