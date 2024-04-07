
# ! This one is showing dependent dropdowns

# Import packages
from dash import Dash, html, dcc, callback_context, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

options = [
    {"label": "New York City", "value": "NYC"},
    {"label": "Montreal", "value": "MTL"},
    {"label": "San Francisco", "value": "SF"},
]

cities = {
    "NYC": ["Brooklyn", "Queens", "Manhattan"],
    "MTL": ["Plateau", "Downtown", "Old Montreal"],
    "SF": ["Mission", "Castro", "SOMA"]
}


app.layout = html.Div([
    html.Div([
        "Single dynamic Dropdown",
        dcc.Dropdown(id="my-dynamic-dropdown", options=options)
    ]),
    html.Div([
        "Multi dynamic Dropdown",
        dcc.Dropdown(
            id="my-multi-dynamic-dropdown", 
            multi=True,
            options=[{"label": "All", "value": "all"}] + [{"label": city, "value": city} for city in set(sum(cities.values(), []))]
        )
    ]),
])

@app.callback(
    Output("my-multi-dynamic-dropdown", "value"),
    [Input("my-multi-dynamic-dropdown", "options")]
)
def select_all(options):
    return ["all"] if "all" in [opt["value"] for opt in options] else []

@app.callback(
    Output("my-multi-dynamic-dropdown", "options"),
    [Input("my-dynamic-dropdown", "value")]
)
def update_multi_options(selected_city):
    if not selected_city:
        return []
    return [{"label": "All", "value": "all"}] + [{"label": city, "value": city} for city in cities[selected_city]]

if __name__ == '__main__':
    app.run(debug=True, port = 8052)


