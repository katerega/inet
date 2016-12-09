import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OPS_KEY = os.environ.get("OPS_KEY")
OPS_SECRET = os.environ.get("OPS_SECRET")
