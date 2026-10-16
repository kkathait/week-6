import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class Genius:
    def __init__(self, access_token=None):
        
        load_dotenv()
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")
        self.base_url = "https://api.genius.com"

    def search(self, search_term):
    
        url = f"{self.base_url}/search"

        params = {
            "q": search_term,
            "access_token": self.access_token
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_artist(self, search_term):
    
        search_data = self.search(search_term)

        artist_id = search_data["response"]["hits"][0]["result"]["primary_artist"]["id"]

        
        url = f"{self.base_url}/artists/{artist_id}"

        params = {
            "access_token": self.access_token
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_artists(self, search_terms):
        
        records = []

        for search_term in search_terms:
            artist_data = self.get_artist(search_term)
            artist = artist_data["response"]["artist"]

            # find our terms
            records.append({
                "search_term": search_term,
                "artist_name": artist["name"],
                "artist_id": artist["id"],
                "followers_count": artist.get("followers_count")
            })

        return pd.DataFrame(records)