from ortools.sat.python import cp_model

from i18n import translate
from models import Lesson, Teacher


def add_one_teacher_per_lesson(
    model: cp_model.CpModel,
    assignment_vars: dict[tuple[str, str], cp_model.IntVar],
    lessons: list[Lesson],
    eligibility: dict[str, list[str]],
) -> None:
    """Constraint: exactly one teacher per lesson."""

    infeasible = []
    for lesson in lessons:
        possible = [
            assignment_vars[(lesson.id, teacher_id)]
            for teacher_id in eligibility[lesson.id]
            if (lesson.id, teacher_id) in assignment_vars
        ]

        if not possible:
            infeasible.append(lesson.id)
        else:
            model.add(sum(possible) == 1)

    if infeasible:
        print(
            translate(
                "constraints.infeasible.lessons.count", count_infeasible=len(infeasible)
            )
        )
        print(
            translate(
                "constraints.infeasible.lessons.list", lessons_infeasible=infeasible
            )
        )


def add_fixed_assignments(
    model: cp_model.CpModel,
    assignment_vars: dict[tuple[str, str], cp_model.IntVar],
    lessons: list[Lesson],
) -> None:
    """Constraint: fixed teacher assignments."""
    # TODO in check_data: Check if fixed teacher is eligible for the lesson
    for lesson in lessons:
        fixed_teacher_id = lesson.pre_assigned_teacher_id
        if fixed_teacher_id is not None:
            if (lesson.id, fixed_teacher_id) in assignment_vars:
                model.add(assignment_vars[(lesson.id, fixed_teacher_id)] == 1)
            else:
                print(
                    translate(
                        "constraints.fixed.assignment.not.valid",
                        lesson_id=lesson.id,
                        teacher_id=fixed_teacher_id,
                    )
                )


def add_workload_limits(
    model: cp_model.CpModel,
    lessons: list[Lesson],
    teachers: list[Teacher],
    assignment_vars: dict[tuple[str, str], cp_model.IntVar],
) -> dict[str, cp_model.IntVar]:
    """Constraint: min and max workload limits."""
    workload_vars: dict[str, cp_model.IntVar] = {}
    for teacher in teachers:
        terms = []
        for lesson in lessons:
            if (lesson.id, teacher.id) in assignment_vars:
                terms.append(
                    assignment_vars[(lesson.id, teacher.id)] * lesson.two_week_hours
                )

        var = model.new_int_var(
            0, teacher.max_two_week_workload, f"workload_{teacher.id}"
        )
        model.add(var == (sum(terms) if terms else 0))
        workload_vars[teacher.id] = var

        if terms:
            model.add(var >= teacher.min_two_week_workload)
            model.add(var <= teacher.max_two_week_workload)

    return workload_vars
