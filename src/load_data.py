import pandas as pd

from i18n import translate


def load_data(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    print(translate("load.info", path=file_path))

    lessons_df = pd.read_excel(file_path, sheet_name="Lessons")
    teachers_df = pd.read_excel(file_path, sheet_name="Teachers")

    lessons_df.columns = lessons_df.columns.str.strip()
    teachers_df.columns = teachers_df.columns.str.strip()

    print(translate("lessons.info", len=len(lessons_df)))
    print(translate("teachers.info", len=len(teachers_df)))

    return pd.DataFrame(lessons_df), pd.DataFrame(teachers_df)
