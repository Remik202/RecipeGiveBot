import json

SUBSCRIPTION_PRICE = 500
STATS_FILE = "subscription_stats.json"


def load_stats():
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"total_subscriptions": 0, "total_revenue": 0}


def save_stats(stats: dict):
    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4, ensure_ascii=False)


def add_subscription():
    stats = load_stats()
    stats["total_subscriptions"] += 1
    stats["total_revenue"] = stats["total_subscriptions"] * SUBSCRIPTION_PRICE
    save_stats(stats)


def get_total_subscriptions():
    stats = load_stats()
    return stats["total_subscriptions"]


def get_total_revenue():
    stats = load_stats()
    return stats["total_revenue"]