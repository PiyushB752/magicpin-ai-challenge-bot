from fastapi import FastAPI
from pydantic import BaseModel
from engine import score_trigger,best_trigger
from services.reply_service import generate_reply
from services.recommendation_engine import build_recommendation
from store import (
    initialize_store,
    category_store,
    merchant_store,
    customer_store,
    trigger_store,
    merchant_customers,
    merchant_triggers,
    store_context,
    get_context
)

app=FastAPI(
    title="Magicpin AI Challenge Bot",
    version="1.0.0"
)

class ContextRequest(BaseModel):
    entity_type:str
    entity_id:str
    version:int
    payload:dict

class TickRequest(BaseModel):
    merchant_id:str

class ReplyRequest(BaseModel):
    merchant_id:str
    message:str

@app.on_event("startup")
def startup():
    initialize_store()
    print("Merchants:",len(merchant_store))
    print("Customers:",len(customer_store))
    print("Triggers:",len(trigger_store))

@app.get("/")
def root():
    return {
        "message":"Magicpin AI Challenge Bot"
    }

@app.get("/v1/healthz")
def healthz():
    return {
        "status":"ok"
    }

@app.get("/v1/metadata")
def metadata():
    return {
        "service":"magicpin-ai-challenge-bot",
        "version":"1.0.0",
        "categories":sorted(list(category_store.keys())),
        "counts":{
            "categories":len(category_store),
            "merchants":len(merchant_store),
            "customers":len(customer_store),
            "triggers":len(trigger_store)
        }
    }

@app.get("/v1/merchant/{merchant_id}")
def get_merchant(merchant_id:str):
    merchant=merchant_store.get(merchant_id)

    if merchant is None:
        return {
            "error":"merchant_not_found"
        }

    return merchant

@app.get("/v1/customer/{customer_id}")
def get_customer(customer_id:str):
    customer=customer_store.get(customer_id)

    if customer is None:
        return {
            "error":"customer_not_found"
        }

    return customer

@app.get("/v1/trigger/{trigger_id}")
def get_trigger(trigger_id:str):
    trigger=trigger_store.get(trigger_id)

    if trigger is None:
        return {
            "error":"trigger_not_found"
        }

    return trigger

@app.get("/v1/merchant/{merchant_id}/customers")
def merchant_customers_endpoint(merchant_id:str):
    customers=merchant_customers(merchant_id)

    return {
        "merchant_id":merchant_id,
        "count":len(customers),
        "customers":customers
    }

@app.get("/v1/merchant/{merchant_id}/triggers")
def merchant_triggers_endpoint(merchant_id:str):
    triggers=merchant_triggers(merchant_id)

    return {
        "merchant_id":merchant_id,
        "count":len(triggers),
        "triggers":triggers
    }

@app.post("/v1/context")
def save_context(req:ContextRequest):
    return store_context(
        req.entity_type,
        req.entity_id,
        req.version,
        req.payload
    )

@app.get("/v1/context/{entity_type}/{entity_id}")
def read_context(entity_type:str,entity_id:str):
    data=get_context(entity_type,entity_id)

    if data is None:
        return {
            "found":False
        }

    return {
        "found":True,
        "context":data
    }

@app.post("/v1/tick")
def tick(req:TickRequest):
    merchant=merchant_store.get(req.merchant_id)

    if merchant is None:
        return {
            "error":"merchant_not_found"
        }

    triggers=merchant_triggers(req.merchant_id)
    trigger=best_trigger(triggers)

    if trigger is None:
        return {
            "merchant_id":req.merchant_id,
            "recommendation":None
        }

    recommendation=build_recommendation(trigger)

    return {
        "merchant_id":req.merchant_id,
        "score":score_trigger(trigger),
        "trigger":trigger,
        "recommendation":recommendation
    }

@app.post("/v1/reply")
def reply(req:ReplyRequest):
    merchant=merchant_store.get(req.merchant_id)

    if merchant is None:
        return {
            "error":"merchant_not_found"
        }

    response=generate_reply(req.message)

    return {
        "merchant_id":req.merchant_id,
        "message":req.message,
        "response":response
    }