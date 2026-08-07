def one_teacher_per_lesson(
    model: cp_model.CpModel,
    assignment_vars,
    lessons: list[Lesson],
    eligibility: dict[str, list[str]],
) -> None:
    """Constraint: exactly one teacher per lesson."""

    infeasible = []
    for lesson in lessons:
        possible = [
            assignment_vars[(lesson.id, name)]
            for name in eligibility[lesson.id]
            if (lesson.id, name) in assignment_vars
        ]

        if not possible:
            infeasible.append(lesson.id)
        else:
            model.add(sum(possible) == 1)

    if infeasible:
        print(translate("constraints.infeasible.lessons.count").format(len(infeasible)))
        print(translate("constraints.infeasible.lessons.list").format(infeasible))
