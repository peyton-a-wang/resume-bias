#!/usr/bin/ env bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 selenium_scraper.py