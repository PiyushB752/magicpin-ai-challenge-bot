def generate_reply(message):
    msg=message.lower()
    if "renew" in msg:
        return (
            "I can assist with renewing your plan."
        )

    if "campaign" in msg:
        return (
            "I can suggest campaign ideas."
        )

    if "offer" in msg:
        return (
            "Let's create a promotional offer."
        )

    if "review" in msg:
        return (
            "I'll summarize customer feedback."
        )

    if "customer" in msg:
        return (
            "I can identify high-value customers."
        )

    return (
        "How can Vera help your business today?"
    )