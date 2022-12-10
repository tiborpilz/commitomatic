import click
import sys
import json

from revChatGPT.revChatGPT import Chatbot

def get_config():
    with open("config.json") as f:
        config = json.load(f)
    return config

def get_chatbot(config):
    return Chatbot(config, conversation_id=None)


def get_diff():
    with sys.stdin:
        data = sys.stdin.read()
    return data

def get_chatbot_query(emoji, body, choices, commit_type, commit_scope, diff):
    query = "I will provide you with a git diff. I want you to generate a single commit message, briefly summarizing that diff. The header has to follow convenctional commit style.\n"

    query += "\n"

    query += f"Your commit header should start with ${'an appropriate github emoji' if emoji else ''} a commit type, followed by the scope of the changes in parentheses, followed by a colon, and then a brief description of the changes.\n"
    if commit_type:
        query += f"The type is ${commit_type}.'\n"

    if commit_scope:
        query += f"This scope is ${commit_scope}.'\n"

    # query += "Here is an example header:\n"
    # query += ":sparkles: feat(button): add a new feature\n"
    # query += ":bug: fix(router): fix a bug\n"
    # query += ":recycle: refactor(reducer): refactor the reducer\n\n"

    if body:
        query += "Summarize the most important changes in the commit body.\nYou don't need to include every change.\nThe body should not be longer than 6 lines."
    else:
        query += "Don't append a body, use only the commit header.\n"

    query += "Do not answer with anything but the generated commit message, and output your response in code fences.\n"

    query += "this is the commit's diff:\n\n"
    query += "```\n"
    query += diff
    query += "```\n"


    query += "\n"
    if choices > 1:
        query += "Give me ${CHOICES} different messages to choose from"
        if body:
            query += ", each with a commit body"
        query += " .Seperate the choices using three dashes: '---'\n"
    return query

def get_chatbot_response(chatbot, query):
    response_obj = chatbot.get_chat_response(query)
    return response_obj["message"]

@click.command()
@click.option('--emoji',
             default=True,
             help="Whether to add Github-Style Emoji",
              type=bool,
              show_default=True)
@click.option('--body',
             default=True,
             help="Whether to add a commit body",
              type=bool,
              show_default=True)
@click.option('--choices',
             default=1,
             help="The number of choices to return",
              type=int,
              show_default=True)
@click.option('--commit-type',
              default=None,
              help="The commit type (fix, feat, refactor). If empty, it will be inferred",
              type=str)
@click.option('--commit-scope',
              default=None,
              help="The commit scope. If empty, it will be inferred",
              type=str)
@click.option('--dry-run', '-d',
              is_flag=True,
              help="Whether to print the query and exit")
def main(emoji, body, choices, commit_type, commit_scope, dry_run):
    config = get_config()
    diff = get_diff()
    query = get_chatbot_query(emoji, body, choices, commit_type, commit_scope, diff)
    if dry_run:
        print(query)
        return
    chatbot = get_chatbot(config)
    response = get_chatbot_response(chatbot, query)
    print(response)

if __name__ == "__main__":
    main()
