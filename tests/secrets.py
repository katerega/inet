# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPS_KEY = os.environ['OPS_KEY']
OPS_SECRET = os.environ['OPS_SECRET']
