import pandas as pd
import pytest

from fuel_price.boxplot_with_dash import load_data


def test_load_data(tmp_path):
    """Test the load_data function"""
    # Create a test CSV file using Path
    test_csv = tmp_path / "test.csv"
    test_data = """2023-01-01 00:00,150.1,155.2
2023-01-01 01:00,151.1,156.2,1.2"""

    # Write the test data using Path
    test_csv.write_text(test_data)

    # Load the test data
    df = load_data(test_csv)

    # Check the structure and content
    assert isinstance(df, pd.DataFrame), "Result should be a pandas DataFrame"
    assert list(df.columns)[0] == "DateTime"
    assert len(df) == 2, "DataFrame should have 2 rows"
    assert pd.api.types.is_datetime64_any_dtype(
        df["DateTime"]
    ), "DateTime column should be datetime type"
    assert df["Station 1"].dtype == float, "Station 1 column should be float type"
    assert df["Station 2"].dtype == float, "Station 2 column should be float type"

    # Test specific values
    pd.testing.assert_series_equal(
        df["Station 1"], pd.Series([150.1, 151.1], name="Station 1"), check_names=True
    )

    # Test datetime parsing
    expected_dates = pd.to_datetime(["2023-01-01 00:00", "2023-01-01 01:00"])
    pd.testing.assert_series_equal(
        df["DateTime"], pd.Series(expected_dates, name="DateTime"), check_names=True
    )
