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
