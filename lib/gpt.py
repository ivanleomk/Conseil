from instructor import patch, MultiTask
from openai import OpenAI
from datetime import datetime
from lib.db import insert_logging
from lib.models.gpt import Actionable, UserQuery
import os
from typing import List

from lib.pydantic_helpers import serialize_items


def parse_user_message(text: str) -> UserQuery:
    client = patch(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
    completion: UserQuery = client.chat.completions.create(
        model="gpt-4-0613",
        temperature=0.2,
        response_model=UserQuery,
        max_retries=3,
        messages=[
            {
                "role": "system",
                "content": "You are a perfect entity which excels at extracting user queries from simple sentences or descriptions.",
            },
            {
                "role": "assistant",
                "content": "You are about to be presented with a request from a user, make sure to only extract what is specified in the response format in valid json",
            },
            {
                "role": "assistant",
                "content": f"Here is some useful information for you.\n-The date today is {datetime.now().strftime('%Y-%m-%d')} and is a {datetime.now().strftime('%A')}",
            },
            {
                "role": "user",
                "content": f"Could you help me to generate a UserQuery object that adheres to this request: {text}",
            },
        ],
    )

    insert_logging(text, completion.model_dump_json(), "user_todos_query")

    return completion


def generate_actionables(text: str):
    client = patch(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
    MultiActionable = MultiTask(Actionable)

    completion = client.chat.completions.create(
        model="gpt-4-0613",
        temperature=0.2,
        stream=False,
        response_model=MultiActionable,
        messages=[
            {
                "role": "system",
                "content": "You are a perfect actionable extraction system who is able to identify a handful of actionables when presented with a request from a user. Only extract the actionables from the data.",
            },
            {
                "role": "assistant",
                "content": f"Here is some useful information for you.\n-The date today is {datetime.now().strftime('%Y-%m-%d')} and is a {datetime.now().strftime('%A')}",
            },
            {
                "role": "assistant",
                "content": "Remember that if there is no due date specified for a task, you should set the due date for one week from today.",
            },
            {
                "role": "assistant",
                "content": "Correctly segment it into Actionables. Make sure the JSON is correct and to adhere to the requested format.",
            },
            {
                "role": "user",
                "content": f"Consider the data below: \n {text}.",
            },
        ],
        max_tokens=1000,
        max_retries=3,
    )

    actionables: List[Actionable] = [i for i in completion][0][1]

    if actionables:
        actionables_string = serialize_items(actionables)
        insert_logging(text, actionables_string, "actionables")

    return actionables
