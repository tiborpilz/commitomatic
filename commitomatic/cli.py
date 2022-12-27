import json
import os
import typer
from typing import Optional, Dict
from pathlib import Path
from rich.padding import Padding
from rich.markdown import Markdown
from rich import print
import pyperclip
import openai
from pyfzf.pyfzf import FzfPrompt

from .git import Repository
from .query import get_gpt_codex_prompt


def get_config() -> Dict:
    """Load config from file."""
    with open("config.json") as f:
        config = json.load(f)
    return config


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
    body: bool = typer.Option(True, help="Whether to add a commit body"),
    choices: int = typer.Option(1, help="The number of choices to return"),
    commit_type: str = typer.Option(None, help="The commit type. If empty, it will be inferred"),
    dry_run: bool = typer.Option(False, help="Whether to print the query and exit", is_flag=True),
    pick_files: bool = typer.Option(False, help="Whether to pick the files interactively", is_flag=True),
):
    """Generate commit messages from GPT-2 with openai.com"""
    openai.api_key = os.getenv("OPENAI_API_KEY")

    repo_path = repo_path or Path.cwd()
    repository = Repository(repo_path)

    if pick_files:
        pick_files(repository)
    else:
        repository.set_files(repository.get_diff_files())

    repository.filter_files_by_changed_lines()

    diff = repository.get_diff()
    prompt = get_gpt_codex_prompt(diff, commit_type)

    if dry_run or (diff is None):
        info = Markdown("## Prompt\n\n" + prompt + "...")
        print(Padding(info, (2, 4)))
        pyperclip.copy(prompt)
        return

    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        temperature=0.1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.6,
        presence_penalty=0.2,
        n=choices,
        suffix="\nEOF",
    )

    header = [line for line in response["choices"][0]["text"].split("\n")
              if line.strip() != ""][0]

    body_prompt = get_gpt_codex_prompt(diff, header=header)
    body_response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=body_prompt,
        temperature=0.1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.6,
        presence_penalty=0.2,
        n=choices,
        suffix="\nEOF",
    )

    body = body_response["choices"][0]["text"]

    commit_message = typer.edit(f"{header}\n{body}", require_save=True)

    if commit_message is not None:
        repository.git.commit(f"-m{commit_message}")


def pick_files(repository: Repository):
    """Prompt for files to use for the commit message."""
    files = repository.get_diff_files()
    fzf = FzfPrompt()
    preview_command = (
        "git -c color.diff=always diff" +
        (" --staged" if repository.use_staged else "") +
        " -- {}"
    )
    fzf_options = (
        "--multi"
        " --cycle"
        " --info=hidden"
        " --margin='5%'"
        " --disabled"
        " --ansi"
        f" --preview='{preview_command}'"
        " --bind='start:last+select-all'"
    )
    filtered_files = fzf.prompt(
        files,
        fzf_options,
    )
    repository.set_files(filtered_files)


def main():
    """Run the CLI."""
    typer.run(app)
