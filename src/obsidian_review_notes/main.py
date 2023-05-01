from __future__ import annotations

from pathlib import Path

import jinja2

from obsidian_review_notes.commit_reader import links_for_review
from obsidian_review_notes.weeks import Week


def render_review(*args, **kwargs) -> str:
    env = jinja2.Environment(
        loader=jinja2.PackageLoader("obsidian_review_notes", "templates"),
    )
    template = env.get_template("review.md")

    return template.render(*args, **kwargs)


def make_weekly_review(root: Path, *, week: Week):
    links = links_for_review(root, since=week.begin, until=week.end)

    print(
        render_review(
            links=links,
            prev_week=week.prev.name,
            next_week=week.next.name,
            weekdays=week.days,
        )
    )


def main():
    make_weekly_review(
        Path(r"C:\Users\tamir\OneDrive\Documents\Obsidian Vault"),
        week=Week(year=2023, week=17),
    )


if __name__ == "__main__":
    main()
