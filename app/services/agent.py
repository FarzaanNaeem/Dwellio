import asyncio

from app.api.events import publish_event
from app.api.feedback import preference_store
from app.services.listings import load_listings
from app.services.ranking import rank_listings


LISTINGS = load_listings()

best_seen = {}


async def run_agent() -> None:
    await asyncio.sleep(2)

    while True:
        await asyncio.sleep(10)

        for session_id, prefs in preference_store.items():
            tags = list(prefs.get("tags", set()))
            if not tags:
                continue

            preferences = {"tags": tags}

            ranked = rank_listings(preferences, LISTINGS)
            if not ranked:
                continue

            top = ranked[0]
            prev = best_seen.get(session_id)

            if not prev or (
                top["score"] > prev["score"]
                or (top["score"] == prev["score"] and top["id"] != prev["listing_id"])
            ):
                best_seen[session_id] = {
                    "score": top["score"],
                    "listing_id": top["id"],
                }

                publish_event(
                    session_id,
                    {
                        "type": "better_listing",
                        "listing": top,
                        "score": top["score"],
                    },
                )
