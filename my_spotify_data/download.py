import logging
import pathlib
import shutil
from typing import Union, List

import requests

from my_spotify_data import Spotify as sp

logger = logging.getLogger(__name__)


def get_image(
    image_url: str, save_path: Union[str, pathlib.Path]
) -> Union[pathlib.Path, None]:
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(save_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

        logger.info(f"Image sucessfully Downloaded: {save_path}")
        return save_path
    else:
        logger.info("Image Couldn't be retreived")
        return None


def get_track_ids(response: dict) -> List[str]:
    return [track["id"] for track in response["tracks"]["items"]]


def get_features(track_id: str) -> Union[dict, None]:
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return None