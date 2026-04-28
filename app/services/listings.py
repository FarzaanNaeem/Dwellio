import json
from pathlib import Path


LISTINGS_PATH = Path(__file__).resolve().parent.parent / "data" / "mock_listings.json"


def load_listings() -> list[dict]:
    with LISTINGS_PATH.open("r", encoding="utf-8") as file:
        listings = json.load(file)

    if not isinstance(listings, list):
        raise ValueError("Mock listings data must be a list.")

    return listings
