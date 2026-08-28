from collections import defaultdict

from enums import Week
from models import Assignment, Lesson, Teacher, TeacherStat


def extract_assignments(
    lessons: list[Lesson], assignment_vars_vals: dict[tuple[str, str], int]
) -> tuple[list[Assignment], dict[str, int], dict[str, int], dict[str, int]]:
    assignments: list[Assignment] = []
    total_workload: defaultdict[str, int] = defaultdict(int)
    even_workload: defaultdict[str, int] = defaultdict(int)
    odd_workload: defaultdict[str, int] = defaultdict(int)

    teacher_by_lesson = {
        lesson_id: teacher_id
        for (lesson_id, teacher_id), val in assignment_vars_vals.items()
        if val == 1
    }

    for lesson in lessons:
        teacher_id = teacher_by_lesson.get(lesson.id)

        if teacher_id is not None:
            total_workload[teacher_id] += lesson.two_week_hours
            if lesson.week == Week.EVEN:
                even_workload[teacher_id] += lesson.two_week_hours
            elif lesson.week == Week.ODD:
                odd_workload[teacher_id] += lesson.two_week_hours
            else:
                even_workload[teacher_id] += lesson.two_week_hours // 2
                odd_workload[teacher_id] += lesson.two_week_hours // 2

        assignments.append(Assignment(lesson=lesson, assigned_teacher_id=teacher_id))

    return (
        assignments,
        dict(total_workload),
        dict(even_workload),
        dict(odd_workload),
    )


def build_stats(
    teachers: list[Teacher],
    total_workload: dict[str, int],
    even_workload: dict[str, int],
    odd_workload: dict[str, int],
) -> list[TeacherStat]:
    stats = []
    for teacher in teachers:
        stats.append(
            TeacherStat(
                teacher=teacher,
                total_workload=total_workload.get(teacher.id, 0),
                even_workload=even_workload.get(teacher.id, 0),
                odd_workload=odd_workload.get(teacher.id, 0),
                target_deviation=(
                    total_workload.get(teacher.id, 0) - teacher.target_two_week_workload
                ),
                even_odd_diff=(
                    even_workload.get(teacher.id, 0) - odd_workload.get(teacher.id, 0)
                ),
            )
        )

    return stats
