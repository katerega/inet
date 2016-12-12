import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OPS_KEY = os.environ.get("OPS_KEY")
OPS_SECRET = os.environ.get("OPS_SECRET")
TWITTER_CONSUMER_ACCESS = os.environ['TWITTER_CONSUMER_ACCESS']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS = os.environ['TWITTER_ACCESS']
TWITTER_SECRET = os.environ['TWITTER_SECRET']
