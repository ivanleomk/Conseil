from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta


class Actionable(BaseModel):
    """
    This is a single instance of an Actionable. An Actionable represents a concrete task that has a title, description and some context.

    For instance
    eg. Remind me to buy some eggs and bread sometime soon. I'd say I need to do it next week latest
    -> title: Buy Groceries, description: Buy eggs and toast at the supermarket, context: You set a reminder to buy some eggs and toast by next week latest some time ago
    """

    title: str = Field(
        ...,
        description="This is a unique title for the Actionable which can help to identify it",
    )
    description: str = Field(
        ...,
        description="This is a short description of the task and some things to take note of",
    )
    context: str = Field(
        ...,
        description="This is some additional context about the task which was provided in the original message.",
    )
    due_date: str = Field(
        default_factory=lambda: (datetime.now() + timedelta(days=7)).strftime(
            "%Y-%m-%d"
        ),
        description="This is the due date of the actionable. If no due date is present, this should be omitted. This is a date string in the format YYYY-MM-DD (Eg.2032-04-23)",
    )

    @validator("due_date", pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            # We try to format the date time object if it fails
            datetime.strptime(v, "%Y-%m-%d")
        return v
