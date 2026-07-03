from store import customer_store

def compose_recall_due(trigger):
    customer_id = trigger["customer_id"]
    customer = customer_store.get(customer_id)
    payload = trigger["payload"]
    due = payload["service_due"]
    name = customer["identity"]["name"]
    return (
        f"{name} is due for "
        f"{due.replace('_', ' ')}."
    )