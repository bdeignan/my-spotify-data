"""Use this file to initially authorize your app with spotify API. 
See details: https://spotipy.readthedocs.io/en/2.6.1/#authorization-code-flow
"""
import os
from pathlib import Path

import dotenv
import spotipy.util as util

dotenv.load_dotenv(Path(__file__).parents[1] / ".env")
assert os.getenv("SPOT_CLIENT_ID")  # None evals to False here

# TODO: rename env vars to automatically captured by spotipy
username = os.getenv("SPOT_USERNAME")
client_id = os.getenv("SPOT_CLIENT_ID")
client_secret = os.getenv("SPOT_CLIENT_SECRET")
redirect_uri = "https://localhost:7777/callback"
scope = "user-read-recently-played"

token = util.prompt_for_user_token(
    username=username,
    scope=scope,
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
)

print(token)
