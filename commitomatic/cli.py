import sys
import json
import typer
from rich.progress import track
from rich.padding import Padding
from rich.markdown import Markdown
from rich import print
from time import sleep
import pyperclip

from revChatGPT.revChatGPT import Chatbot

def get_config():
    with open("config.json") as f:
        config = json.load(f)
    return config

def get_chatbot(config):
    return Chatbot(config, conversation_id=None)


def get_diff():
    if sys.stdin.isatty():
        # TODO: Execute git diff
        return ""
    else:
        with sys.stdin:
            data = sys.stdin.read()
        return data

def get_chatbot_query(emoji, body, choices, commit_type, commit_scope):
    query = "I will provide you with a git diff. I want you to generate a single commit message, briefly summarizing that diff. The header has to follow convenctional commit style.\n"
    query += "\n"
    query += f"Your commit header should start with ${'an appropriate github emoji' if emoji else ''} a commit type, followed by the scope of the changes in parentheses, followed by a colon, and then a brief description of the changes.\n"
    if commit_type:
        query += f"The type is ${commit_type}.'\n"
    if commit_scope:
        query += f"This scope is ${commit_scope}.'\n"
    if body:
        query += "Summarize the most important changes in the commit body.\nYou don't need to include every change.\nThe body should not be longer than 6 lines."
    else:
        query += "Don't append a body, use only the commit header.\n"

    query += "Do not answer with anything but the generated commit message, and output your response in code fences.\n"

    query += "\n"
    if choices > 1:
        query += "Give me ${CHOICES} different messages to choose from"
        if body:
            query += ", each with a commit body"
        query += " .Seperate the choices using three dashes: '---'\n"

    query += "this is the commit's diff:\n\n"
    return query

def get_chatbot_response(chatbot, query):
    response_obj = chatbot.get_chat_response(query)
    return response_obj["message"]

def app(
    emoji: bool = typer.Option(True, help="Whether to add Github-Style Emoji"),
    body: bool = typer.Option(True, help="Whether to add a commit body"),
    choices: int = typer.Option(1, help="The number of choices to return"),
    commit_type: str = typer.Option(None, help="The commit type. If empty, it will be inferred"),
    commit_scope: str = typer.Option(None, help="The commit scope. If empty, it will be inferred"),
    dry_run: bool = typer.Option(False, help="Whether to print the query and exit", is_flag=True),
):
    config = get_config()
    diff = get_diff()

    skip_query = dry_run or (diff is None)

    query = get_chatbot_query(emoji, body, choices, commit_type, commit_scope)
    prompt = query + (diff if diff is not None else "")

    print(Padding(Markdown(prompt), (2, 4)))
    if skip_query:
        # query_output = "## Query\n\n" + query + "## Diff\n\n" + (diff[0:1000] + "..." if len(prompt) > 1000 else prompt)
        pyperclip.copy(prompt)
        return

    chatbot = get_chatbot(config)
    response = get_chatbot_response(chatbot, prompt)
    total = 0
    for _ in track(range(100), description="Generating commit messages..."):
        sleep(0.01)
        total += 1

    print(response)

def main():
    typer.run(app)
