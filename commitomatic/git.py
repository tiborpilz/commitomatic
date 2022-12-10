# First, get a diff from the repo. For now, just use the
# current working directory.
# Then check whether the interactive option is set.
# If yes, get all files that have been changed and prompt the user with a multiselection,
# Afterwards, create a new diff with only the selected files.

from pathlib import Path
from git import Repo


class Repository(object):
    def __init__(self, path: Path, staged: bool = True):
        self.diff_target = None
        self.path = path
        # TODO: error handling
        self.repo = Repo(path)
        assert not self.repo.bare
        self.git = self.repo.git
        self.files = None
        self.flags = ["--staged"] if staged else []

    def get_diff(self, *flags, **kwargs):
        params = [f"--{key} {value}" for key, value in kwargs.items()]
        file_args = ["--", *self.files] if self.files is not None else []
        return self.git.diff(self.diff_target, *self.flags, *flags, *params, *file_args)

    def get_diff_files(self):
        return self.get_diff("--name-only").split("\n")

    def set_files(self, files):
        self.files = files

    def toggle_flag(self, flag):
        if flag in self.flags:
            self.flags = [f for f in self.flags if f != flag]
        else:
            slef.flags.append(f)

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
            message += f"#\file:   {file}\n"

        message += "# Changes not staged for commit:\n"
        for file in unstaged_files:
            message += f"#\file:   {file}\n"

        message += "#"
        return message
