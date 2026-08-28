import constants as c
from i18n import translate
from models import TeacherStat


def print_phase_stats(stats: list[TeacherStat], title: str) -> None:
    print("\n" + c.SEPARATOR)
    print(title)
    print(c.SEPARATOR)

    print(format_row([label for label, _, _ in c.CONSOLE_COLS]))
    print(" ".join("─" * width for _, width, _ in c.CONSOLE_COLS))

    for s in stats:
        print(format_row(teacher_row_values(s)))

    total_dev = sum(abs(s.target_deviation) for s in stats)
    total_diff = sum(abs(s.even_odd_diff) for s in stats)
    print(c.SEPARATOR)
    print(
        f"{translate('console.sum'):.<30} {'':>7} {'':>5} {total_dev:>+6.1f} "
        f"{'':>7} {'':>7} {total_diff:>+6.1f}"
    )


def format_row(values: list[str]) -> str:
    cells = [
        f"{v:{align}{width}}"
        for v, (_, width, align) in zip(values, c.CONSOLE_COLS, strict=True)
    ]
    return " ".join(cells)


def teacher_row_values(s: TeacherStat) -> list[str]:
    return [
        s.teacher.name,
        f"{s.total_workload:.1f}",
        str(s.teacher.target_two_week_workload),
        f"{s.target_deviation:+.1f}",
        f"{s.even_workload:.1f}",
        f"{s.odd_workload:.1f}",
        f"{s.even_odd_diff:+.1f}",
    ]


def print_phase_comparison(
    stats1: list[TeacherStat], stats2: list[TeacherStat]
) -> None:
    total_dev_p1 = sum(abs(s.target_deviation) for s in stats1)
    total_dev_p2 = sum(abs(s.target_deviation) for s in stats2)
    total_diff_p1 = sum(abs(s.even_odd_diff) for s in stats1)
    total_diff_p2 = sum(abs(s.even_odd_diff) for s in stats2)

    print("\n" + c.SEPARATOR)
    print(translate("console.phase.comparison.header"))
    print(c.SEPARATOR)
    print(
        translate(
            "console.phase.comparison.dev",
            total_dev_p1=total_dev_p1,
            total_dev_p2=total_dev_p2,
        )
    )
    print(
        translate(
            "console.phase.comparison.diff",
            total_diff_p1=total_diff_p1,
            total_diff_p2=total_diff_p2,
        )
    )
