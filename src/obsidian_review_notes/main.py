from __future__ import annotations

import sys
from pathlib import Path

import jinja2
import typer

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

    return render_review(
        links=links,
        prev_week=week.prev.name,
        next_week=week.next.name,
        weekdays=week.days,
    )


def review(
    vault: Path = typer.Argument(...),
    review_dir: str = "Weekly",
    year: int = typer.Option(...),
    week: int = typer.Option(...),
    force: bool = False,
    preview: bool = False,
):
    review_week = Week(year=year, week=week)
    weekly_review = make_weekly_review(vault, week=review_week)

    if preview:
        print(f"# {review_week.name}")
        print(weekly_review)

        typer.Exit()
        return

    review_path = (vault / review_dir / review_week.name).with_suffix(".md")

    if review_path.exists() and not force:
        print(
            f"Review note already exists at {review_path}\n"
            "Use --force to overwrite.",
            file=sys.stderr,
        )
        typer.Exit(code=1)
    else:
        review_path.write_text(weekly_review)


def main():
    typer.run(review)


if __name__ == "__main__":
    main()
