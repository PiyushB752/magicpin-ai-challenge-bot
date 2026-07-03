def score_trigger(trigger):
    score=trigger["urgency"]*10

    bonuses={
        "supply_alert":50,
        "renewal_due":45,
        "perf_dip":40,
        "active_planning_intent":35,
        "review_theme_emerged":25,
        "trial_followup":20,
        "festival_upcoming":15,
        "research_digest":10
    }

    score+=bonuses.get(
        trigger["kind"],
        0
    )

    return score


def best_trigger(triggers):
    if not triggers:
        return None

    return max(
        triggers,
        key=score_trigger
    )