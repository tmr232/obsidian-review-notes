from __future__ import annotations

import glob
import typing
from collections import defaultdict
from pathlib import Path

import attrs


def get_all_notes(root: str) -> list[str]:
    return glob.glob("**/*.md", root_dir=root, recursive=True)


def get_note_name(note: Path) -> str:
    return note.name.rstrip(".md")


def make_full_link(note: Path) -> str:
    return note.as_posix().rstrip(".md")


@attrs.frozen
class Vault:
    root: Path
    notes: list[Path]
    _links: dict[Path, str]

    @staticmethod
    def open(root: Path) -> Vault:
        notes = [Path(path) for path in get_all_notes(str(root))]

        names: typing.DefaultDict[str, set[Path]] = defaultdict(set)
        for note in notes:
            names[get_note_name(note)].add(note)

        links: dict[Path, str] = {}
        for name, sharers in names.items():
            if len(sharers) > 1:
                for note in sharers:
                    links[note] = make_full_link(note)
            else:
                note, *_ = sharers
                links[note] = name

        return Vault(root=root, notes=notes, links=links)

    def get_link(self, note: Path) -> str:
        return f"[[{self._links[note]}]]"
