def compose_research_digest(trigger):
    payload = trigger["payload"]
    category = payload["category"]
    item = payload["top_item_id"]
    return (
        f"New {category} research available: "
        f"{item}"
    )