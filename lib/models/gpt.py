from typing import Literal, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator, validator
from datetime import datetime, timedelta
from typing_extensions import Annotated


def check_valid_date(v: str):
    if not v:
        return v
    datetime.strptime(v, "%Y-%m-%d")


DateString = Annotated[str, check_valid_date]


class UserQuery(BaseModel):
    """
    This is a simple class which encapsulates all of the necessary information to execute a simple query to answer the user's question.
    """

    start: Optional[DateString] = Field(
        description="This is the earliest date that the user would like to see. In the event that no start date is specified, simply return null",
        default=None,
    )

    end: Optional[DateString] = Field(
        description="This is the latest date that the user would like to see. In the event that no end date is specified, simply return null",
        default=None,
    )

    completed: Optional[Union[Literal["y"], Literal["n"]]] = Field(
        description="If the user has specified he only wants to see completed tasks, this should be a 'n'. If the user woud like to see unfinished tasks, this should be a 'y'. If the user has not specified whether he wants unfinished or finished tasks, this should be Null",
        default=None,
    )

    @model_validator(mode="after")
    def validate_start_and_end_date(self) -> "UserQuery":
        # Validate that start and end date, if they exist are not the same
        if self.start and self.end:
            if self.start == self.end:
                raise ValueError(
                    "Start and End cannot be the same date. There must be at least one day in between them"
                )

            start = datetime.strptime(self.start, "%Y-%m-%d")
            end = datetime.strptime(self.end, "%Y-%m-%d")
            if start > end:
                raise ValueError("Start date must be before end date.")

        return self


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

    @field_validator("due_date")
    def parse_date(cls, v):
        if isinstance(v, str):
            # We try to format the date time object if it fails
            datetime.strptime(v, "%Y-%m-%d")
        return v
