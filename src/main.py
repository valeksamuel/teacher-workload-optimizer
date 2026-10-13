import argparse
import sys

import constants as c
from builders import build_eligibility, build_lessons, build_teachers
from console_report import print_phase_comparison, print_phase_stats
from i18n import translate
from loader import load_data
from solver import build_and_solve, phase1_objective, phase2_objective
from stats import build_stats, extract_assignments
from xlsx_output import export_to_excel


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
    teachers_by_id = {teacher.id: teacher for teacher in teachers}
    eligibility = build_eligibility(lessons, teachers)

    print("\n" + c.SEPARATOR)
    print(translate("phase1.start"))
    print(c.SEPARATOR)

    result_ph1 = build_and_solve(
        lessons,
        teachers,
        eligibility,
        prefix="ph1_",
        phase_label=translate("phase1.label"),
        build_objective=phase1_objective,
        time_limit=args.time,
        num_workers=args.workers,
    )
    if result_ph1 is None:
        print(translate("phase1.infeasible"))
        sys.exit(1)

    print(translate("phase1.complete", obj_value=int(result_ph1.objective_value)))

    assignments1, total_wl1, even_wl1, odd_wl1 = extract_assignments(
        lessons, result_ph1.assignment_vars_vals
    )
    stats1 = build_stats(teachers, total_wl1, even_wl1, odd_wl1)
    print_phase_stats(stats1, translate("phase1.stats.title"))

    print("\n" + c.SEPARATOR)
    print(translate("phase2.start"))
    print(c.SEPARATOR)

    result_ph2 = build_and_solve(
        lessons,
        teachers,
        eligibility,
        prefix="ph2_",
        phase_label=translate("phase2.label"),
        build_objective=phase2_objective,
        time_limit=args.time,
        num_workers=args.workers,
        hint=result_ph1.assignment_vars_vals,
    )

    if result_ph2 is None:
        print(translate("phase2.infeasible"))
        result_ph2 = result_ph1

    print(translate("phase2.complete", obj_value=int(result_ph2.objective_value)))

    assignments2, total_wl2, even_wl2, odd_wl2 = extract_assignments(
        lessons, result_ph2.assignment_vars_vals
    )
    stats2 = build_stats(teachers, total_wl2, even_wl2, odd_wl2)
    print_phase_stats(stats2, translate("phase2.stats.title"))

    print_phase_comparison(stats1, stats2)

    # TODO: bug fix, check if console export is OK (I removed in limits), check xlsx exp, refactor based on new input .xlsx and there are errors and tips from claude
    export_to_excel(
        output_path=args.output,
        assignments1=assignments1,
        stats1=stats1,
        assignments2=assignments2,
        stats2=stats2,
        teachers_by_id=teachers_by_id,
    )


if __name__ == "__main__":
    main()
