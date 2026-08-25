from ortools.sat.python import cp_model

from builders import build_assignment_vars
from constraints import (
    add_fixed_assignments,
    add_one_teacher_per_lesson,
    add_workload_limits,
)
from enums import Week
from i18n import translate
from models import Lesson, PhaseResult, Teacher


def build_and_solve(
    lessons: list[Lesson],
    teachers: list[Teacher],
    eligibility: dict[str, list[str]],
    prefix: str,
    phase_label: str,
    build_objective,
    time_limit: int,
    num_workers: int,
    hint: dict[tuple[str, str], int] | None = None,
) -> PhaseResult | None:
    model = cp_model.CpModel()

    assignment_vars = build_assignment_vars(model, lessons, eligibility)

    add_one_teacher_per_lesson(model, assignment_vars, lessons, eligibility)
    add_fixed_assignments(model, assignment_vars, lessons)
    add_workload_limits(model, lessons, teachers, assignment_vars)

    objective_terms = build_objective(model, assignment_vars, lessons, teachers)

    model.minimize(sum(objective_terms))

    if hint:
        for (lesson_id, teacher_id), var in assignment_vars.items():
            if (lesson_id, teacher_id) in hint:
                model.add_hint(var, hint[(lesson_id, teacher_id)])

    solver = solve(model, time_limit, num_workers, phase_label)
    if solver is None:
        return None

    vals = {key: solver.value(var) for key, var in assignment_vars.items()}

    return PhaseResult(
        assignment_vars_vals=vals, objective_value=solver.objective_value
    )


def phase1_objective(
    model: cp_model.CpModel,
    assignment_vars: dict[tuple[str, str], cp_model.IntVar],
    lessons: list[Lesson],
    teachers: list[Teacher],
) -> list[cp_model.IntVar]:
    deviations = []
    for teacher in teachers:
        deviation = model.new_int_var(
            0,
            teacher.max_two_week_workload - teacher.min_two_week_workload,
            f"ph1_dev_{teacher.id}",
        )
        assert teacher.workload_var is not None, (
            "Workload variable should be set for each teacher."
        )
        model.add_abs_equality(
            deviation, teacher.workload_var - teacher.target_two_week_workload
        )
        deviations.append(deviation)

    return deviations


def phase2_objective(
    model: cp_model.CpModel,
    assignment_vars: dict[tuple[str, str], cp_model.IntVar],
    lessons: list[Lesson],
    teachers: list[Teacher],
) -> list[cp_model.IntVar]:
    imbalances = []
    for teacher in teachers:
        even_terms = []
        odd_terms = []

        for lesson in lessons:
            if (lesson.id, teacher.id) not in assignment_vars:
                continue

            var = assignment_vars[(lesson.id, teacher.id)]

            if lesson.week == Week.EVEN:
                even_terms.append(var * lesson.two_week_hours)
            elif lesson.week == Week.ODD:
                odd_terms.append(var * lesson.two_week_hours)
            else:
                even_terms.append(var * lesson.two_week_hours)
                odd_terms.append(var * lesson.two_week_hours)

            even_var = model.new_int_var(
                0, teacher.max_two_week_workload, f"ph2_even_{teacher.id}"
            )
            odd_var = model.new_int_var(
                0, teacher.max_two_week_workload, f"ph2_odd_{teacher.id}"
            )
            diff = model.new_int_var(
                0, teacher.max_two_week_workload, f"ph2_diff_{teacher.id}"
            )

            model.add(even_var == (sum(even_terms) if even_terms else 0))
            model.add(odd_var == (sum(odd_terms) if odd_terms else 0))
            model.add_abs_equality(diff, even_var - odd_var)

            imbalances.append(diff)

    return imbalances


def solve(
    model: cp_model.CpModel, time_limit: int, num_workers: int, phase_label: str
) -> cp_model.CpSolver | None:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = num_workers
    solver.parameters.log_search_progress = False  # set to True for debugging

    print(
        translate(
            "solver.phase.start",
            phase=phase_label,
            time_limit=time_limit,
            num_workers=num_workers,
        )
    )

    status = solver.solve(model)

    if status == cp_model.OPTIMAL:
        print(translate("solver.optimal.solution"))
        return solver

    if status == cp_model.FEASIBLE:
        print(translate("solver.feasible.solution"))
        return solver

    print(translate("solver.no.solution", status=solver.status_name(status)))
    return None
