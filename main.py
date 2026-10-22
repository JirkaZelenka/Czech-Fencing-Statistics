import os
import warnings
import pandas as pd

from apps.layout import create_layout, create_intro_layout, create_people_layout, create_medals_layout, \
                    create_clubs_layout, create_duels_layout, create_eliminations_layout, \
                     create_tournament_results_layout, create_tournaments_layout, create_personal_stats_layout
from apps.callbacks import register_callbacks
import dash
import dash_auth
from dash.dependencies import Input, Output, State

# import plotly.graph_objects as go

from apps.run import Runner

from dotenv import load_dotenv
load_dotenv()
username = os.getenv("APP_USERNAME")
password = os.getenv("APP_PASSWORD")

VALID_USERNAME_PASSWORD_PAIRS = {
    username: password
    }

runner = Runner()

# Load V1 data (Database)
print("Loading V1 data from database...")
df_clubs_v1, df_duels_v1, df_events_v1, df_fencers_v1, df_tournaments_v1, df_tournament_results_v1 = runner.data_prep()

#? combined DFs including extra info for filtering
df_duels_prep_v1 = runner.df_duels_prep(df_duels_v1, df_events_v1, df_fencers_v1, df_clubs_v1, df_tournaments_v1)
df_tournament_results_prep_v1 = runner.df_tournament_results_prep(df_tournament_results_v1, df_events_v1, df_tournaments_v1)

print(f"V1 - LOADED DATA of CLUBS: {len(df_clubs_v1)}")
print(f"V1 - LOADED DATA of DUELS: {len(df_duels_v1)}")
print(f"V1 - LOADED DATA of EVENTS: {len(df_events_v1)}")
print(f"V1 - LOADED DATA of FENCERS: {len(df_fencers_v1)}")
print(f"V1 - LOADED DATA of TOURNAMENTS: {len(df_tournaments_v1)}")
print(f"V1 - LOADED DATA of TOURNAMENTS RESULTS: {len(df_tournament_results_v1)}")

# Load V2 data (Excel files)
print("\nLoading V2 data from Excel files...")
try:
    excel_dir = os.getenv("EXCEL_DATA_DIR", "C:\\Users\\jirka\\Downloads")
    df_clubs_v2, df_duels_v2, df_events_v2, df_fencers_v2, df_tournaments_v2, df_tournament_results_v2 = runner.data_prep_v2(excel_dir)
    
    #? combined DFs including extra info for filtering
    df_duels_prep_v2 = runner.df_duels_prep_v2(df_duels_v2, df_events_v2, df_fencers_v2, df_clubs_v2, df_tournaments_v2)
    df_tournament_results_prep_v2 = runner.df_tournament_results_prep_v2(df_tournament_results_v2, df_events_v2, df_tournaments_v2)
    
    print(f"V2 - LOADED DATA of CLUBS: {len(df_clubs_v2)}")
    print(f"V2 - LOADED DATA of DUELS: {len(df_duels_v2)}")
    print(f"V2 - LOADED DATA of EVENTS: {len(df_events_v2)}")
    print(f"V2 - LOADED DATA of FENCERS: {len(df_fencers_v2)}")
    print(f"V2 - LOADED DATA of TOURNAMENTS: {len(df_tournaments_v2)}")
    print(f"V2 - LOADED DATA of TOURNAMENTS RESULTS: {len(df_tournament_results_v2)}")
except Exception as e:
    print(f"Warning: Could not load V2 data: {e}")
    print("V2 features will be limited. Creating empty dataframes...")
    df_clubs_v2 = pd.DataFrame()
    df_duels_v2 = pd.DataFrame()
    df_events_v2 = pd.DataFrame()
    df_fencers_v2 = pd.DataFrame()
    df_tournaments_v2 = pd.DataFrame()
    df_tournament_results_v2 = pd.DataFrame()
    df_duels_prep_v2 = pd.DataFrame()
    df_tournament_results_prep_v2 = pd.DataFrame()

# Default to V1
df_clubs = df_clubs_v1
df_duels = df_duels_v1
df_events = df_events_v1
df_fencers = df_fencers_v1
df_tournaments = df_tournaments_v1
df_tournament_results = df_tournament_results_v1
df_duels_prep = df_duels_prep_v1
df_tournament_results_prep = df_tournament_results_prep_v1

