import os
import requests
from lib.models.db import AddTodoResponse

from lib.models.gpt import Actionable


def insert_logging(input, output, tag):
    url = f"{os.environ['DB_URL']}/add-log"
    print(url)

    insert_request = requests.post(
        url,
        json={"input": input, "output": output, "tag": tag},
        headers={"Content-Type": "application/json"},
    )

    assert insert_request.status_code == 200


def insert_todo(actionable: Actionable):
    url = f"{os.environ['DB_URL']}/add"
    print(url)

    insert_request = requests.post(
        url,
        json={
            "title": actionable.title,
            "description": actionable.description,
            "context": actionable.context,
            "due_date": actionable.due_date,
        },
        headers={"Content-Type": "application/json"},
    )

    resp = insert_request.json()

    return AddTodoResponse.model_validate(resp)


def delete_todo(id: str):
    url = f"{os.environ['DB_URL']}/delete?id={id}"
    print(url)

    delete = requests.get(url)

    assert (
        delete.status_code == 200
    ), f"API Request failed with status of {delete.status_code}"

    return
