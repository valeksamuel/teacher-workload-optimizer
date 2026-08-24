from dataclasses import dataclass, field

from ortools.sat.python import cp_model

from enums import Week


@dataclass(slots=True, kw_only=True)
class Lesson:
    # TODO in check_data: Check if all IDs have correct format
    id: str
    name: str
    class_name: str
    two_week_hours: int
    week: Week
    assigned_teacher: Teacher | None = None

    @property
    def get_subject_abbreviation(self) -> str:
        return self.id.split("-")[1]


@dataclass(slots=True, kw_only=True)
class Teacher:
    id: str
    name: str
    min_two_week_workload: int
    target_two_week_workload: int
    max_two_week_workload: int
    subject_qualifications: set[str] = field(default_factory=set)
    workload_var: cp_model.IntVar

    def is_qualified_for(self, subject: str) -> bool:
        return subject in self.subject_qualifications


@dataclass
class PhaseResult:
    assignment_vars_vals: dict[tuple[str, str], int]
    objective_value: int
