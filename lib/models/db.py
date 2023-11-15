from pydantic import BaseModel, Field


class TodoItem(BaseModel):
    todoId: int
    title: str
    description: str
    context: str
    due_date: str
    completed: bool = Field(..., json_schema_extra={"converter": bool})
