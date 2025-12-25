import os
import warnings

from apps.layout import create_layout, create_intro_layout, create_people_layout, create_medals_layout, \
                    create_clubs_layout, create_duels_layout, create_eliminations_layout, \
                     create_tournament_results_layout, create_tournaments_layout, create_personal_stats_layout
from apps.callbacks import register_callbacks
import dash
import dash_auth

# import plotly.graph_objects as go

# import pandas as pd

from apps.run import Runner

from dotenv import load_dotenv
load_dotenv()
username = os.getenv("APP_USERNAME")
password = os.getenv("APP_PASSWORD")

VALID_USERNAME_PASSWORD_PAIRS = {
    username: password
    }

runner = Runner()

df_clubs, df_duels, df_events, df_fencers, df_tournaments, df_tournament_results = runner.data_prep()

#? combined DFs including extra info for filtering
df_duels_prep = runner.df_duels_prep(df_duels, df_events, df_fencers, df_clubs, df_tournaments)
df_tournament_results_prep = runner.df_tournament_results_prep(df_tournament_results, df_events, df_tournaments)

# print(df_duels_prep["name_fencer_winner"].unique())
# print(df_duels_prep["name_fencer_loser"].unique())

print(f"LOADED DATA of CLUBS: {len(df_clubs)}")
print(f"LOADED DATA of DUELS: {len(df_duels)}")
print(f"LOADED DATA of EVENTS: {len(df_events)}")
print(f"LOADED DATA of FENCERS: {len(df_fencers)}")
print(f"LOADED DATA of TOURNAMENTS: {len(df_tournaments)}")
print(f"LOADED DATA of TOURNAMENTS RESULTS: {len(df_tournament_results)}")

app = dash.Dash(__name__, suppress_callback_exceptions=True)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS,
    secret_key="Whatever_makes_the_dash_happy!123",
)

app.layout = create_layout()

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    dash.dependencies.Input('url', 'pathname')
)
def display_page(pathname):
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
        return create_eliminations_layout(df_duels) #? this one needs it for setup
    elif pathname == '/tournament_results':
        return create_tournament_results_layout()
    elif pathname == '/tournaments':
        return create_tournaments_layout()
    elif pathname == '/personal_stats':
        return create_personal_stats_layout(df_duels_prep) #? this is for picklist of fencers

register_callbacks(app, runner, df_clubs, df_duels, df_events,
                   df_fencers, df_tournaments, df_tournament_results,
                   df_duels_prep, df_tournament_results_prep) #? prep data předpočítaná předem

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8052)
