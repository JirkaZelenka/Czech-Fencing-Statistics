import pandas as pd
from typing import Optional
import os
import json
from tqdm import tqdm

import re
import requests
from bs4 import BeautifulSoup

class DataGetting:
    """This class
    """
    
    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir
        self.base_url = "https://www.fencingtimelive.com/tournaments/search/data/advanced"
        
        
    def read_excel_file(self, file_name: str) -> pd.DataFrame:
        file_path = os.path.join(self.data_dir, file_name)
        df = pd.read_excel(file_path)
        return df
    
    def save_excel_file(self, df: pd.DataFrame, file_name: str) -> None:
        file_path = os.path.join(self.data_dir, file_name)
        df.to_excel(file_path, index=False)
                
    def get_events_df(self, date_from, date_to, country_code) -> pd.DataFrame:
       
        results = []
        url = f"{self.base_url}?country={country_code}&from={date_from}&to={date_to}"
       
        events = requests.get(url)
        if events.status_code == 200:
            events_json = events.json()
            print(f"Found {len(events_json)} events between {date_from} and {date_to}.")

        for event in tqdm(events_json):
            results.append([event["id"], event["name"], event["dates"]])
            
        events_df = pd.DataFrame(results, columns=["event_id", "event_name", "date"])
        return events_df
    
    #TODO: TBD ... now it is a part of the jup notebook