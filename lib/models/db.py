from pydantic import BaseModel, Field


class AddTodoResponse(BaseModel):
    todoId: int
    title: str
    description: str
    context: str
    due_date: str
    completed: bool = Field(..., converter=bool)
