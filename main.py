import os
import warnings

from apps.layout import create_layout, create_intro_layout, create_people_layout, create_medals_layout, \
                    create_clubs_layout, create_duels_layout, create_predictions_layout, create_tournaments_layout
from apps.callbacks import register_callbacks
import dash
import dash_auth

from apps.run import Runner

from dotenv import load_dotenv
load_dotenv()
username = os.getenv("APP_USERNAME")
password = os.getenv("APP_PASSWORD")

VALID_USERNAME_PASSWORD_PAIRS = {
    username: password
    }

runner = Runner()
data = runner.data_manager.get_all_tournament_results()
print(f"LOADED DATA of TOURNAMENTS: {len(data)}")

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
    elif pathname == '/predictions':
        return create_predictions_layout()
    elif pathname == '/tournaments':
        return create_tournaments_layout()

register_callbacks(app, runner, data) # runner can be part of it

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8052)
