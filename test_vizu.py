import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

# Sample data: level, player1, player2, result ('W' means player1 won), score
matches = [
    (8, "A", "B", "W", "15:12"),
    (8, "C", "D", "W", "18:10"),
    (8, "E", "F", "W", "20:19"),
    (8, "G", "H", "W", "22:17"),
    (4, "A", "C", "W", "16:11"),
    (4, "E", "G", "W", "21:20"),
    (2, "A", "E", "W", "19:18"),
]

# Extract all players for dropdown
all_players = sorted(set(p for match in matches for p in match[1:3]))

# Generate coordinates for plotting
def generate_layout(matches):
    coords = {}
    level_counts = {}
    for level, p1, p2, result, score in matches:
        level_counts.setdefault(level, 0)
        y = level_counts[level]
        x = level
        coords[(p1, level)] = (x, y * 2)
        coords[(p2, level)] = (x, y * 2 + 1)
        level_counts[level] += 1
    return coords

# Build the figure
def build_figure(matches, highlight_player=None):
    coords = generate_layout(matches)
    fig = go.Figure()
    highlighted_edges = []

    score_annotations = {}

    for level, p1, p2, result, score in matches:
        x1, y1 = coords[(p1, level)]
        x2, y2 = coords[(p2, level)]

        winner = p1 if result == 'W' else p2
        next_level = level // 2
        x_mid = next_level
        y_mid = (y1 + y2) / 2

        coords[(winner, next_level)] = (x_mid, y_mid)
        score_annotations[(winner, next_level)] = score

        line_color = 'red' if highlight_player in [p1, p2, winner] else 'gray'

        if next_level >= 1:
            fig.add_trace(go.Scatter(
                x=[x1, x_mid], y=[y1, y_mid], mode='lines', line=dict(color=line_color), showlegend=False,
                hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=[x2, x_mid], y=[y2, y_mid], mode='lines', line=dict(color=line_color), showlegend=False,
                hoverinfo='skip'
            ))

        # Add player nodes
        for player, x, y in [(p1, x1, y1), (p2, x2, y2)]:
            fig.add_trace(go.Scatter(
                x=[x], y=[y], text=[player], mode='markers+text', textposition="middle right",
                marker=dict(color='red' if highlight_player == player else 'blue', size=10),
                hovertext=f"Score: {score}", hoverinfo='text',
                customdata=[player],
                showlegend=False
            ))

    # Draw final winner node if exists and place score
    for (player, level), (x, y) in coords.items():
        if level == 1:
            fig.add_trace(go.Scatter(
                x=[x], y=[y], text=[player], mode='markers+text', textposition="middle right",
                marker=dict(color='red' if highlight_player == player else 'blue', size=12),
                hoverinfo='text',
                customdata=[player],
                showlegend=False
            ))
        if (player, level) in score_annotations:
            fig.add_trace(go.Scatter(
                x=[x], y=[y - 0.3], text=[score_annotations[(player, level)]], mode='text', textposition="bottom center",
                showlegend=False, hoverinfo='skip'
            ))

    fig.update_layout(
        clickmode='event+select',
        xaxis=dict(title='Level', autorange='reversed'),
        yaxis=dict(showgrid=False, showticklabels=False),
        margin=dict(l=20, r=20, t=20, b=20),
        height=600
    )
    return fig

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='player-search',
        options=[{'label': p, 'value': p} for p in all_players],
        placeholder='Search player...',
        searchable=True,
        style={'width': '300px'}
    ),
    dcc.Graph(id='bracket-graph', figure=build_figure(matches))
])

@app.callback(
    Output('bracket-graph', 'figure'),
    [Input('player-search', 'value'),
     Input('bracket-graph', 'clickData')],
    [State('player-search', 'value')]
)
def update_figure(player_name, click_data, dropdown_value):
    # Prioritize dropdown if selected
    if player_name:
        return build_figure(matches, highlight_player=player_name)
    elif click_data and click_data['points']:
        clicked_name = click_data['points'][0]['customdata']
        return build_figure(matches, highlight_player=clicked_name)
    return build_figure(matches)

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8053)
