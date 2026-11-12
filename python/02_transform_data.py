import pandas as pd

from config import (
    DATE_COLUMN,
    DATE_FORMATS,
    START_DATE,
    END_DATE,
)


# ==========================================================
# CONVERT DATETIME
# ==========================================================

def convert_datetime(df):

    if DATE_COLUMN not in df.columns:
        raise KeyError(
            f"Kolom '{DATE_COLUMN}' tidak ditemukan."
        )

    print()
    print("Convert Datetime")

    print("\n===== TYPE =====")
    print(df[DATE_COLUMN].apply(type).value_counts())

    print("\nFormat yang dicoba:")

    for fmt in DATE_FORMATS:
        print(f" - {fmt}")

    parsed = pd.Series(pd.NaT, index=df.index)

    for fmt in DATE_FORMATS:

        mask = parsed.isna()

        parsed.loc[mask] = pd.to_datetime(
            df.loc[mask, DATE_COLUMN],
            format=fmt,
            errors="coerce",
        )

    df[DATE_COLUMN] = parsed

    return df


# ==========================================================
# REMOVE INVALID DATE
# ==========================================================

def remove_invalid_date(df):

    before = len(df)

    df = df.dropna(
        subset=[DATE_COLUMN]
    )

    after = len(df)

    print()

    print(f"Invalid Date : {before-after:,}")
    print(f"Valid Date   : {after:,}")

    return df


# ==========================================================
# FILTER DATE
# ==========================================================

def filter_date(df):

    if START_DATE:

        start = pd.to_datetime(
            START_DATE
        )

        df = df[
            df[DATE_COLUMN] >= start
        ]

    if END_DATE:

        end = pd.to_datetime(
            END_DATE
        )

        df = df[
            df[DATE_COLUMN] <= end
        ]

    return df


# ==========================================================
# SORT DATA
# ==========================================================

def sort_data(df):

    return (
        df.sort_values(DATE_COLUMN)
        .reset_index(drop=True)
    )


# ==========================================================
# ADD MONTH COLUMN
# ==========================================================

def add_month(df):

    df["Month"] = df[
        DATE_COLUMN
    ].dt.month

    return df


# ==========================================================
# TRANSFORM
# ==========================================================

def transform_data(df):

    print()

    print("========== TRANSFORM ==========")

    df = convert_datetime(df)

    df = remove_invalid_date(df)

    df = filter_date(df)

    df = sort_data(df)

    df = add_month(df)

    print()

    print(
        "Date Range : "
        f"{df[DATE_COLUMN].min()} "
        "-> "
        f"{df[DATE_COLUMN].max()}"
    )

    print()

    print(f"Total Rows : {len(df):,}")

    return df