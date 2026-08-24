import argparse
import sys

from builders import build_eligibility, build_lessons, build_teachers
from i18n import translate
from loader import load_data
from solver import build_and_solve, phase1_objective, phase2_objective


def main() -> None:
    parser = argparse.ArgumentParser(description=translate("cli.description"))
    parser.add_argument(
        "--input", default="input.xlsx", help=translate("cli.input.help")
    )
    parser.add_argument(
        "--output", default="output.xlsx", help=translate("cli.output.help")
    )
    parser.add_argument(
        "--time", type=int, default=120, help=translate("cli.time.help")
    )
    parser.add_argument(
        "--workers", type=int, default=8, help=translate("cli.workers.help")
    )
    args = parser.parse_args()

    print(translate("initial.message.top"))
    print(translate("initial.message.mid"))
    print(translate("initial.message.bottom"))

    lessons_df, teachers_df = load_data(args.input)
    lessons = build_lessons(lessons_df)
    teachers = build_teachers(teachers_df)
    eligibility = build_eligibility(lessons, teachers)

    print("\n" + "═" * 62)
    print(translate("phase1.start"))
    print("═" * 62)

    result_ph1 = build_and_solve(
        lessons,
        teachers,
        eligibility,
        prefix="ph1_",
        phase_label="Fáza 1",
        build_objective=phase1_objective,
        time_limit=args.time,
        num_workers=args.workers,
    )
    if result_ph1 is None:
        print(translate("phase1.infeasible"))
        sys.exit(1)

    print(translate("phase1.complete", obj_value=int(result_ph1.objective_value)))

    print("\n" + "═" * 62)
    print(translate("phase2.start"))
    print("═" * 62)

    result_ph2 = build_and_solve(
        lessons,
        teachers,
        eligibility,
        prefix="ph2_",
        phase_label="Fáza 2",
        build_objective=phase2_objective,
        time_limit=args.time,
        num_workers=args.workers,
        hint=result_ph1.assignment_vars_vals,
    )

    if result_ph2 is None:
        print(translate("phase2.infeasible"))
        result_ph2 = result_ph1

    print(translate("phase2.complete", obj_value=int(result_ph2.objective_value)))


if __name__ == "__main__":
    main()
