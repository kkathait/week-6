import requests
import pandas as pd


class Genius:
    """A client for retrieving artist information from the Genius API."""

    BASE_URL = "https://api.genius.com"

    def __init__(self, access_token):
        """Initialize the client with a Genius API access token."""
        if not access_token:
            raise ValueError("An access token is required.")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })

    def _get(self, endpoint, params=None):
        """Send an authenticated GET request to the Genius API."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = self.session.get(
            url,
            params=params,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    def _search_artist(self, search_term):
        """Find the primary artist from the first search result."""
        data = self._get(
            "search",
            params={"q": search_term}
        )

        hits = data.get("response", {}).get("hits", [])

        if not hits:
            return None

        return hits[0].get("result", {}).get("primary_artist")

    def get_artist(self, search_term):
        """
        Return the Genius API JSON dictionary for the matched artist.

        The artist ID is extracted from the first search hit.
        """
        artist = self._search_artist(search_term)

        if not artist or not artist.get("id"):
            return {}

        artist_id = artist["id"]
        return self._get(f"artists/{artist_id}")

    def get_artists(self, search_terms):
        """
        Return a DataFrame with artist names, IDs, and follower counts.
        """
        rows = []

        for search_term in search_terms:
            artist_data = self.get_artist(search_term)

            artist = (
                artist_data.get("response", {}).get("artist", {})
            )

            rows.append({
                "search_term": search_term,
                "artist_name": artist.get("name"),
                "artist_id": artist.get("id"),
                "followers_count": artist.get("followers_count"),
            })

        return pd.DataFrame(
            rows,
            columns=[
                "search_term",
                "artist_name",
                "artist_id",
                "followers_count",
            ],
        )

    