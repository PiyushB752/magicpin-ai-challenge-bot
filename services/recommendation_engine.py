def build_recommendation(trigger):
    kind=trigger["kind"]
    payload=trigger["payload"]
    if kind=="renewal_due":
        return {
            "title":"Subscription Renewal",
            "priority":"high",
            "action":"renew",
            "message":
            f"Subscription expires in {payload['days_remaining']} days."
        }
    elif kind=="perf_dip":
        return {
            "title":"Performance Recovery",
            "priority":"high",
            "action":"visibility_boost",
            "message":
            "Views and calls are declining."
        }
    elif kind=="active_planning_intent":
        return {
            "title":"Planning Opportunity",
            "priority":"high",
            "action":"campaign_creation",
            "message":
            "Merchant is actively seeking guidance."
        }
    elif kind=="review_theme_emerged":
        return {
            "title":"Customer Sentiment",
            "priority":"medium",
            "action":"review_response",
            "message":
            "Negative reviews are increasing."
        }
    elif kind=="supply_alert":
        return {
            "title":"Compliance Alert",
            "priority":"critical",
            "action":"customer_notification",
            "message":
            "Immediate attention required."
        }
    return {
        "title":"Opportunity",
        "priority":"low",
        "action":"engage",
        "message":
        "Suggested next step available."
    }