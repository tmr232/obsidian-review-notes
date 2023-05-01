from __future__ import annotations

import datetime

import attrs


def prev_day(date: datetime.date) -> datetime.date:
    return datetime.date.fromordinal(date.toordinal() - 1)


def next_day(date: datetime.date) -> datetime.date:
    return datetime.date.fromordinal(date.toordinal() + 1)


def prev_week(date: datetime.date) -> datetime.date:
    return datetime.date.fromordinal(date.toordinal() - 7)


def next_week(date: datetime.date) -> datetime.date:
    return datetime.date.fromordinal(date.toordinal() + 7)


def get_week_name(*, year: int, week: int) -> str:
    return f"{year:04}-W{week:02}"


def week_to_range(
    *, year: int, week: int, start_on_sunday: bool = True
) -> tuple[str, str]:
    week_name = get_week_name(year=year, week=week)
    week_start = datetime.date.fromisoformat(week_name)
    week_end = next_week(week_start)

    if start_on_sunday:
        week_start = prev_day(week_start)
        week_end = prev_day(week_end)

    return week_start.isoformat(), week_end.isoformat()


def date_to_week(
    *, date: datetime.date, start_on_sunday: bool = True
) -> tuple[int, int]:
    if start_on_sunday:
        date = next_day(date)

    iso = date.isocalendar()
    return iso.year, iso.week


@attrs.frozen
class Week:
    year: int
    week: int
    week_starts_sunday: bool = True

    @staticmethod
    def from_date(
        year: int, month: int, day: int, *, week_starts_sunday: bool = True
    ) -> Week:
        year, week = date_to_week(
            date=datetime.date(year, month, day), start_on_sunday=week_starts_sunday
        )

        return Week(year=year, week=week, week_starts_sunday=week_starts_sunday)

    @property
    def name(self):
        return get_week_name(year=self.year, week=self.week)

    @property
    def next(self):
        year, month, day, *_ = next_week(self._as_date()).timetuple()
        return Week.from_date(
            year, month, day, week_starts_sunday=self.week_starts_sunday
        )

    @property
    def prev(self):
        year, month, day, *_ = prev_week(self._as_date()).timetuple()
        return Week.from_date(
            year, month, day, week_starts_sunday=self.week_starts_sunday
        )

    def _as_date(self) -> datetime.date:
        return datetime.date.fromisocalendar(self.year, self.week, 1)

    @property
    def days(self):
        date = datetime.date
        week_start = self._as_date()
        return [
            date.fromordinal(week_start.toordinal() + offset) for offset in range(7)
        ]

    @property
    def begin(self):
        return self._as_date()

    @property
    def end(self):
        return prev_day(self.next._as_date())


def main():
    print(week_to_range(year=2015, week=1))
    print(week_to_range(year=2023, week=1))
    print(date_to_week(date=datetime.date(2014, 12, 28)))

    week = Week(2023, 17)
    print(week.days)
    print(week.begin)
    print(week.end)


if __name__ == "__main__":
    main()
