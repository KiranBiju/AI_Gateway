import hashlib
import json


def generate_cache_key(data: dict):
    raw = json.dumps(data, sort_keys=True)
    return "cache:" + hashlib.sha256(raw.encode()).hexdigest()