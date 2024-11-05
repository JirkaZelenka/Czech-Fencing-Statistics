from datetime import datetime, timedelta
from dash.dependencies import Input, Output, State
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def register_callbacks(app,runner, data):
    
    @app.callback(
        Output('output-number_tournaments', 'children'),
        Input('refresh-data-button', 'n_clicks'),
    )
     
    def refres_number_of_tournaments(n_clicks):
        
          if n_clicks > 0:
               current_time = datetime.now()
               return f"Currently, {current_time}, there are {len(data)} records loaded."
                    
          else:
               pass
          