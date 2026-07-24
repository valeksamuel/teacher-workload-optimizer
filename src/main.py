import argparse

from builders import build_eligibility, build_lessons, build_teachers
from i18n import translate
from loader import load_data


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


if __name__ == "__main__":
    main()
