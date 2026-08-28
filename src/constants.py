from i18n import translate

COL_LESSON_ID = translate("excel.col.lesson.id")
COL_CLASS_NAME = translate("excel.col.class.name")
COL_LESSON_NAME = translate("excel.col.lesson.name")
COL_LESSON_WEEKLY_LOAD = translate("excel.col.lesson.weekly.load")
COL_LESSON_WEEK = translate("excel.col.lesson.week")
COL_SUBJECT_TEACHER = translate("excel.col.subject.teacher")
COL_TEACHER_ID = translate("excel.col.teacher.id")
COL_TEACHER_NAME = translate("excel.col.teacher.name")
COL_TEACHER_MIN_2WEEKS_WORKLOAD = translate("excel.col.min.2week.workload")
COL_TEACHER_TARGET_2WEEKS_WORKLOAD = translate("excel.col.target.2week.workload")
COL_TEACHER_MAX_2WEEKS_WORKLOAD = translate("excel.col.max.2week.workload")
INFO_COLS = {
    COL_TEACHER_ID,
    COL_TEACHER_NAME,
    COL_TEACHER_MIN_2WEEKS_WORKLOAD,
    COL_TEACHER_TARGET_2WEEKS_WORKLOAD,
    COL_TEACHER_MAX_2WEEKS_WORKLOAD,
}
WEEK_TYPE_EVEN = translate("week.type.even")
WEEK_TYPE_ODD = translate("week.type.odd")
WEEK_TYPE_EVERY = translate("week.type.every")

# Console printing - adjust column widths and alignment for better readability
SEPARATOR = "─" * 62
CONSOLE_COLS = [
    (translate("console.col.teacher"), 30, "<"),
    (translate("console.col.workload"), 7, ">"),
    (translate("console.col.target"), 5, ">"),
    (translate("console.col.deviation"), 6, ">"),
    (translate("console.col.even"), 7, ">"),
    (translate("console.col.odd"), 7, ">"),
    (translate("console.col.e.o.diff"), 6, ">"),
]
