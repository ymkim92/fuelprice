import pandas as pd
import plotly.express as px
from datetime import datetime

# Read CSV data
file_path = "petrol_prices.csv"  # Replace with your file path
data = pd.read_csv(file_path, header=None)

# Define column names
data.columns = ["DateTime"] + [f"Station {i+1}" for i in range(data.shape[1] - 1)]

# Convert DateTime column to pandas datetime format
data["DateTime"] = pd.to_datetime(data["DateTime"])

# Function to filter and plot data
def plot_petrol_prices(start_time=None, end_time=None):
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

    # Create the box plot
    fig = px.box(
        melted_data,
        x="DateTime",
        y="Price",
        title="Petrol Prices Over Time (Per Timestamp)",
        labels={"DateTime": "Date/Time", "Price": "Price (cents)"}
    )

    # Update layout for better visualization
    # fig.update_xaxes(tickformat="%Y-%m-%d %H:%M", rangeslider_visible=True)
    # fig.update_layout(legend_title="Stations", xaxis_title="Date/Time")
    fig.show()

# Example usage:
# Specify the start and end time in ISO format (or leave as None for no filter)
start_time = "2024-11-21T00:00:00"
end_time = "2024-11-23T09:00:00"
plot_petrol_prices(start_time, end_time)
