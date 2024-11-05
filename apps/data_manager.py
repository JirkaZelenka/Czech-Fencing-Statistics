import pandas as pd
from tqdm import tqdm
import sqlite3

from config import Config 

#from utils.logger import logger_scraping

class DataManager:
    
    def __init__(self) -> None: 
        self.cf = Config()      
        
    def _get_connection(self):
        
        try:
            conn = sqlite3.connect(f"{self.cf.project_path}/{self.cf.db_name}")
            return conn
        except sqlite3.Error as e:
            print(f'Error connecting to database: {e}') 

            return None

    def get_all_tournament_results(self, table_name="tournament_results"):
        
        with self._get_connection() as conn:        
            try:
                query = f"SELECT * FROM {table_name}"
            
                return pd.read_sql_query(query, conn)
            
            except sqlite3.Error as e:
                print(f'Error loading rows from table {table_name}: {e}') 
                conn.rollback()