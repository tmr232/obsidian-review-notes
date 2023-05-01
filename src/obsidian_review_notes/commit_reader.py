from pathlib import Path

import pygit2
from pygit2 import Repository
import rich
import git

from obsidian_review_notes.commit_tracker import diffs_to_commands, track, collect
from obsidian_review_notes.main import Vault

REPO_PATH = r"c:\Temp\git-rename-test"


def main_pygit():
    repo = Repository(REPO_PATH)

    diff = repo.diff("bc7c3b21a47deb989c21522c0fae4d3111834313", "d2a5df6ee61a75369ae0da09da73d4fc342ae537")
    for delta in diff.deltas:
        rich.inspect(delta)
        print(delta.old_file.path, delta.new_file.path)

def get_diffs(repo:git.Repo, **kwargs:str)->list[git.Diff]:
    diffs:list[git.Diff] = []
    for commit in repo.iter_commits(**kwargs):
        # TODO: Handle ordering here - commits are atomic.
        #  We can have a move + a rename that _seem_ to conflict if we disregard this.
        prev = repo.commit(f"{commit.hexsha}~1")
        diffs.extend(prev.diff(commit))

    return diffs[::-1]


def collect_modified(repo:git.Repo, since:str, until:str):
    collect_diffs = get_diffs(repo, since=since, until=until)
    track_diffs = get_diffs(repo, since=until)
    collect_commands = diffs_to_commands(collect_diffs)
    track_commands = diffs_to_commands(track_diffs)

    files = set()
    for command in collect_commands:
        files = collect(files, command)

    for command in track_commands:
        files = track(files, command)

    return files


def is_note(name:str)->bool:
    if Path(name).is_relative_to(Path(".obsidian")):
        return False

    return name.endswith(".md")

def links_for_review(root:Path, since:str, until:str)->list[str]:
    vault = Vault.open(root)
    modified_files = collect_modified(git.Repo(root), since=since, until=until)
    modified_notes = list(filter(is_note, modified_files))
    links = [vault.get_link(Path(note)) for note in modified_notes]
    return links


def main():

    rich.print(links_for_review(Path(r"C:\Users\tamir\OneDrive\Documents\Obsidian Vault"), since="2023-04-10", until="2023-04-20"))


if __name__ == "__main__":
    main()