"""
A module for analyzing and visualizing petrol price data over time. Provides functionality
to load petrol price data from CSV files and create interactive box plots using Plotly.

The module includes functions for:
- Loading and preprocessing CSV data containing petrol prices
- Creating box plots showing price distributions over time
- Filtering data by time ranges
- Web interface integration for interactive visualization

The data format expected is CSV files with a datetime column followed by price columns
for different petrol stations. The module handles CSVs with varying numbers of stations.
"""

import os
from datetime import datetime
from typing import Optional, Union

import pandas as pd
import plotly.express as px  # type: ignore[import-untyped]
from plotly.graph_objects import Figure  # type: ignore[import-untyped]


def load_data(file_path: str) -> pd.DataFrame:
    """Load and prepare the data from CSV file"""
    # First pass to determine maximum number of columns
    with open(file_path, encoding="utf-8") as f:
        max_cols = max(len(line.strip().split(",")) for line in f)

    # Read CSV with the maximum number of columns
    data = pd.read_csv(
        file_path,
        header=None,
        names=["DateTime"] + [f"Station {i+1}" for i in range(max_cols - 1)],
        on_bad_lines="warn",
    )

    data["DateTime"] = pd.to_datetime(data["DateTime"])
    return data


def plot_petrol_prices(
    data: pd.DataFrame,
    start_time: Optional[Union[str, datetime]] = None,
    end_time: Optional[Union[str, datetime]] = None,
    csv_filename: Optional[str] = None,
) -> Figure:
    """
    Create a box plot of petrol prices over time

    Args:
        data: DataFrame containing petrol price data
        start_time: Start time for filtering data (ISO format string or datetime object)
        end_time: End time for filtering data (ISO format string or datetime object)
        csv_filename: Name of the CSV file for the title

    Returns:
        Plotly Figure object
    """
    # Filter data based on the date range
    data_filtered = data.copy()

    if start_time:
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        data_filtered = data_filtered[data_filtered["DateTime"] >= start_time]

    if end_time:
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)
        data_filtered = data_filtered[data_filtered["DateTime"] <= end_time]

    # Melt the data for box plot compatibility
    melted_data = data_filtered.melt(id_vars="DateTime", var_name="Station", value_name="Price")

    # Create title with CSV filename if provided
    base_title = "Petrol Prices Over Time"
    title = f"{base_title} - {csv_filename}" if csv_filename else base_title

    # Create the box plot
    fig = px.box(
        melted_data,
        x="DateTime",
        y="Price",
        title=title,
        labels={"DateTime": "Date/Time", "Price": "Price (cents)"},
    )

    # Update x-axis to show only the actual timestamps
    fig.update_xaxes(
        type="category",  # This makes it categorical instead of continuous
        tickangle=45,  # Rotate labels for better readability
        tickformat="%Y-%m-%d %H:%M",
    )
    return fig


# For web usage, you can create a function that handles the web interface
def create_web_plot(
    csv_path: str,
    start_time_str: Optional[str] = None,
    end_time_str: Optional[str] = None,
) -> Figure:
    """
    Create plot for web display with optional time filtering

    Args:
        csv_path: Path to the CSV file
        start_time_str: Start time in ISO format (YYYY-MM-DDTHH:MM:SS)
        end_time_str: End time in ISO format (YYYY-MM-DDTHH:MM:SS)

    Returns:
        Plotly Figure object
    """
    # Load data
    data = load_data(csv_path)
    csv_filename = os.path.basename(csv_path)

    # Create and return the plot
    return plot_petrol_prices(data, start_time_str, end_time_str, csv_filename)
