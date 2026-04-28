from fastapi import APIRouter, HTTPException

from app.services.listings import load_listings


router = APIRouter(prefix="/api")

LISTINGS = load_listings()
LISTING_BY_ID = {listing["id"]: listing for listing in LISTINGS}

feedback_store = {}
preference_store = {}


@router.post("/feedback")
def submit_feedback(payload: dict) -> dict:
    session_id = payload.get("session_id")
    listing_id = payload.get("listing_id")
    action = payload.get("action")

    if not session_id or not listing_id:
        raise HTTPException(status_code=400, detail="session_id and listing_id are required")

    if action not in {"like", "dislike"}:
        raise HTTPException(status_code=400, detail="action must be 'like' or 'dislike'")

    if listing_id not in LISTING_BY_ID:
        raise HTTPException(status_code=400, detail="listing_id does not exist")

    feedback = feedback_store.setdefault(
        session_id,
        {
            "liked": set(),
            "disliked": set(),
        },
    )
    preferences = preference_store.setdefault(session_id, {"tags": set()})

    if action == "like":
        feedback["liked"].add(listing_id)
        feedback["disliked"].discard(listing_id)

    if action == "dislike":
        feedback["disliked"].add(listing_id)
        feedback["liked"].discard(listing_id)

    update_preferences_from_feedback(preferences, feedback)

    return {
        "status": "ok",
        "session_id": session_id,
        "feedback": {
            "liked": sorted(feedback["liked"]),
            "disliked": sorted(feedback["disliked"]),
        },
    }


def update_preferences_from_feedback(preferences: dict, feedback: dict) -> dict:
    tags = set()

    for listing_id in feedback["liked"]:
        tags.update(LISTING_BY_ID[listing_id]["tags"])

    preferences["tags"] = tags
    return preferences
