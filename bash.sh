#!/bin/bash

pip install virtualenv
virtualenv venv
source venv/bin/activate

pip install bs4
pip install lxml
pip install telebot
pip install matplotlib
pip install json

python3 main.py