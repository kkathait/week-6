import requests
import pandas as pd

from genius_api import ACCESS_TOKEN


class Genius:
    BASE_URL = "https://api.genius.com"

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def _get(self, endpoint, params=None):
        response = requests.get(
            f"{self.BASE_URL}{endpoint}",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_artist(self, search_term):
        search_data = self._get(
            "/search",
            params={"q": search_term}
        )

        artist_id = (
            search_data["response"]["hits"][0]
            ["result"]["primary_artist"]["id"]
        )

        return self._get(f"/artists/{artist_id}")

    def get_artists(self, search_terms):
        artists = []

        for search_term in search_terms:
            artist_data = self.get_artist(search_term)
            artist = artist_data["response"]["artist"]

            artists.append({
                "search_term": search_term,
                "artist_name": artist["name"],
                "artist_id": artist["id"],
                "followers_count": artist.get("followers_count")
            })

        return pd.DataFrame(artists)


genius = Genius(access_token=ACCESS_TOKEN)
with open("artists.txt", "r", encoding="utf-8") as file:
    artists = [line.strip() for line in file if line.strip()]

df = genius.get_artists(artists)

df.to_csv("artists.csv", index=False)

print(f"Saved {len(df)} artists to artists.csv")