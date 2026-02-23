"""
Module for enriching song metadata from non-Spotify sources.
"""

import logging
from typing import Any, Dict, Optional

import requests

from spotdl.types.song import Song

from ytmusicapi import YTMusic

logger = logging.getLogger(__name__)

# Lazily initialize YTMusic client
_ytm_client = None

def get_ytm_client() -> YTMusic:
    global _ytm_client
    if _ytm_client is None:
        _ytm_client = YTMusic()
    return _ytm_client


def get_deezer_metadata(query: str) -> Dict[str, Any]:
    """
    Search Deezer for track metadata.

    ### Arguments
    - query: The search query.

    ### Returns
    - A dictionary containing track metadata.
    """

    url = f"https://api.deezer.com/search?q={query}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("data"):
            return data["data"][0]
    except Exception as exc:
        logger.error("Failed to fetch Deezer metadata: %s", exc)

    return {}


def get_itunes_metadata(query: str) -> Dict[str, Any]:
    """
    Search iTunes for track metadata.

    ### Arguments
    - query: The search query.

    ### Returns
    - A dictionary containing track metadata.
    """

    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            return data["results"][0]
    except Exception as exc:
        logger.error("Failed to fetch iTunes metadata: %s", exc)

    return {}


def get_ytm_metadata(query: str) -> Dict[str, Any]:
    """
    Search YouTube Music for track metadata.

    ### Arguments
    - query: The search query.

    ### Returns
    - A dictionary containing track metadata.
    """

    try:
        client = get_ytm_client()
        search_results = client.search(query, filter="songs", limit=1)

        if search_results:
            return search_results[0]
    except Exception as exc:
        logger.error("Failed to fetch YouTube Music metadata: %s", exc)

    return {}


def enrich_song_metadata(song: Song) -> Song:
    """
    Enrich song metadata using Deezer and iTunes.

    ### Arguments
    - song: The Song object to enrich.

    ### Returns
    - The enriched Song object.
    """

    query = f"{song.artist} - {song.name}"

    # Try Deezer for ISRC and structural metadata
    deezer_data = get_deezer_metadata(query)
    if deezer_data:
        if not song.isrc:
            song.isrc = deezer_data.get("isrc") or deezer_data.get("isrc_code")
        if song.track_number == 0:
             song.track_number = deezer_data.get("track_position", 1)
        if song.disc_number == 0:
             song.disc_number = deezer_data.get("disk_number", 1)
        if not song.album_name and deezer_data.get("album"):
            song.album_name = deezer_data["album"].get("title")
        if not song.artist_cover_url and deezer_data.get("artist"):
            song.artist_cover_url = deezer_data["artist"].get("picture_xl") or deezer_data["artist"].get("picture_medium")

    # Try iTunes for high-res artwork
    itunes_data = get_itunes_metadata(query)
    if itunes_data:
        artwork_url = itunes_data.get("artworkUrl100")
        if artwork_url:
            # Upscale to 1000x1000
            song.cover_url = artwork_url.replace("100x100bb.jpg", "1000x1000bb.jpg")

        if itunes_data.get("primaryGenreName"):
            song.genres = [itunes_data["primaryGenreName"]]

    # Try YouTube Music for high-res artwork and artist art
    ytm_data = get_ytm_metadata(query)
    if ytm_data:
        if not song.cover_url and ytm_data.get("thumbnails"):
            # Get the highest resolution thumbnail
            thumbnails = ytm_data["thumbnails"]
            best_thumb = max(thumbnails, key=lambda x: x.get("width", 0))
            song.cover_url = best_thumb["url"]

        if not song.artist_cover_url and ytm_data.get("artists"):
            try:
                artist_id = ytm_data["artists"][0].get("browseId")
                if artist_id:
                    artist_data = get_ytm_client().get_artist(artist_id)
                    if artist_data.get("thumbnails"):
                        artist_thumbs = artist_data["thumbnails"]
                        best_artist_thumb = max(artist_thumbs, key=lambda x: x.get("width", 0))
                        song.artist_cover_url = best_artist_thumb["url"]
            except Exception:
                pass

    # Ensure all mandatory fields are not None to satisfy mutagen and other tools
    # These were potentially None if Song.from_missing_data was used
    if song.genres is None:
        song.genres = []
    if song.track_number is None or song.track_number == 0:
        song.track_number = 1
    if song.tracks_count is None or song.tracks_count == 0:
        song.tracks_count = 1
    if song.disc_number is None or song.disc_number == 0:
        song.disc_number = 1
    if song.disc_count is None or song.disc_count == 0:
        song.disc_count = 1
    
    if not song.year and song.date:
        try:
            song.year = int(song.date[:4])
        except (ValueError, TypeError):
            song.year = 2024
    
    if song.year is None:
        song.year = 2024

    if song.date is None:
        song.date = ""
    if song.publisher is None:
        song.publisher = ""
    if song.copyright_text is None:
        song.copyright_text = ""
    if song.isrc is None:
        song.isrc = ""
    if song.album_id is None:
        song.album_id = "0"
    if song.album_artist is None:
        song.album_artist = song.artist if song.artist else ""
    if song.album_name is None:
        song.album_name = ""
    if song.popularity is None:
        song.popularity = 0
    if song.explicit is None:
        song.explicit = False

    return song
