from store import trigger_store

from composers.research_digest import compose_research_digest
from composers.recall_due import compose_recall_due
from composers.generic import compose_generic


def handle_tick(trigger_id):
    trigger = trigger_store.get(trigger_id)
    if not trigger:
        return {
            "accepted": False,
            "reason": "trigger_not_found"
        }
    kind = trigger["kind"]

    if kind == "research_digest":
        message = compose_research_digest(trigger)
    elif kind == "recall_due":
        message = compose_recall_due(trigger)
    else:
        message = compose_generic(trigger)

    return {
        "accepted": True,
        "trigger_id": trigger_id,
        "kind": kind,
        "message": message
    }