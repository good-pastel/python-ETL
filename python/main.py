import importlib
import time


def main():

    start_time = time.perf_counter()

    print("=" * 60)
    print("             PYTHON ETL TOOLS")
    print("=" * 60)

    # =====================================================
    # IMPORT MODULE
    # =====================================================

    importer = importlib.import_module("01_import_data")
    transformer = importlib.import_module("02_transform_data")
    exporter = importlib.import_module("03_export_excel")

    # =====================================================
    # IMPORT
    # =====================================================

    print("\n[1/3] Import Data")

    df = importer.import_data()

    # =====================================================
    # TRANSFORM
    # =====================================================

    print("\n[2/3] Transform Data")

    df = transformer.transform_data(df)

    # =====================================================
    # EXPORT
    # =====================================================

    print("\n[3/3] Export Excel")

    exporter.export_excel(df)

    # =====================================================
    # FINISH
    # =====================================================

    elapsed = time.perf_counter() - start_time

    print("\n" + "=" * 60)
    print("ETL Completed Successfully")
    print(f"Execution Time : {elapsed:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()