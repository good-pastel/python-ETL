import zipfile
from pathlib import Path

import pandas as pd

from config import (
    INPUT_FOLDER,
    SUPPORTED_FILES,
)


# ==========================================================
# PREPARE DATAFRAME
# ==========================================================

def prepare_dataframe(
    df,
    source_file,
    source_type,
    sheet_name=None,
):

    df.columns = (
        df.columns.astype(str)
        .str.strip()
    )

    df["_SourceFile"] = source_file
    df["_SourceType"] = source_type
    df["_SheetName"] = sheet_name

    return df


# ==========================================================
# READ CSV
# ==========================================================

def read_csv(file_path):

    df = pd.read_csv(
        file_path,
        low_memory=False,
    )

    return prepare_dataframe(
        df,
        source_file=file_path.name,
        source_type="CSV",
    )


# ==========================================================
# READ EXCEL
# ==========================================================

def read_excel(file_path):

    dataframes = []

    workbook = pd.read_excel(
        file_path,
        sheet_name=None,
    )   

    for sheet_name, df in workbook.items():

        df = prepare_dataframe(
            df,
            source_file=file_path.name,
            source_type="EXCEL",
            sheet_name=sheet_name,
        )

        dataframes.append(df)

    return dataframes


# ==========================================================
# READ ZIP
# ==========================================================

def read_zip(file_path):

    dataframes = []

    with zipfile.ZipFile(file_path) as zip_file:

        for member in zip_file.namelist():

            if not member.lower().endswith(".csv"):
                continue

            with zip_file.open(member) as csv_file:

                df = pd.read_csv(
                    csv_file,
                    low_memory=False,
                )

            df = prepare_dataframe(
                df,
                source_file=f"{file_path.name}/{member}",
                source_type="ZIP",
            )

            dataframes.append(df)

    return dataframes


# ==========================================================
# IMPORT
# ==========================================================

def import_data():

    print()

    print("========== IMPORT ==========")

    if not INPUT_FOLDER.exists():

        raise FileNotFoundError(
            f"Folder '{INPUT_FOLDER}' tidak ditemukan."
        )

    dataframes = []

    files = sorted(INPUT_FOLDER.iterdir())

    if not files:

        raise FileNotFoundError(
            "Folder data kosong."
        )

    print()

    for file_path in files:

        suffix = file_path.suffix.lower()

        if suffix not in SUPPORTED_FILES:
            continue

        print(file_path.name)

        if suffix == ".csv":

            dataframes.append(
                read_csv(file_path)
            )

        elif suffix in (".xlsx", ".xls"):

            dataframes.extend(
                read_excel(file_path)
            )

        elif suffix == ".zip":

            dataframes.extend(
                read_zip(file_path)
            )

    if not dataframes:

        raise ValueError(
            "Tidak ada data yang berhasil diimport."
        )

    df = pd.concat(
        dataframes,
        ignore_index=True,
        sort=False,
    )

    print()

    print(f"Source File : {len(files):,}")
    print(f"Total Rows  : {len(df):,}")

    return df