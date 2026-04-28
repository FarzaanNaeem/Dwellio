def generate_explanation(preferences: dict, listing: dict) -> dict:
    strengths = []
    tradeoffs = []
    max_price = preferences.get("max_price")
    bedrooms = preferences.get("bedrooms")

    if max_price is not None:
        if listing.get("price", 0) <= max_price:
            strengths.append("fits your budget")
        else:
            tradeoffs.append("above your budget")

    if bedrooms is not None:
        if listing.get("bedrooms") == bedrooms:
            strengths.append("matches your bedroom preference")
        else:
            tradeoffs.append("bedroom count is not an exact match")

    if strengths:
        summary = "This listing " + " and ".join(strengths) + "."
    else:
        summary = "This listing has tradeoffs against your main preferences."

    return {
        "summary": summary,
        "tradeoffs": tradeoffs,
    }
