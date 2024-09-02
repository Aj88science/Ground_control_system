# Ground_control_system\\

1. Dash (by Plotly)
Description: Dash is a powerful Python framework for building analytical web applications. It is particularly suited for data scientists and engineers who are already familiar with Plotly for creating interactive plots.

Strengths: Great for complex dashboards, supports real-time updates, and integrates seamlessly with Plotly for advanced visualizations.

Usage: Suitable for building dashboards that require intricate plots and real-time updates.

Explanation:
Dash Initialization:

The Dash app is initialized at the start.
Data Storage:

The lists temp, alt, pres, and time_values are used to store temperature, altitude, pressure, and time values, respectively.
Layout:

The layout consists of multiple Div containers that hold the metrics, graphs, and other text elements. The dcc.Interval component triggers updates at regular intervals (every 100 ms in this case).
Callbacks:

The callback function updates the displayed metrics and plots based on the simulated data retrieved from the get_data() function.
It updates the metrics like temperature, altitude, pressure, time elapsed, velocity, and maximum height, and refreshes the graphs.
Graphing:

Plotly's go.Scatter is used to create line graphs for temperature, altitude, and pressure over time.
Running the App:

The app is run using app.run_server(debug=True).
