import os
import requests
from lib.models.db import TodoItem

from lib.models.gpt import Actionable, UserQuery


def get_filtered_tasks(query: UserQuery):
    url = f"{os.environ['DB_URL']}/get-all"

    if query.completed:
        url += f"?completed={query.completed}"

    if query.start:
        url = (
            f"{url}&start={query.start}" if "?" in url else f"{url}?start={query.start}"
        )

    if query.end:
        url = f"{url}&end={query.end}" if "?" in url else f"{url}?end={query.end}"
    print(f"Making url request to {url}")
    get_request = requests.get(
        url,
    )
    # We then parse everything
    data = get_request.json()
    parsed_items = [TodoItem(**i) for i in data]

    return parsed_items


def get_all_tasks():
    url = f"{os.environ['DB_URL']}/get-all?completed=n"
    get_request = requests.get(
        url,
    )
    # We then parse everything
    data = get_request.json()

    # It will be a list of todos
    parsed_items = [TodoItem(**i) for i in data]

    return parsed_items


def insert_logging(input, output, tag):
    url = f"{os.environ['DB_URL']}/add-log"

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

    return TodoItem.model_validate(resp)


def delete_todo(id: str):
    url = f"{os.environ['DB_URL']}/delete?id={id}"
    print(url)

    delete = requests.post(url)

    assert (
        delete.status_code == 200
    ), f"API Request failed with status of {delete.status_code}"

    return
