from datetime import datetime
from datetime import timezone
from datetime import timedelta
import json


def default(obj):
    if isinstance(obj, datetime):
        return {"_isoformat": obj.isoformat()}
    raise TypeError("...")


def object_hook(obj):
    _isoformat = obj.get("_isoformat")
    if _isoformat is not None:
        return datetime.fromisoformat(_isoformat)
    return obj


def write_json_file(filename, data):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, default=default)


def load_json_file(filename):
    with open(filename, "r") as json_file:
        return json.load(json_file, object_hook=object_hook)
