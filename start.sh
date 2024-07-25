#!/usr/bin/env bash
python -m venv /data/venv
source /data/venv/bin/activate
pip install -r requirements.txt

flask run