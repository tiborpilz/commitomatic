import json
import typer
from typing import Optional
from pathlib import Path
from rich.padding import Padding
from rich.markdown import Markdown
from rich import print
import pyperclip

from .git import Repository
from .query import get_chatbot_query

from revChatGPT.revChatGPT import Chatbot
from pyfzf.pyfzf import FzfPrompt


def get_config():
    with open("config.json") as f:
        config = json.load(f)
    return config


def get_chatbot(config):
    return Chatbot(config, conversation_id=None)


def get_chatbot_response(chatbot, query):
    response_obj = chatbot.get_chat_response(query)
    return response_obj["message"]


def app(
    repo_path: Optional[Path] = typer.Argument(
        None,
        help="Path to the git repository",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    emoji: bool = typer.Option(True, help="Whether to add Github-Style Emoji"),
    body: bool = typer.Option(True, help="Whether to add a commit body"),
    choices: int = typer.Option(1, help="The number of choices to return"),
    commit_type: str = typer.Option(None, help="The commit type. If empty, it will be inferred"),
    commit_scope: str = typer.Option(None, help="The commit scope. If empty, it will be inferred"),
    dry_run: bool = typer.Option(False, help="Whether to print the query and exit", is_flag=True),
    pick_files: bool = typer.Option(False, help="Whether to pick the files interactively", is_flag=True),
):
    config = get_config()

    repo_path = repo_path or Path.cwd()

    repository = Repository(repo_path)
    if pick_files:
        files = repository.get_diff_files()
        fzf = FzfPrompt()
        fzf_options = (
            "--multi"
            " --cycle"
            " --info=hidden"
            " --margin='5%'"
            " --disabled"
            " --ansi"
            " --preview='git -c color.diff=always diff --staged -- {}'")
        filtered_files = fzf.prompt(
            files,
            fzf_options,
        )
        repository.set_files(filtered_files)
    diff = repository.get_diff()

    skip_query = dry_run or (diff is None)

    query = get_chatbot_query(emoji, body, choices, commit_type, commit_scope)
    prompt = query + (diff if diff is not None else "")

    if skip_query:
        info = Markdown("## Prompt\n\n" + prompt[0:1000] + "...")
        print(Padding(info, (2, 4)))
        pyperclip.copy(prompt)
        return

    chatbot = get_chatbot(config)
    response = get_chatbot_response(chatbot, prompt)
    # buffer = response + "\n" + repository.get_message_footer() TODO: Use buffer when fixed
    commit_message = typer.edit(response, require_save=True)

    if commit_message is not None:
        repository.git.commit(f"-m{commit_message}")


def main():
    typer.run(app)
