from typing import NewType, Generator

import attrs
import git
import rich


@attrs.frozen
class File:
    name: str

@attrs.frozen
class Deleted:
    name: str

@attrs.frozen
class Added:
    name: str
@attrs.frozen
class Modified:
    name: str


@attrs.frozen
class Renamed:
    old: str
    new: str


Command = NewType("Command", Deleted | Added | Modified | Renamed)


def diffs_to_commands(diffs:list[git.Diff])->list[Command]:
    def _convert()->Generator[Command, None, None]:
        for diff in diffs:
            match diff.change_type:
                case "A":
                    yield Added(diff.b_path)
                case "D":
                    yield Deleted(diff.a_path)
                case "M":
                    yield Modified(diff.a_path)
                case "R":
                    yield Renamed(diff.rename_from, diff.rename_to)
                case _:
                    raise RuntimeError(diff.change_type)

    return list(_convert())

def collect(files: set[File], command: Command):
    new_files = files.copy()
    match command:
        case Added(name):
            new_files.add(name)

        case Deleted(name):
            if name in new_files:
                new_files.remove(name)

        case Modified(name):
            new_files.add(name)

        case Renamed(old, new):
            if old in new_files:
                new_files.remove(old)
                new_files.add(new)

    return new_files

def track(files: set[File], command: Command):
    new_files = files.copy()
    match command:
        case Deleted(name):
            if name in new_files:
                new_files.remove(name)

        case Renamed(old, new):
            if old in new_files:
                new_files.remove(old)
                new_files.add(new)

    return new_files

def main():
    files = set()
    collect_commands = [
        Renamed("a","b"),
        Added("a"),
        ]
    track_commands = [
        Modified("b"),
        Deleted("b"),
        Deleted("a"),
    ]

    for command in collect_commands:
        files = collect(files, command)
        rich.print(files)

    for command in track_commands:
        files = track(files, command)
        rich.print(files)

if __name__ == "__main__":
    main()
