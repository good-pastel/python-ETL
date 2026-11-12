from math import ceil

import pandas as pd

from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from config import (
    OUTPUT_FILE,
    SHEET_NAME,
    DATE_COLUMN,
    MAX_ROWS_PER_SHEET,
    SPLIT_SHEET_BY_MONTH,
    AUTO_SPLIT_SHEET,
    FREEZE_HEADER,
    AUTO_FILTER,
    AUTO_COLUMN_WIDTH,
    FORMULA_PROTECTION,
    REMOVE_ILLEGAL_CHARACTERS,
    CREATE_SUMMARY_SHEET,
)

# ==========================================================
# CONSTANT
# ==========================================================

FORMULA_PREFIX = (
    "=",
    "+",
    "-",
    "@",
)

# Excel memiliki 1.048.576 baris termasuk header
MAX_DATA_ROWS = MAX_ROWS_PER_SHEET - 1


# ==========================================================
# CLEAN CELL
# ==========================================================

def clean_cell(value):

    if pd.isna(value):
        return value

    if not isinstance(value, str):
        return value

    if REMOVE_ILLEGAL_CHARACTERS:
        value = ILLEGAL_CHARACTERS_RE.sub(
            "",
            value,
        )

    if (
        FORMULA_PROTECTION
        and value.lstrip().startswith(FORMULA_PREFIX)
    ):
        value = "'" + value

    return value


# ==========================================================
# CLEAN DATAFRAME
# ==========================================================

def clean_dataframe(df):

    df = df.copy(deep=True)

    object_columns = df.select_dtypes(
        include=[
            "object",
            "string",
        ]
    ).columns

    for column in object_columns:

        df[column] = df[column].apply(
            clean_cell
        )

    return df


# ==========================================================
# FREEZE HEADER
# ==========================================================

def freeze_header(ws):

    if not FREEZE_HEADER:
        return

    ws.freeze_panes = "A2"

    for cell in ws[1]:

        cell.font = Font(
            bold=True
        )


# ==========================================================
# AUTO FILTER
# ==========================================================

def apply_filter(ws):

    if not AUTO_FILTER:
        return

    ws.auto_filter.ref = ws.dimensions


# ==========================================================
# AUTO COLUMN WIDTH
# ==========================================================

def adjust_column_width(ws):

    if not AUTO_COLUMN_WIDTH:
        return

    for column in ws.columns:

        letter = get_column_letter(
            column[0].column
        )

        max_length = 0

        for cell in column:

            if cell.value is None:
                continue

            try:
                length = len(str(cell.value))
            except Exception:
                length = 10

            if length > max_length:
                max_length = length

        ws.column_dimensions[
            letter
        ].width = min(
            max_length + 2,
            50,
        )


# ==========================================================
# SPLIT DATAFRAME
# ==========================================================

def split_dataframe(df):

    if (
        not AUTO_SPLIT_SHEET
        or len(df) <= MAX_DATA_ROWS
    ):
        return [df]

    chunks = []

    total = ceil(
        len(df) / MAX_DATA_ROWS
    )

    for index in range(total):

        start = index * MAX_DATA_ROWS

        end = start + MAX_DATA_ROWS

        chunks.append(
            df.iloc[start:end]
        )

    return chunks

# ==========================================================
# SUMMARY
# ==========================================================

def create_summary_sheet(
    workbook,
    df,
):

    if not CREATE_SUMMARY_SHEET:
        return

    ws = workbook.create_sheet(
        title="Summary",
        index=0,
    )

    summary = {

        "Total Rows": len(df),

        "Source Files": df[
            "_SourceFile"
        ].nunique(),

        "Start Date": df[
            DATE_COLUMN
        ].min(),

        "End Date": df[
            DATE_COLUMN
        ].max(),

    }

    for key, value in summary.items():

        ws.append(
            [key, value]
        )

    freeze_header(ws)

    adjust_column_width(ws)


# ==========================================================
# WRITE SHEET
# ==========================================================

def write_sheet(
    writer,
    df,
    sheet_name,
):

    df = clean_dataframe(df)

    df.to_excel(
        writer,
        sheet_name=sheet_name,
        index=False,
    )

    ws = writer.sheets[
        sheet_name
    ]

    freeze_header(ws)

    apply_filter(ws)

    adjust_column_width(ws)


# ==========================================================
# EXPORT
# ==========================================================

def export_excel(df):

    print()

    print("========== EXPORT ==========")

    if df.empty:
        raise ValueError(
            "Tidak ada data untuk diexport."
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl",
    ) as writer:

        create_summary_sheet(
            writer.book,
            df,
        )

        # ==========================================
        # SPLIT BY MONTH
        # ==========================================

        if SPLIT_SHEET_BY_MONTH:

            months = sorted(
                df["Month"]
                .dropna()
                .unique()
            )

            total_sheet = 0

            for month in months:

                month_df = df[
                    df["Month"] == month
                ]

                chunks = split_dataframe(
                    month_df
                )

                for index, chunk in enumerate(
                    chunks,
                    start=1,
                ):

                    if index == 1:

                        sheet_name = (
                            f"{month:02d}"
                        )

                    else:

                        sheet_name = (
                            f"{month:02d}_{index}"
                        )

                    print(
                        f"Export Sheet : {sheet_name:<8}"
                        f"{len(chunk):>10,} rows"
                    )

                    write_sheet(
                        writer,
                        chunk,
                        sheet_name,
                    )

                    total_sheet += 1

        # ==========================================
        # SINGLE SHEET
        # ==========================================

        else:

            chunks = split_dataframe(df)

            total_sheet = 0

            for index, chunk in enumerate(
                chunks,
                start=1,
            ):

                if index == 1:

                    sheet_name = SHEET_NAME

                else:

                    sheet_name = (
                        f"{SHEET_NAME}_{index}"
                    )

                print(
                    f"Export Sheet : {sheet_name:<8}"
                    f"{len(chunk):>10,} rows"
                )

                write_sheet(
                    writer,
                    chunk,
                    sheet_name,
                )

                total_sheet += 1

    print()

    print(
        f"Total Sheet : {total_sheet}"
    )

    print(
        f"Output File : {OUTPUT_FILE}"
    )

    print(
        f"Total Rows  : {len(df):,}"
    )

    print()