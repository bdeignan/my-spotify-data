import logging
import json
from pathlib import Path
from my_spotify_data import Spotify as sp

logger = logging.getLogger(__name__)

test_path = Path(__file__).parents[1] / "tests"

artist = "Radiohead"
track_name = "Creep"
search_str = f"track:{track_name} artist:{artist}"

result = sp.search(search_str, type="track")
success = "tracks" in result
logger.info(f"Found search results: {success}")

if success:
    with open(test_path / "example-response.json", "w") as f:
        json.dump(result, f)
    logger.info(f"Created test input file: {test_path / 'example-response.json'}")