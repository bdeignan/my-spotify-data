"""Take in csv as argument and do 3 things:
1. Get Spotify track id
2. Get track numeric features
3. Download track's album image to data/

For 1 and 2, write to CSV along with another log CSV for:
trackid, track name, artist, features_found (bool) and image url (None or Str)
"""
import argparse

from my_spotify_data.download import get_track_ids


# for artist, song in history:
#     r = search(artist, song)
#     # get track ids
#     get_track_ids(r)
#     # get song features
#     get song features(r)
#     found_image = False
#     for item in r[tracls][items]
#         album name = item[album][name]
#         album id = ...
#         album uri ...
#         album release date = ...
#         album images = [image[url] for image in item[album][images]]
#         while not found_image:
#             for url in album images:
#                 image_path = download_image(...)
#                 found_image = image_path != None
#         album image = image_path
#         if found_image:
#             break # next song
