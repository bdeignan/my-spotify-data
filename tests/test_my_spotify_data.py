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
    # Set up the image URL and filename
    image_url = "https://i.scdn.co/image/ab67616d0000b273bc97aa53df9447f9dc1b4dcb"
    # filename = tmp_path / image_url.split("/")[-1]
    file_path = (
        tmp_path / image_url.split("/")[-1]
    )  # tmp_path.mkdir("mydir").join("myfile")
    new_file_path = download.download_image(image_url, file_path)
    assert new_file_path
    assert imghdr.what(new_file_path) == "jpeg"
