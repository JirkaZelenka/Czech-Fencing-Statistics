import pandas as pd
from typing import Optional
import os
import json
from tqdm import tqdm

from apps.data_manager import DataManager
from apps.utils import Utilities
from config import Config

# from utils.logger import logger_scraping

class Runner:
    
    def __init__(self) -> None: 
        self.cf = Config()   
        self.data_manager = DataManager()
        self.utils = Utilities()
  
        
    def data_prep(self):
        
        df_clubs = self.data_manager.get_all_data("clubs")
        df_duels = self.data_manager.get_all_data("duels")
        
        #TODO: tyto obecné úpravy by mohly být jinde..ale v main taky nechci.
        df_events = self.data_manager.get_all_data("events")
        df_events['date'] = pd.to_datetime(df_events['date']).dt.strftime('%Y-%m-%d')
        
        df_fencers = self.data_manager.get_all_data("fencers")
        df_tournaments = self.data_manager.get_all_data("tournaments")
        df_tournament_results = self.data_manager.get_all_data("tournament_results")
        
        return df_clubs, df_duels, df_events, df_fencers, df_tournaments, df_tournament_results
    
    
    def df_duels_prep(self, df_duels, df_events, df_fencers, df_clubs, df_tournaments) -> pd.DataFrame:
        
        #? Extra data pro filtry na stránkách
        #? některé sloupce, jako tournament_id, beru jen kvůli dalíšmu joinu
        df = df_duels.copy()
                    
        df = pd.merge(df, df_events[['id', "name", "date", "tournament_id", "gender"]], left_on='event_id', right_on='id', how='left', suffixes=('', '_event'))
        #? musím to dělat nadvakrát, obojí, abych si pokaždý označil W a L?
        df = pd.merge(df, df_fencers[['id', "name", "club_id"]], left_on='winner_id', right_on='id', how='left', suffixes=('', '_fencer_winner'))
        df = pd.merge(df, df_fencers[['id', "name", "club_id"]], left_on='loser_id', right_on='id', how='left', suffixes=('', '_fencer_loser'))
        df = pd.merge(df, df_clubs[['id', "name"]], left_on='club_id', right_on='id', how='left', suffixes=('', '_club_winner'))
        df = pd.merge(df, df_clubs[['id', "name"]], left_on='club_id_fencer_loser', right_on='id', how='left', suffixes=('', '_club_loser'))
        #? tento vyloženě jen kvůli jménu a linku na turnaj
        df = pd.merge(df, df_tournaments[['id', 'name', "f_id"]], left_on='tournament_id', right_on='id', how='left', suffixes=('', '_tournament'))

        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

        df['tournament_url'] = df.apply(
            lambda row: f"[{row['name_tournament']}](https://www.czechfencing.cz/portal/tournaments/detail/{row['f_id']})" if pd.notna(row['f_id']) and row['f_id'] else  f"[{row['f_id']}](https://www.czechfencing.cz/)",
            axis=1
                    )
        
        return df
    
    
    def df_tournament_results_prep(self, df_tournament_results, df_events, df_tournaments) -> pd.DataFrame:
        
        #? Extra data pro filtry na stránkách
        #? některé sloupce, jako tournament_id, beru jen kvůli dalíšmu joinu
        df = df_tournament_results.copy()
                            
        df = pd.merge(df, df_events[['id', "tournament_id", "date"]], left_on='event_id', right_on='id', how='left', suffixes=('', '_event'))
        
        #? tento vyloženě jen kvůli jménu a linku na turnaj
        df = pd.merge(df, df_tournaments[['id', 'name', "f_id"]], left_on='tournament_id', right_on='id', how='left', suffixes=('', '_tournament'))

        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

        df['tournament_url'] = df.apply(
            lambda row: f"[{row['name']}](https://www.czechfencing.cz/portal/tournaments/detail/{row['f_id']})" if pd.notna(row['f_id']) and row['f_id'] else  f"[{row['f_id']}](https://www.czechfencing.cz/)",
            axis=1
                    )
        
        return df
    
