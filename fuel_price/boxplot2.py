import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Optional, Union
from plotly.graph_objects import Figure

def load_data(file_path: str) -> pd.DataFrame:
    """Load and prepare the data from CSV file"""
    data = pd.read_csv(file_path, header=None)
    data.columns = ["DateTime"] + [f"Station {i+1}" for i in range(data.shape[1] - 1)]
    data["DateTime"] = pd.to_datetime(data["DateTime"])
    return data

def plot_petrol_prices(
    data: pd.DataFrame,
    start_time: Optional[Union[str, datetime]] = None,
    end_time: Optional[Union[str, datetime]] = None
) -> Figure:
    """
    Create a box plot of petrol prices over time

    Args:
        data: DataFrame containing petrol price data
        start_time: Start time for filtering data (ISO format string or datetime object)
        end_time: End time for filtering data (ISO format string or datetime object)

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

    # Create the box plot
    fig = px.box(
        melted_data,
        x="DateTime",
        y="Price",
        title="Petrol Prices Over Time (Per Timestamp)",
        labels={"DateTime": "Date/Time", "Price": "Price (cents)"}
    )

    # Update x-axis to show only the actual timestamps
    fig.update_xaxes(
        type='category',  # This makes it categorical instead of continuous
        tickangle=45,     # Rotate labels for better readability
        tickformat="%Y-%m-%d %H:%M"
    )
    return fig

# For web usage, you can create a function that handles the web interface
def create_web_plot(start_time_str: Optional[str] = None, end_time_str: Optional[str] = None) -> Figure:
    """
    Create plot for web display with optional time filtering

    Args:
        start_time_str: Start time in ISO format (YYYY-MM-DDTHH:MM:SS)
        end_time_str: End time in ISO format (YYYY-MM-DDTHH:MM:SS)

    Returns:
        Plotly Figure object
    """
    # Load data
    data = load_data("petrol_prices.csv")

    # Create and return the plot
    return plot_petrol_prices(data, start_time_str, end_time_str)

# Example usage for web:
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

app = Dash(__name__)

# Calculate default dates
default_end_date = datetime.now().date()
default_start_date = (datetime.now() - timedelta(weeks=3)).date()

app.layout = html.Div([
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=default_start_date,
        end_date=default_end_date,
        start_date_placeholder_text="Start Date",
        end_date_placeholder_text="End Date",
    ),
    dcc.Graph(id='price-box-plot')
])

@app.callback(
    Output('price-box-plot', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(start_date, end_date):
    if start_date is None:
        start_date = default_start_date.isoformat()
    if end_date is None:
        end_date = default_end_date.isoformat()
    return create_web_plot(start_date, end_date)

if __name__ == '__main__':
    app.run_server(debug=True)
