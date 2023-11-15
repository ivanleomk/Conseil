from datetime import datetime, timedelta
from gpt import Actionable, UserQuery


class TestUserQuery:
    def test_user_query(self):
        empty_payload = {}
        only_completed_field = {"completed": "y"}
        only_start_field = {"start": "2023-10-04"}

        assert UserQuery.model_validate(empty_payload).start is None
        assert UserQuery.model_validate(empty_payload).end is None
        assert UserQuery.model_validate(empty_payload).completed is None

        assert UserQuery.model_validate(only_completed_field).completed == "y"
        assert UserQuery.model_validate(only_completed_field).start is None
        assert UserQuery.model_validate(only_completed_field).end is None

        assert UserQuery.model_validate(only_start_field).completed is None
        assert UserQuery.model_validate(only_start_field).start == "2023-10-04"
        assert UserQuery.model_validate(only_start_field).end is None


class TestActionable:
    def test_actionable(self):
        # Test case with valid data
        expected_date = datetime.now() + timedelta(days=7)
        valid_data = {
            "title": "Buy Groceries",
            "description": "Buy eggs and toast at the supermarket",
            "context": "You set a reminder to buy some eggs and toast by next week latest some time ago",
        }
        actionable = Actionable(**valid_data)
        assert actionable.title == valid_data["title"]
        assert actionable.description == valid_data["description"]
        assert actionable.context == valid_data["context"]
        assert actionable.due_date == expected_date.strftime("%Y-%m-%d")

        # Test case with valid data
        expected_date = datetime.now() + timedelta(days=7)
        valid_data = {
            "title": "Buy Groceries",
            "description": "Buy eggs and toast at the supermarket",
            "context": "You set a reminder to buy some eggs and toast by next week latest some time ago",
            "due_date": "2023-04-05",
        }
        actionable = Actionable(**valid_data)
        assert actionable.title == valid_data["title"]
        assert actionable.description == valid_data["description"]
        assert actionable.context == valid_data["context"]
        assert actionable.due_date == "2023-04-05"
