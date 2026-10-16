import os
import requests
import pandas as pd
from dotenv import load_dotenv


class Genius:
    def __init__(self, access_token=None):
        """Initialize the Genius API client."""
        load_dotenv()
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")
        self.base_url = "https://api.genius.com"

        if not self.access_token:
            raise ValueError("Genius API access token is missing.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}"
        })

    def search(self, search_term):
        """Search the Genius API for a given term."""
        url = f"{self.base_url}/search"

        response = self.session.get(
            url,
            params={"q": search_term},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_artist(self, search_term):
        """Return the Genius API JSON dictionary for an artist."""
        search_data = self.search(search_term)
        hits = search_data.get("response", {}).get("hits", [])

        if not hits:
            return {}

        artist = hits[0].get("result", {}).get("primary_artist", {})
        artist_id = artist.get("id")

        if not artist_id:
            return {}

        url = f"{self.base_url}/artists/{artist_id}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        return response.json()

    def get_artists(self, search_terms):
        """Return a DataFrame of artist information."""
        records = []

        for search_term in search_terms:
            artist_data = self.get_artist(search_term)
            artist = artist_data.get("response", {}).get("artist", {})

            records.append({
                "search_term": search_term,
                "artist_name": artist.get("name"),
                "artist_id": artist.get("id"),
                "followers_count": artist.get("followers_count")
            })

        return pd.DataFrame(
            records,
            columns=[
                "search_term",
                "artist_name",
                "artist_id",
                "followers_count"
            ]
        )
