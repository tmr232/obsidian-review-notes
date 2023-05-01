from pathlib import Path

import git

from obsidian_review_notes.commit_tracker import collect, diffs_to_commands, track
from obsidian_review_notes.vault import Vault


def get_diffs(repo: git.Repo, **kwargs: str) -> list[git.Diff]:
    diffs: list[git.Diff] = []
    for commit in repo.iter_commits(**kwargs):
        # TODO: Handle ordering here - commits are atomic.
        #  We can have a move + a rename that _seem_ to conflict if we disregard this.
        prev = repo.commit(f"{commit.hexsha}~1")
        diffs.extend(prev.diff(commit))

    return diffs[::-1]


def collect_modified(repo: git.Repo, since: str, until: str):
    collect_diffs = get_diffs(repo, since=since, until=until)
    track_diffs = get_diffs(repo, since=until)
    collect_commands = diffs_to_commands(collect_diffs)
    track_commands = diffs_to_commands(track_diffs)

    files: set[str] = set()
    for command in collect_commands:
        files = collect(files, command)

    for command in track_commands:
        files = track(files, command)

    return files


def is_note(name: str) -> bool:
    if Path(name).is_relative_to(Path(".obsidian")):
        return False

    return name.endswith(".md")


# TODO: Make configurable!
EXCLUDED_NOTES = {"Excalibrain/excalibrain.md"}


def links_for_review(root: Path, since: str, until: str) -> list[str]:
    vault = Vault.open(root)
    modified_files = collect_modified(git.Repo(root), since=since, until=until)
    modified_notes = set(filter(is_note, modified_files))
    modified_notes -= EXCLUDED_NOTES
    links = [vault.get_link(Path(note)) for note in modified_notes]
    return links
