from db import TodoItem


def test_AddTodoResponse():
    # Create an instance of the model
    obj = {
        "todoId": 1,
        "title": "Test",
        "description": "Test description",
        "context": "Test context",
        "due_date": "2022-12-31",
        "completed": 0,
    }

    parsed_obj = TodoItem.model_validate(obj)
    # Validate that Type Coercion is working nicely
    assert parsed_obj.completed is False
