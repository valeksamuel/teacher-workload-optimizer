from openpyxl import Workbook

from i18n import translate
from models import Assignment, TeacherStat


def export_to_excel(
    output_path: str,
    assignments1: list[Assignment],
    stats1: list[TeacherStat],
    assignments2: list[Assignment],
    stats2: list[TeacherStat],
) -> None:
    wb = Workbook()
    default_sheet = wb.active
    assert default_sheet is not None
    wb.remove(default_sheet)

    # sheet_assignments(wb, translate("excel.sheet1.title"), assignments1, 1)
    # sheet_teachers(wb, translate("excel.sheet2.title"), stats1, 1)
    # sheet_assignments(wb, translate("excel.sheet3.title"), assignments2, 2)
    # sheet_teachers(wb, translate("excel.sheet4.title"), stats2, 2)

    wb.save(output_path)

    print(translate("excel.export.complete", output_path=output_path))
