from pathlib import Path
import pytest
from git import Repo, cmd
from commitomatic.git import Repository

def read_message():
    with open("tests/fixtures/message.txt", "r") as f:
        return f.read()

def read_diff(name=None):
    filename = f"diff_{name}.txt" if name else "diff.txt"
    with open(f"tests/fixtures/{filename}", "r") as f:
        return f.read()

def mock_execute(self, cmd, **kwargs):
    if cmd[1] == "diff":
        if "--name-only" in cmd:
            return "poetry.lock\npyproject.toml\ncommitomatic/git.py"
        elif "pyproject.toml" in cmd:
            return read_diff("pyproject")
        elif "commitomatic/git.py" in cmd:
            return read_diff("git")
        elif "poetry.lock" in cmd:
            return read_diff("poetry")
        else:
            return read_diff()
    if cmd[1] == "config":
        if cmd[2] == "user.name":
            return "Test User"
        if cmd[2] == "user.email":
            return "test@example.com"

    if cmd[1] == "rev-parse":
        return "test/example-branch"

@pytest.fixture
def repo(mocker):
    mocker.patch.object(cmd.Git, "execute", mock_execute)
    mocker.spy(cmd.Git, "execute")
    repo = Repository(Path("."))
    return repo


def test_get_diff(repo):
    repo = Repository(Path("."))
    repo.get_diff()
    assert cmd.Git.execute.call_count == 1
    assert cmd.Git.execute.call_args[0][1][1] == 'diff'


def test_get_diff_staged(repo):
    repo.enable_flag("--staged")
    repo.get_diff()
    assert "--staged" in cmd.Git.execute.call_args[0][1]


def test_get_diff_no_staged(repo):
    repo.disable_flag("--staged")
    repo.get_diff()
    assert "--staged" not in cmd.Git.execute.call_args[0][1]

def test_get_diff_files(repo):
    files = repo.get_diff_files()
    assert files == ["poetry.lock", "pyproject.toml", "commitomatic/git.py"]


def test_file_lines_changed(repo):
    lines_git = repo.file_lines_changed("commitomatic/git.py")
    assert lines_git == 15
    lines_poetry = repo.file_lines_changed("poetry.lock")
    assert lines_poetry == 295
    lines_pyproject = repo.file_lines_changed("pyproject.toml")
    assert lines_pyproject == 4


def test_filter_files_by_changed_lines(repo):
    repo.files = ["poetry.lock", "pyproject.toml", "commitomatic/git.py"]
    repo.filter_files_by_changed_lines()
    assert repo.files == ["poetry.lock", "pyproject.toml", "commitomatic/git.py"]
    repo.max_lines = 100

    repo.filter_files_by_changed_lines()
    assert repo.files == ["pyproject.toml", "commitomatic/git.py"]

    repo.max_lines = 10
    repo.filter_files_by_changed_lines()
    assert repo.files == ["pyproject.toml"]


def  test_filter_files_initial_change(repo):
    repo.files = ["poetry.lock"]
    repo.max_lines = 100
    repo.filter_files_by_changed_lines()
    assert repo.files == []

def test_get_message_footer(repo):
    message = repo.get_message_footer()
    expected_message = read_message()
    assert message == expected_message
