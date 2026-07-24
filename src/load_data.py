import pandas as pd

from i18n import translate


def load_data(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    # TODO in check_data: Check for duplicate lesson IDS

    print(translate("load.info", path=file_path))

    lessons_df = pd.read_excel(file_path, sheet_name=translate("excel.sheet.lessons"))
    teachers_df = pd.read_excel(file_path, sheet_name=translate("excel.sheet.teachers"))

    lessons_df.columns = lessons_df.columns.str.strip()
    teachers_df.columns = teachers_df.columns.str.strip()

    lessons_df = lessons_df[
        [col for col in lessons_df.columns if not str(col).startswith("Unnamed")]
    ]
    teachers_df = teachers_df[
        [col for col in teachers_df.columns if not str(col).startswith("Unnamed")]
    ]

    print(translate("lessons.info", len=len(lessons_df)))
    print(translate("teachers.info", len=len(teachers_df)))

    return pd.DataFrame(lessons_df), pd.DataFrame(teachers_df)
