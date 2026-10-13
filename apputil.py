import requests


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
        # Search Genius
        search_data = self._get(
            "/search",
            params={"q": search_term}
        )

        # Artist ID from first hit
        artist_id = search_data["response"]["hits"][0]["result"]["primary_artist"]["id"]

        # Get artist info
        artist_data = self._get(f"/artists/{artist_id}")

        # Return the artist JSON dictionary
        return artist_data

import requests
import pandas as pd
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


from dotenv import load_dotenv
import os

def load_artists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def main():
    load_dotenv()

    access_token = os.getenv("ACCESS_TOKEN")

    genius = Genius(access_token=access_token)

    artists = load_artists("artists.txt")

    df = genius.get_artists(artists)

    df.to_csv("artists.csv", index=False)

    print(f"Saved {len(df)} artists to artists.csv")

