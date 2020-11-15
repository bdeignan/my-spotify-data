import json
import imghdr
from pathlib import Path
from my_spotify_data import __version__, download

test_path = Path(__file__).parents[1] / "tests"

with open(test_path / "example-response.json", "r") as f:
    response = json.load(f)


def test_version():
    assert __version__ == "0.1.0"


def test_search_response_basic():
    assert "tracks" in response


def test_download_jpeg(tmp_path):
    image_url = "https://i.scdn.co/image/ab67616d0000b273bc97aa53df9447f9dc1b4dcb"
    file_path = tmp_path / image_url.split("/")[-1]
    new_file_path = download.get_image(image_url, file_path)
    assert new_file_path
    assert imghdr.what(new_file_path) == "jpeg"


def test_get_track_ids():
    id_list = download.get_track_ids(response)
    assert len(id_list) > 0


def test_get_track_features():
    feats = download.get_features("6b2oQwSGFkzsMtQruIWm2p")
    assert feats
    assert isinstance(feats, dict)
    empty_feats = download.get_features("madeup")
    assert empty_feats is None


def test_get_album():
    album = download.get_album(response)
    data = next(album)
    assert data["name"] == "Pablo Honey"
