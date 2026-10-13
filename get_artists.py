import os
from dotenv import load_dotenv
from apputil import Genius


def main():
    load_dotenv()

    genius = Genius(
        access_token=os.environ["ACCESS_TOKEN"]
    )

    with open("artists.txt", "r", encoding="utf-8") as file:
        search_terms = [
            line.strip()
            for line in file
            if line.strip()
        ]

    artists_df = genius.get_artists(search_terms)
    artists_df.to_csv("artists.csv", index=False)

    print(f"Saved {len(artists_df)} artists to artists.csv")


if __name__ == "__main__":
    main()