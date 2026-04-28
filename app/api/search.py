import re
from uuid import uuid4

from fastapi import APIRouter

from app.services.explanations import generate_explanation
from app.services.listings import load_listings
from app.services.ranking import rank_listings


router = APIRouter(prefix="/api")

SUPPORTED_TAGS = {
    "quiet": ["quiet", "peaceful"],
    "near_subway": ["subway", "train"],
    "near_path": ["path"],
    "pet_friendly": ["pet", "pet friendly"],
}


@router.post("/search")
def search_apartments(payload: dict) -> dict:
    session_id = payload.get("session_id") or str(uuid4())
    query = payload.get("query", "")

    if not query or not query.strip():
        return {
            "session_id": session_id,
            "preferences": {},
            "results": [],
        }

    preferences = parse_query(query)
    listings = load_listings()
    ranked_listings = rank_listings(preferences, listings)

    results = []
    for listing in ranked_listings[:5]:
        results.append(
            {
                **listing,
                "explanation": generate_explanation(preferences, listing),
            }
        )

    return {
        "session_id": session_id,
        "preferences": preferences,
        "results": results,
    }


def parse_query(query: str) -> dict:
    query = query.lower()

    return {
        "max_price": extract_max_price(query),
        "bedrooms": extract_bedrooms(query),
        "tags": extract_tags(query),
    }


def extract_max_price(query: str) -> int | None:
    dollar_match = re.search(r"\$\s*(\d{3,6})", query)
    if dollar_match:
        return int(dollar_match.group(1))

    number_match = re.search(r"\b\d{3,6}\b", query)
    if number_match:
        return int(number_match.group(0))

    return None


def extract_bedrooms(query: str) -> int | None:
    bedroom_match = re.search(r"\b(\d+)\s*(?:bedroom|bedrooms|br)\b", query)
    if bedroom_match:
        return int(bedroom_match.group(1))

    return None


def extract_tags(query: str) -> list[str]:
    tags = []

    for tag, keywords in SUPPORTED_TAGS.items():
        if any(keyword in query for keyword in keywords):
            tags.append(tag)

    return tags
