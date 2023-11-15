from typing import List
from pydantic import BaseModel
import json


def serialize_items(x: List[BaseModel]):
    return json.dumps([i.model_dump_json() for i in x])
