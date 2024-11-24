"""without dash"""

from datetime import datetime

import pandas as pd
import plotly.express as px


def plot_petrol_prices(start_time=None, end_time=None):
    # Read CSV data
    # file_path = "petrol_prices.csv"
    file_path = "price_list_E10_4122.csv"
    data = pd.read_csv(file_path, header=None)
    data.columns = ["DateTime"] + [f"Station {i+1}" for i in range(data.shape[1] - 1)]
    data["DateTime"] = pd.to_datetime(data["DateTime"])

    # Filter data based on the date range
    if start_time:
        start_time = datetime.fromisoformat(start_time)
        data_filtered = data[data["DateTime"] >= start_time]
    else:
        data_filtered = data

    if end_time:
        end_time = datetime.fromisoformat(end_time)
        data_filtered = data_filtered[data_filtered["DateTime"] <= end_time]

    # Melt the data for box plot compatibility
    melted_data = data_filtered.melt(id_vars="DateTime", var_name="Station", value_name="Price")

    # Create the box plot with categorical x-axis
    fig = px.box(
        melted_data,
        x="DateTime",
        y="Price",
        title="Petrol Prices Over Time (Per Timestamp)",
        labels={"DateTime": "Date/Time", "Price": "Price (cents)"},
    )

    # Update x-axis to show only the actual timestamps
    fig.update_xaxes(
        type="category",  # This makes it categorical instead of continuous
        tickangle=45,  # Rotate labels for better readability
        tickformat="%Y-%m-%d %H:%M",
    )

    fig.show()


# Example usage:
start_time = "2024-11-21T00:00:00"
end_time = "2024-11-23T09:00:00"
plot_petrol_prices(start_time, end_time)
