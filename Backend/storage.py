import json
from pathlib import Path

# Store lists in a JSON file (change for a DB)
DATA_FILE = Path(__file__).parent / "storage.json"

# Default structure if no file exists
_default_data = {"whitelist": [], "blacklist": []}

def _load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return _default_data.copy()

def _save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

#Public wrapper para save data()
def save_data():
    """Saves current lists to file (used by control.py)"""
    _save_data({"whitelist": get_whitelist(), "blacklist": get_blacklist()})

# Public API
def get_whitelist():
    return _load_data()["whitelist"]

def get_blacklist():
    return _load_data()["blacklist"]

def add_to_whitelist(domain: str):
    data = _load_data()
    if domain not in data["whitelist"]:
        data["whitelist"].append(domain)
        _save_data(data)

def add_to_blacklist(domain: str):
    data = _load_data()
    if domain not in data["blacklist"]:
        data["blacklist"].append(domain)
        _save_data(data)
