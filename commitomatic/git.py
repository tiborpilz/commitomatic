# First, get a diff from the repo. For now, just use the
# current working directory.
# Then check whether the interactive option is set.
# If yes, get all files that have been changed and prompt the user with a multiselection,
# Afterwards, create a new diff with only the selected files.

from pathlib import Path
from git import Repo


class Repository(object):
    def __init__(self, path: Path):
        self.diff_target = None
        self.path = path
        # TODO: error handling
        self.repo = Repo(path)
        assert not self.repo.bare
        self.git = self.repo.git

    def get_diff(self, *flags, **kwargs):
        params = [f"--{key} {value}" for key, value in kwargs.items()]
        return self.git.diff(self.diff_target, *flags, *params)

    def get_diff_files(self):
        return self.get_diff("--name-only").split("\n")
