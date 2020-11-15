"""Take in csv as argument and do 3 things:
1. Get Spotify track id
2. Get track numeric features
3. Download track's album image to data/

For 1 and 2, write to CSV along with another log CSV for:
trackid, track name, artist, features_found (bool) and image url (None or Str)
"""
import argparse
import logging
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from my_spotify_data import download

logger = logging.getLogger(__name__)
log_path = Path(__file__).resolve().parents[1] / "logs"
log_path.mkdir(parents=True, exist_ok=True)
log_file = f"{Path(__file__).stem}_{datetime.now().strftime('%H_%M_%S_%d_%m_%Y')}.log"
fileHandler = logging.FileHandler(log_path / log_file)
logger.addHandler(fileHandler)


song_features = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "type",
    "id",
    "uri",
    "track_href",
    "analysis_url",
    "duration_ms",
    "time_signature",
]

current_milli_time = lambda: int(round(time.time() * 1000))


def is_valid_file(arg):
    if not Path(arg).exists():
        parser.error("The file %s does not exist!" % arg)
    else:
        return Path(arg)  # return an open file handle


def album_info():
    info = ["name", "id", "uri", "release_date", "image_url", "image_path"]
    return ["album_" + item for item in info]


def dedupe_history(history: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["artist_name", "track_name"]
    return (
        history.sort_values(group_cols + ["end_time"])
        .groupby(group_cols, as_index=False)
        .first()
        .copy()
    )


def update_row_with_dict(dictionary, dataframe, index):
    for key in dictionary.keys():
        dataframe.loc[index, key] = dictionary.get(key)


parser = argparse.ArgumentParser(
    description="Augment listening history data using Spotify API"
)
parser.add_argument(
    "-i",
    "--input",
    dest="filepath",
    required=True,
    help="Path to listening history CSV",
    metavar="FILE",
    type=is_valid_file,
)

parser.add_argument(
    "-a",
    "--album-images",
    default=Path(__file__).resolve().parents[1] / "data" / "albums",
    help="Path to image files",
    metavar="FILE",
    type=is_valid_file,
)

parser.add_argument(
    "-o",
    "--output-path",
    default=Path(__file__).resolve().parents[1] / "data" / "final",
    help="Path to augmented history data",
    metavar="FILE",
    type=is_valid_file,
)

if __name__ == "__main__":
    args = parser.parse_args()
    logger.info(f"Input file: {args.filepath}")
    logger.info(f"Save location for album images: {args.album_images}")
    timehex = "{0:x}".format(current_milli_time())
    outfile = args.output_path / f"{args.filepath.stem}_augmented_{timehex}.csv"
    logger.info(f"Save location for final dataset: {outfile}")
    args.album_images.mkdir(parents=True, exist_ok=True)
    args.output_path.mkdir(parents=True, exist_ok=True)
    # read in data
    history = pd.read_csv(args.filepath)
    # add new columns to get data for
    newcols = ["track_id"] + album_info()
    history = pd.concat([history, pd.DataFrame(columns=newcols + song_features)])
    # make new columns strings
    history[newcols] = history[newcols].astype(str)
    history["found_image"] = False
    # Only keep first time listening to track
    logger.debug(history.head())
    logger.debug(f"Original shape of history: {history.shape}")
    history = dedupe_history(history)
    logger.debug(f"Deduped shape of history: {history.shape}")

    # brute force album info
    # TODO: there's gotta be a smarter, async way to do this
    for i, row in history.iterrows():
        logger.info(
            f"Found {history['found_image'].sum()} out of {history.shape[0]} images so far."
        )
        logger.info(f"Updating row: {(row['artist_name'],row['track_name'])}")
        data = download.search_track(
            artist_name=row["artist_name"], track_name=row["track_name"]
        )
        # get first track id in list of ids
        track_ids = download.get_track_ids(data)
        track_id = track_ids[0] if track_ids else None
        history.at[i, "track_id"] = track_id
        # features
        features = download.get_features(track_id)
        if features:
            update_row_with_dict(features, history, i)
        else:
            logger.info(
                f"No features found for track_id: {track_id}, name: {row.track_name}"
            )

        # album info:
        album_generator = download.get_album(data)
        found_image = row["found_image"]

        while not found_image:
            res = None
            image_url = None
            try:
                curr_album = next(album_generator)
            except StopIteration:
                logger.info(
                    f"No album images found for track_id: {track_id}, name: {row.track_name}"
                )
                break
            logger.debug(f"Searching album cover for: {curr_album}")
            if curr_album["images"]:
                for image in curr_album["images"]:
                    # exludes larger image files of height 640
                    if image.get("height", 501) > 500:
                        continue
                    # check the rate limits here. I keep getting stuck
                    res = download.get_image(
                        image["url"], args.album_images / curr_album["id"]
                    )
                    if res:
                        image_url = image["url"]
                        found_image = True
                        break

            if found_image:
                to_update = {
                    "found_image": found_image,
                    "album_name": curr_album["name"],
                    "album_id": curr_album["id"],
                    "album_uri": curr_album["uri"],
                    "album_image_path": res,
                    "album_image_url": image_url,
                    "album_release_date": curr_album["release_date"],
                }
                logger.info(f"Found album info: {to_update}")
                update_row_with_dict(to_update, history, i)

        logger.info(f"Appending row {i} to final csv.")
        history.iloc[[i]].to_csv(
            outfile, mode="a", header=not outfile.exists(), index=False
        )

    logger.info(f"FINISHED. Data saved to {outfile}")
