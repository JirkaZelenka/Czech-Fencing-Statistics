from datetime import datetime, timedelta
from dash.dependencies import Input, Output, State
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def register_callbacks(app, runner, df_clubs, df_duels, df_fencers, df_tournaments, df_tournaments_results):
    
    
    @app.callback(
        Output('fencers-table', 'data'),
        Output('output-number_fencers', 'children'),
        Input('refresh-fencers-button', 'n_clicks'),
    )
     
    def refresh_fencers(n_clicks):
                
        if n_clicks > 0:
            current_time = datetime.now()
            
            data = df_fencers
               
            data['name_url'] = data['name'].apply(lambda x: f"[{x}](https://www.czechfencing.cz/portal/tournaments/detail/606efd9e-1453-4548-8800-d2ebf708ae9c)")
               
            #data = data.sort_values(by='date')
            data = data.to_dict('records')
               
            message_count_fencers = f"Currently, {current_time}, there are {len(data)} records loaded."
               
            return data, message_count_fencers
                    
        else:
            return [], "Missing refresh"
        
    
    @app.callback(
        Output('clubs-table', 'data'),
        Output('output-number_clubs', 'children'),
        Input('refresh-clubs-button', 'n_clicks'),
    )
     
    def refresh_clubs(n_clicks):
                
        if n_clicks > 0:
            current_time = datetime.now()
            
            data = df_clubs
               
            data['name_url'] = data['name'].apply(lambda x: f"[{x}](https://www.czechfencing.cz/portal/tournaments/detail/606efd9e-1453-4548-8800-d2ebf708ae9c)")
               
            #data = data.sort_values(by='date')
            data = data.to_dict('records')
               
            message_count_clubs = f"Currently, {current_time}, there are {len(data)} records loaded."
               
            return data, message_count_clubs
                    
        else:
            return [], "Missing refresh"
    
    @app.callback(
        Output('duels-table', 'data'),
        Output('output-number_duels', 'children'),
        Input('refresh-duels-button', 'n_clicks'),
    )
     
    def refresh_duels(n_clicks):
        
        #TODO: This one needs to JOIN for FENCERs names, TOURNAMENT name, and DATE to sort
        
        if n_clicks > 0:
            current_time = datetime.now()
            
            data = df_duels
               
            data['fencer_id_url'] = data['fencer_id'].apply(lambda x: f"[{x}](https://www.czechfencing.cz/portal/tournaments/detail/606efd9e-1453-4548-8800-d2ebf708ae9c)")
               
            #data = data.sort_values(by='date')
            data = data.to_dict('records')
               
            message_count_duels = f"Currently, {current_time}, there are {len(data)} records loaded."
               
            return data, message_count_duels
                    
        else:
            return [], "Missing refresh"
        
    
    @app.callback(
        Output('tournaments_results-table', 'data'),
        Output('output-number_tournaments_results', 'children'),
        Input('refresh-tournaments_results-button', 'n_clicks'),
    )
     
    def refresh_tournaments_results(n_clicks):
        
        if n_clicks > 0:
            current_time = datetime.now()
            
            data = df_tournaments_results
               
            data['tournament_id_url'] = data['tournament_id'].apply(lambda x: f"[{x}](https://www.czechfencing.cz/portal/tournaments/detail/606efd9e-1453-4548-8800-d2ebf708ae9c)")
            data['fencer_id_url'] = data['fencer_id'].apply(lambda x: f"[{x}](https://www.czechfencing.cz/portal/tournaments/detail/606efd9e-1453-4548-8800-d2ebf708ae9c)")
               
            #data = data.sort_values(by='date')
            data = data.to_dict('records')
               
            message_count_tournaments_results = f"Currently, {current_time}, there are {len(data)} records loaded."
               
            return data, message_count_tournaments_results
                    
        else:
            return [], "Missing refresh"
          
    
    @app.callback(
        Output('tournaments-table', 'data'),
        Output('output-number_tournaments', 'children'),
        Input('refresh-tournaments-button', 'n_clicks'),
    )
     
    def refresh_tournaments(n_clicks):
        
        if n_clicks > 0:
            current_time = datetime.now()
            
            data = df_tournaments
               
            data['name_url'] = data['name'].apply(lambda x: f"[{x}](https://www.czechfencing.cz/portal/tournaments/detail/606efd9e-1453-4548-8800-d2ebf708ae9c)")
               
            data = data.sort_values(by='date')
            data = data.to_dict('records')
               
            message_count_tournaments = f"Currently, {current_time}, there are {len(data)} records loaded."
               
            return data, message_count_tournaments
                    
        else:
            return [], "Missing refresh"
          