from dataclasses import dataclass, field


@dataclass(slots=True)
class Lesson:
    id: str
    name: str
    class_name: str
    two_week_hours: int
    week: str
    assigned_teacher: Teacher | None = None


@dataclass(slots=True)
class Teacher:
    id: str
    name: str
    min_two_week_workload: int
    target_two_week_workload: int
    max_two_week_workload: int
    subject_qualifications: set[str] = field(default_factory=set)
