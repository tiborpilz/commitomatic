# First, get a diff from the repo. For now, just use the
# current working directory.
# Then check whether the interactive option is set.
# If yes, get all files that have been changed and prompt the user with a multiselection,
# Afterwards, create a new diff with only the selected files.

from pathlib import Path
from git import Repo


class Repository():
    repo = Repo(Path.cwd())

    def __init__(self, path: Path, use_staged: bool = True):
        self.diff_target = None
        self.path = path
        # TODO: error handling
        self.repo = Repo(path)
        self.git = self.repo.git
        self.files = []
        self.use_staged = use_staged
        self.flags = []
        self.flags.append("-U0")
        if self.use_staged:
            self.flags.append("--staged")
        self.max_lines = 300

    def get_diff(self, *flags, files=None, **kwargs):
        params = [f"--{key} {value}" for key, value in kwargs.items()]
        if files is not None:
            file_args = ["--", *files]
        elif self.files is not None:
            file_args = ["--", *self.files]
        else:
            file_args = []
        return self.git.diff(
            self.diff_target,
            *self.flags,
            *flags,
            *params,
            *file_args
        )

    def file_lines_changed(self, file):
        diff = self.get_diff(files=[file])
        change_lines = [line for line in diff.split("\n")
                        if line.startswith("+") or line.startswith("-")]
        return len(change_lines)

    def filter_files_by_changed_lines(self):
        self.files = [file for file in self.files if
                      self.file_lines_changed(file) < self.max_lines]

    def get_diff_files(self):
        return self.get_diff("--name-only").split("\n")

    def set_files(self, files):
        self.files = files

    def toggle_flag(self, flag):
        if flag in self.flags:
            self.flags = [f for f in self.flags if f != flag]
        else:
            self.flags.append(f)

    def enable_flag(self, flag):
        if flag not in self.flags:
            self.flags.append(flag)

    def disable_flag(self, flag):
        if flag in self.flags:
            self.flags = [f for f in self.flags if f != flag]

    def set_flag(self, flag, value):
        if value:
            self.enable_flag(flag)
        else:
            self.disable_flag(flag)

    # TODO: Fix this
    def get_message_footer(self):
        author = self.git.config("user.name")
        email = self.git.config("user.email")
        branch = self.git.rev_parse("--abbrev-ref", "HEAD")

        staged = "staged" in self.flags

        self.enable_flag("--staged")
        staged_files = self.get_diff_files()

        self.disable_flag("--staged")
        unstaged_files = self.get_diff_files()

        self.set_flag("--staged", staged)

        message = f"\n# Author:     {author} <{email}>\n"
        message += "#\n"
        message += f"# On branch  {branch}\n"

        message += "# Changes to be committed:\n"
        for file in staged_files:
            message += f"# file:   {file}\n"

        message += "# Changes not staged for commit:\n"
        for file in unstaged_files:
            message += f"# file:   {file}\n"

        message += "#\n"
        return message