app = dash.Dash(__name__, suppress_callback_exceptions=True)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS,
    secret_key="Whatever_makes_the_dash_happy!123",
)

app.layout = create_layout()

# Version switching callback
@app.callback(
    Output('app-version', 'data'),
    Output('version-v1-btn', 'style'),
    Output('version-v2-btn', 'style'),
    Input('version-v1-btn', 'n_clicks'),
    Input('version-v2-btn', 'n_clicks'),
    State('app-version', 'data'),
    prevent_initial_call=True
)
def switch_version(v1_clicks, v2_clicks, current_version):
    from apps.layout import MODERN_COLORS, get_modern_button_style
    
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_version, dash.no_update, dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'version-v1-btn':
        new_version = 'v1'
        v1_style = {**get_modern_button_style(), 'padding': '6px 12px', 'fontSize': '12px', 'marginRight': '5px', 'backgroundColor': MODERN_COLORS['secondary']}
        v2_style = {**get_modern_button_style(), 'padding': '6px 12px', 'fontSize': '12px', 'backgroundColor': MODERN_COLORS['gray_medium']}
    else:
        new_version = 'v2'
        v1_style = {**get_modern_button_style(), 'padding': '6px 12px', 'fontSize': '12px', 'marginRight': '5px', 'backgroundColor': MODERN_COLORS['gray_medium']}
        v2_style = {**get_modern_button_style(), 'padding': '6px 12px', 'fontSize': '12px', 'backgroundColor': MODERN_COLORS['secondary']}
    
    return new_version, v1_style, v2_style

# Update navigation styles based on version
@app.callback(
    Output('nav-clubs', 'style'),
    Output('nav-people', 'style'),
    Input('app-version', 'data')
)
def update_nav_styles(version):
    from apps.layout import MODERN_COLORS
    
    nav_link_style = {
        'color': MODERN_COLORS['white'],
        'fontSize': '15px',
        'fontWeight': '500',
        'textDecoration': 'none',
        'padding': '8px 16px',
        'borderRadius': '6px',
        'transition': 'all 0.3s ease',
        'margin': '0 4px'
    }
    
    nav_link_style_unavailable = {
        **nav_link_style,
        'color': MODERN_COLORS['warning'],
        'opacity': '0.7',
        'fontStyle': 'italic'
    }
    
    if version == 'v2':
        return nav_link_style_unavailable, nav_link_style_unavailable
    else:
        return {**nav_link_style, 'fontWeight': '600'}, {**nav_link_style, 'fontWeight': '600'}

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    dash.dependencies.Input('url', 'pathname'),
    dash.dependencies.Input('app-version', 'data')
)
def display_page(pathname, version):
    # Select data based on version
    if version == 'v2':
        current_duels = df_duels_v2
        current_duels_prep = df_duels_prep_v2
    else:
        current_duels = df_duels_v1
        current_duels_prep = df_duels_prep_v1
    
    if pathname == '/intro':
        return create_intro_layout()
    elif pathname == '/people':
        return create_people_layout()
    elif pathname == '/medals':
        return create_medals_layout()
    elif pathname == '/clubs':
        return create_clubs_layout()
    elif pathname == '/duels':
        return create_duels_layout() 
    elif pathname == '/eliminations':
        return create_eliminations_layout(current_duels) #? this one needs it for setup
    elif pathname == '/tournament_results':
        return create_tournament_results_layout()
    elif pathname == '/tournaments':
        return create_tournaments_layout()
    elif pathname == '/personal_stats':
        return create_personal_stats_layout(current_duels_prep) #? this is for picklist of fencers

# Register callbacks with both V1 and V2 data
register_callbacks(app, runner, 
                   df_clubs_v1, df_duels_v1, df_events_v1, df_fencers_v1, df_tournaments_v1, df_tournament_results_v1,
                   df_duels_prep_v1, df_tournament_results_prep_v1,
                   df_clubs_v2, df_duels_v2, df_events_v2, df_fencers_v2, df_tournaments_v2, df_tournament_results_v2,
                   df_duels_prep_v2, df_tournament_results_prep_v2) #? prep data předpočítaná předem

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8052)
