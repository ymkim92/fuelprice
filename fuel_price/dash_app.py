"""
Usage guide for the boxplot_with_dash.py script:

```bash
# Basic Usage
python boxplot_with_dash.py path/to/your/fuel_prices.csv
```
Example usage description:

```text
This script creates an interactive web dashboard to visualize fuel prices using box plots.

Input CSV file:
- CSV file with fuel price data (first column should be datetime, subsequent columns should be
  fuel prices)


Example csv file format:
```
2024-11-22T08:00:05,160.9,161.9,163.9,165.9,169.9,170.5,172.9,172.9,172.9,172.9,172.9,172.9,172.9,172.9,173.9,173.9,173.9,173.9,173.9,173.9
2024-11-22T12:00:04,160.9,161.9,163.9,165.9,169.9,169.9,170.5,170.9,170.9,172.9,172.9,172.9,172.9,172.9,172.9,173.9,173.9,173.9,173.9,173.9
2024-11-22T16:00:04,160.9,161.9,163.9,165.9,165.9,169.9,169.9,169.9,169.9,169.9,169.9,170.5,170.9,170.9,172.4,172.4,172.9,172.9,173.9,173.9
2024-11-23T08:00:02,160.9,161.9,163.9,165.9,165.9,169.9,169.9,169.9,169.9,169.9,169.9,169.9,170.5,170.9,170.9,172.4,172.4,172.9,173.9,173.9
```

The file above can be collected by the `racq_fuel_price` command with `-o raw` option.

"""

import argparse
from datetime import datetime, timedelta
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from fuel_price.boxplot_with_dash import create_web_plot

def main():
    parser = argparse.ArgumentParser(description="Fuel Price Box Plot")
    parser.add_argument("csv_file", type=str, help="Path to the CSV file containing fuel price data")
    args = parser.parse_args()

    app = Dash(__name__)

    # Calculate default dates
    default_end_date = datetime.now().date()
    default_start_date = (datetime.now() - timedelta(weeks=3)).date()

    app.layout = html.Div(
        [
            dcc.DatePickerRange(
                id="date-picker-range",
                start_date=default_start_date,
                end_date=default_end_date,
                start_date_placeholder_text="Start Date",
                end_date_placeholder_text="End Date",
            ),
            dcc.Graph(id="price-box-plot"),
        ]
    )

    @app.callback(
        Output("price-box-plot", "figure"),
        [Input("date-picker-range", "start_date"), Input("date-picker-range", "end_date")],
    )
    def update_graph(start_date, end_date):
        if start_date is None:
            start_date = default_start_date.isoformat()
        if end_date is None:
            end_date = default_end_date.isoformat()
        return create_web_plot(args.csv_file, start_date, end_date)

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
