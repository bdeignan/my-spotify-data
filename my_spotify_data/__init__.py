"""Handle logging, paths and Spotify API object

NOTE: Must first run ../bin/initial_spotipy_call.py before using
Spotify API through `spotipy`.
"""
import logging
import os
from pathlib import Path

import spotipy
from dotenv import find_dotenv, load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(pathname)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

__version__ = "0.1.0"

load_dotenv(find_dotenv())

try:
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv("SPOT_CLIENT_ID"),
        client_secret=os.getenv("SPOT_CLIENT_SECRET"),
    )
    Spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    logger.info("Spotify API class succesfully initialized!")
except Exception as e:
    logger.error(f"Failed to initialize Spotify API class: {e}")
