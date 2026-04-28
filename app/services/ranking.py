def rank_listings(preferences: dict, listings: list[dict]) -> list[dict]:
    ranked = []

    for listing in listings:
        score = 0
        max_price = preferences.get("max_price")
        bedrooms = preferences.get("bedrooms")

        if max_price is not None and listing.get("price", 0) <= max_price:
            score += 40

        if bedrooms is not None and listing.get("bedrooms") == bedrooms:
            score += 30

        preferred_tags = set(preferences.get("tags", []))
        listing_tags = set(listing.get("tags", []))
        if preferred_tags:
            score += int((len(preferred_tags & listing_tags) / len(preferred_tags)) * 30)

        ranked.append({**listing, "score": score})

    return sorted(
        ranked,
        key=lambda listing: (-listing["score"], listing.get("price", 0), listing.get("id", "")),
    )
