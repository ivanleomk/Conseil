from models.gpt import Actionable
from pydantic_helpers import serialize_items
import json


class TestSerialization:
    def test_list_serialization(self):
        valid_data = {
            "title": "Buy Groceries",
            "description": "Buy eggs and toast at the supermarket",
            "context": "You set a reminder to buy some eggs and toast by next week latest some time ago",
        }
        actionable = Actionable(**valid_data)
        actionable_list = [actionable]
        serialized_items = serialize_items(actionable_list)
        items = json.loads(serialized_items)
        parsed_items = [Actionable.model_validate(json.loads(item)) for item in items]
        assert parsed_items == actionable_list
