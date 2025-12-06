#!/bin/bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python init_admin.py
python populate_foods.py
