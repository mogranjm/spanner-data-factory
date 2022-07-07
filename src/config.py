import os

from dotenv import load_dotenv

config = load_dotenv('.env')

env = os.environ

SPANNER_INSTANCE = env.get("SPANNER_INSTANCE")
SPANNER_DATABASE = env.get("SPANNER_DATABASE")
