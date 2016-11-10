import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
SKIP_TAGS = os.environ['SKIP_TAGS'].split()
