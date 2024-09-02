import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random
import time as t

# Initialize the Dash app
app = dash.Dash(__name__)

# Initialize data storage
temp, alt, pres, time_values = [], [], [], []

# HTML text for the header
html_text = '''
    <div style="text-align:center;">
        <h1>V-SAT</h1>
        <h2>ASI2022-008</h2>
    </div>
'''

start_time = t.time()
thresh_time = 0
thresh_alt = 0

# Function to simulate data retrieval
def get_data():
    return random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000)

# App layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3("Temperature"),
            html.Div(id="temperature-display", style={"fontSize": 24}),
        ], className="three columns"),

        html.Div([
            html.H3("Altitude"),
            html.Div(id="altitude-display", style={"fontSize": 24}),
        ], className="three columns"),

        html.Div([
            html.H3("Pressure"),
            html.Div(id="pressure-display", style={"fontSize": 24}),
        ], className="three columns"),

        html.Div([
            html.H3("Time Elapsed"),
            html.Div(id="time-display", style={"fontSize": 24}),
        ], className="three columns"),
    ], className="row"),

    html.Div([
        dcc.Graph(id='temperature-graph'),
        dcc.Graph(id='altitude-graph'),
        dcc.Graph(id='pressure-graph'),
    ], className="row"),

    html.Div([
        dcc.Markdown(html_text),
        html.Div(id="velocity-display", style={"fontSize": 24, "textAlign": "center"}),
        html.Div(id="max-height-display", style={"fontSize": 24, "textAlign": "center"}),
        html.Div(id="time-text", style={"fontSize": 18, "textAlign": "center"})
    ], className="row"),

    dcc.Interval(id='interval-component', interval=100, n_intervals=0)
])

# Callback to update all displays and graphs
@app.callback(
    [Output("temperature-display", "children"),
     Output("altitude-display", "children"),
     Output("pressure-display", "children"),
     Output("time-display", "children"),
     Output("temperature-graph", "figure"),
     Output("altitude-graph", "figure"),
     Output("pressure-graph", "figure"),
     Output("velocity-display", "children"),
     Output("max-height-display", "children"),
     Output("time-text", "children")],
    Input("interval-component", "n_intervals")
)
def update_data(n):
    global thresh_time, thresh_alt

    # Simulate data retrieval
    ard_temp, ard_alt, ard_pres, ard_time = get_data()

    # Threshold logic for altitude and time
    if thresh_alt == 0 and thresh_time == 0 and ard_alt >= 800:
        thresh_time = ard_time
        thresh_alt = ard_alt
    if thresh_time != 0:
        thresh_alt += ard_alt

    # Append data to lists
    temp.append(ard_temp)
    alt.append(ard_alt)
    pres.append(ard_pres)
    time_values.append(ard_time)

    # Generate the figures for each graph
    temperature_fig = {
        "data": [go.Scatter(x=time_values, y=temp, mode="lines", name="Temperature")],
        "layout": go.Layout(xaxis={"title": "Time"}, yaxis={"title": "Temperature"})
    }

    altitude_fig = {
        "data": [go.Scatter(x=time_values, y=alt, mode="lines", name="Altitude")],
        "layout": go.Layout(xaxis={"title": "Time"}, yaxis={"title": "Altitude"})
    }

    pressure_fig = {
        "data": [go.Scatter(x=time_values, y=pres, mode="lines", name="Pressure")],
        "layout": go.Layout(xaxis={"title": "Time"}, yaxis={"title": "Pressure"})
    }

    # Calculate velocity and maximum height
    velocity = (thresh_alt / (time_values[-1] - thresh_time)) if thresh_time != 0 else 0
    max_height = max(alt)

    # Update all the metrics and displays
    return (f"{temp[-1]} °C",
            f"{alt[-1]} mts",
            f"{pres[-1]} bar",
            f"{round(((t.time() - start_time) / 60), 2)} Mins",
            temperature_fig,
            altitude_fig,
            pressure_fig,
            f"Velocity: {velocity:.2f} m/s",
            f"Maximum Height: {max_height} mts",
            t.strftime("%Y-%m-%d %H:%M:%S", t.gmtime()))

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
