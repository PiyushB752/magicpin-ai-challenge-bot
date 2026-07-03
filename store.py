import json
from pathlib import Path
from datetime import datetime,UTC

BASE_DIR=Path(__file__).parent
DATASET_DIR=BASE_DIR/"dataset"
CATEGORY_DIR=DATASET_DIR/"categories"

category_store={}
merchant_store={}
customer_store={}
trigger_store={}
conversation_store={}

def load_json(path):
    with open(path,"r",encoding="utf-8") as f:
        return json.load(f)

def load_categories():
    for file in CATEGORY_DIR.glob("*.json"):
        category_store[file.stem]=load_json(file)

def load_merchants():
    data=load_json(
        DATASET_DIR/"merchants_seed.json"
    )

    for merchant in data["merchants"]:
        merchant_store[
            merchant["merchant_id"]
        ]=merchant

def load_customers():
    data=load_json(
        DATASET_DIR/"customers_seed.json"
    )

    for customer in data["customers"]:
        customer_store[
            customer["customer_id"]
        ]=customer

def load_triggers():
    data=load_json(
        DATASET_DIR/"triggers_seed.json"
    )

    for trigger in data["triggers"]:
        trigger_store[
            trigger["id"]
        ]=trigger

def initialize_store():
    load_categories()
    load_merchants()
    load_customers()
    load_triggers()

def merchant_triggers(merchant_id):
    return [
        trigger
        for trigger in trigger_store.values()
        if trigger["merchant_id"]==merchant_id
    ]

def merchant_customers(merchant_id):
    return [
        customer
        for customer in customer_store.values()
        if customer["merchant_id"]==merchant_id
    ]

def store_context(
        entity_type,
        entity_id,
        version,
        payload
):
    allowed = {
        "merchant",
        "customer",
        "category",
        "trigger"
    }

    if entity_type not in allowed:
        return {
            "accepted": False,
            "reason": "unsupported_entity_type"
        }

    key = f"{entity_type}:{entity_id}"
    existing = conversation_store.get(key)
    if existing:
        current_version = existing["version"]
        if version <= current_version:
            return {
                "accepted": False,
                "reason": "stale_version",
                "current_version": current_version
            }
    stored_at = datetime.now(UTC).isoformat()
    ack_id = (
        f"ack_"
        f"{entity_type}_"
        f"{entity_id}_"
        f"v{version}"
    )

    conversation_store[key] = {
        "version": version,
        "payload": payload,
        "stored_at": stored_at
    }

    return {
        "accepted": True,
        "ack_id": ack_id,
        "stored_at": stored_at
    }

def get_context(entity_type,entity_id):
    key=f"{entity_type}:{entity_id}"
    return conversation_store.get(key)