
from __future__ import annotations

import datetime
import glob
import typing
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import importlib.resources
import attrs
import jinja2
import pydriller


def get_all_notes(root: str) -> list[str]:
    return glob.glob("**/*.md", root_dir=root, recursive=True)


def get_note_name(note:Path)->str:
    return note.name.rstrip(".md")

def make_full_link(note:Path)->str:
    return note.as_posix().rstrip(".md")
@attrs.frozen
class Vault:
    root: Path
    notes: list[Path]
    _links: dict[Path, str]

    @staticmethod
    def open(root:Path)->Vault:
        notes = [Path(path) for path in get_all_notes(str(root))]

        names:typing.DefaultDict[str, set[Path]] = defaultdict(set)
        for note in notes:
            names[get_note_name(note)].add(note)

        links:dict[Path, str] = {}
        for name, sharers in names.items():
            if len(sharers) > 1:
                for note in sharers:
                    links[note]  =make_full_link(note)
            else:
                note, *_ = sharers
                links[note] = name

        return Vault(root=root, notes=notes, links=links)

    def get_link(self, note:Path)->str:
        return f"[[{self._links[note]}]]"


def was_changed(
    repo: str,
    file: str,
    since: datetime | None = None,
    to: datetime | None = None,
    from_commit: str | None = None,
    to_commit: str | None = None,
):
    for _ in pydriller.Repository(
        repo, since=since, to=to, filepath=file
    ).traverse_commits():
        return True
    return False


def main():
    links = []
    vault = Vault.open(Path(r"C:\Users\tamir\OneDrive\Documents\Obsidian Vault"))
    for note in vault.notes:
        if was_changed(str(vault.root), str(note), datetime.now() - timedelta(days=7)):
            links.append(vault.get_link(note))

    env = jinja2.Environment(
        loader=jinja2.PackageLoader("obsidian_review_notes","templates"),
    )
    template = env.get_template("review.md")
    print(template.render(links=links))


if __name__ == "__main__":
    main()
