import pandas as pd
from ortools.sat.python import cp_model

import constants as c
from enums import Week
from models import Lesson, Teacher


def build_teachers(teachers_df: pd.DataFrame) -> list[Teacher]:
    # TODO in check_data: Check if any cell in teachers_df is empty (pd.notna)
    # TODO in check_data: Check if any teacher has negative values

    subject_cols = [col for col in teachers_df.columns if col not in c.INFO_COLS]

    teachers: list[Teacher] = []
    for _, row in teachers_df.iterrows():
        qualifications = {
            subject for subject in subject_cols if subject in row and bool(row[subject])
        }

        teachers.append(
            Teacher(
                id=row[c.COL_TEACHER_ID],
                name=row[c.COL_TEACHER_NAME],
                min_two_week_workload=int(row[c.COL_TEACHER_MIN_2WEEKS_WORKLOAD]),
                target_two_week_workload=int(row[c.COL_TEACHER_TARGET_2WEEKS_WORKLOAD]),
                max_two_week_workload=int(row[c.COL_TEACHER_MAX_2WEEKS_WORKLOAD]),
                subject_qualifications=qualifications,
            )
        )

    return teachers


def build_lessons(lessons_df: pd.DataFrame) -> list[Lesson]:
    lessons: list[Lesson] = []
    for _, row in lessons_df.iterrows():
        fixed_teacher = row[c.COL_SUBJECT_TEACHER]

        if row[c.COL_LESSON_WEEK] == c.WEEK_TYPE_EVEN:
            week_type = Week.EVEN
        elif row[c.COL_LESSON_WEEK] == c.WEEK_TYPE_ODD:
            week_type = Week.ODD
        else:
            week_type = Week.EVERY

        lessons.append(
            Lesson(
                id=row[c.COL_LESSON_ID],
                class_name=row[c.COL_CLASS_NAME],
                name=row[c.COL_LESSON_NAME],
                two_week_hours=row[c.COL_LESSON_WEEKLY_LOAD],
                week=week_type,
                assigned_teacher=fixed_teacher if pd.notna(fixed_teacher) else None,
            )
        )

    return lessons


def build_eligibility(
    lessons: list[Lesson], teachers: list[Teacher]
) -> dict[str, list[str]]:
    # TODO in check_data: Check if any lesson has no eligible teacher
    eligibility: dict[str, list[str]] = {}
    for lesson in lessons:
        eligible = [
            teacher.id
            for teacher in teachers
            if teacher.is_qualified_for(lesson.get_subject_abbreviation)
        ]
        eligibility[lesson.id] = eligible

    return eligibility


def build_assignment_vars(
    model: cp_model.CpModel,
    lessons: list[Lesson],
    eligibility: dict[str, list[str]],
) -> dict[tuple[str, str], cp_model.IntVar]:
    assignment_vars: dict[tuple[str, str], cp_model.IntVar] = {}
    for lesson in lessons:
        for teacher_id in eligibility[lesson.id]:
            var_name = f"assign_{lesson.id}_{teacher_id}"
            assignment_vars[(lesson.id, teacher_id)] = model.new_bool_var(var_name)

    return assignment_vars
