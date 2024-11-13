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
        
    def clear_table(self, table_name):
        
        with self._get_connection() as conn: 
            try:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {table_name}")
                conn.commit()
                cursor.close()
            except sqlite3.Error as e:
                print(f'Error clearing table {table_name}: {e}') 
                conn.rollback()
                    
                    
    def drop_table(self, table_name):
        
        with self._get_connection() as conn: 
            try:
                cursor = conn.cursor()
                cursor.execute(f"DROP table {table_name}")
                conn.commit()
                cursor.close()
            except sqlite3.Error as e:
                print(f'Error dropping table {table_name}: {e}') 
                conn.rollback()
                       
                       
    def create_table(self, table_name):
        
        with self._get_connection() as conn: 
        
            table = self.cf.table_definitions[table_name]
            try:
                cursor = conn.cursor()
                cursor.execute(table)
                conn.commit()
                cursor.close()
            except sqlite3.Error as e:
                print(f'Error creating table {table_name}: {e}') 
                conn.rollback()
                         

    def get_all_data(self, table_name):
        
        with self._get_connection() as conn:        
            try:
                query = f"SELECT * FROM {table_name}"
            
                return pd.read_sql_query(query, conn)
            
            except sqlite3.Error as e:
                print(f'Error loading rows from table {table_name}: {e}') 
                conn.rollback()
                
    def insert_new_club(self, table_name, df):
        
        with self._get_connection() as conn:  
            try:
                cursor = conn.cursor()
                
                data_to_upload = []
                for i in range(len(df)):
                    r = df.iloc[i]
                    data_to_upload.append([
                        str(r['id']),
                        str(r['name']),
                        str(r['registration_number']),
                        str(r['identification_number']),
                        str(r['country']),
                        str(r['city']),
                        str(r['city_part']),
                        str(r['street']),
                        str(r['contact_person']),
                        str(r['email']),
                        str(r['phone']),
                        str(r['website']),
                        str(r['created_at']),
                        str(r['updated_at']),
                        str(r['deleted_at']),
                        ])
                print(data_to_upload)

                query = f"""
                        INSERT INTO {table_name} (
                        id, name, registration_number, identification_number,  
                        country, city, city_part, street, contact_person, 
                        email, phone, website, created_at, updated_at, deleted_at)
                        
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ? )
                        """             
                cursor.executemany(query, data_to_upload)
                conn.commit()

            except sqlite3.Error as e:
                print(f'Error inserting offer: {e}')        
                conn.rollback()     
                
    def insert_new_fencer(self, table_name, df):
        
        with self._get_connection() as conn:  
            try:
                cursor = conn.cursor()
                
                data_to_upload = []
                for i in range(len(df)):
                    r = df.iloc[i]
                    data_to_upload.append([
                        str(r['id']),
                        str(r['name']),
                        str(r['club_id']),
                        str(r['f_id']),
                        str(r['country']),
                        str(r['gender']),
                        str(r['birthyear']),
                        str(r['created_at']),
                        str(r['updated_at']),
                        str(r['deleted_at']),
                        ])
                print(data_to_upload)

                query = f"""
                        INSERT INTO {table_name} (
                        id, name, club_id, f_id, country, gender, birthyear,
                        created_at, updated_at, deleted_at)
                        
                        VALUES (?, ?, ?, ?, ?,
                                ?, ?, ?, ?, ?)
                        """             
                cursor.executemany(query, data_to_upload)
                conn.commit()

            except sqlite3.Error as e:
                print(f'Error inserting offer: {e}')        
                conn.rollback()    
                
    
    def insert_new_tournament(self, table_name, df):
        
        with self._get_connection() as conn:  
            try:
                cursor = conn.cursor()
                
                data_to_upload = []
                for i in range(len(df)):
                    r = df.iloc[i]
                    data_to_upload.append([
                        str(r['id']),
                        str(r['f_id']),
                        str(r['name']),
                        str(r['season_name']),
                        str(r['note_url']),
                        str(r['proposition_url']),
                        str(r['group_name']),
                        str(r['date']),
                        
                        str(r['created_at']),
                        str(r['updated_at']),
                        str(r['deleted_at']),
                        ])
                print(data_to_upload)

                query = f"""
                        INSERT INTO {table_name} (
                        id, f_id, name, season_name, note_url, 
                        proposition_url, group_name, date,
                        created_at, updated_at, deleted_at)
                        
                        VALUES (?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?)
                        """             
                cursor.executemany(query, data_to_upload)
                conn.commit()

            except sqlite3.Error as e:
                print(f'Error inserting offer: {e}')        
                conn.rollback()     
                
                
    def insert_new_event(self, table_name, df):
        
        with self._get_connection() as conn:  
            try:
                cursor = conn.cursor()
                
                data_to_upload = []
                for i in range(len(df)):
                    r = df.iloc[i]
                    data_to_upload.append([
                        str(r['id']),
                        str(r['f_id']),
                        str(r['name']),
                        str(r['tournament_id']),
                        str(r['date']),
                        str(r['age_category']),
                        str(r['gender']),
                        str(r['discipline']),
                        str(r['type_id']),
                        str(r['fencers_count']),
                        str(r['results_url']),
                        str(r['is_processed']),
                        
                        str(r['created_at']),
                        str(r['updated_at']),
                        str(r['deleted_at']),
                        ])
                print(data_to_upload)

                query = f"""
                        INSERT INTO {table_name} (
                        id, f_id, name, tournament_id, date, age_category, 
                        gender, discipline, type_id, fencers_count, results_url, is_processed,
                        created_at, updated_at, deleted_at)
                        
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                                ?, ?, ?, ?, ?, ?, ?)
                        """             
                cursor.executemany(query, data_to_upload)
                conn.commit()

            except sqlite3.Error as e:
                print(f'Error inserting offer: {e}')        
                conn.rollback()     
      
                
    def insert_new_result(self, table_name, df):
        
        with self._get_connection() as conn:  
            try:
                cursor = conn.cursor()
                
                data_to_upload = []
                for i in range(len(df)):
                    r = df.iloc[i]
                    data_to_upload.append([
                        str(r['id']),
                        str(r['event_id']),
                        str(r['fencer_id']),
                        str(r['fencer_name_to_check']),
                        str(r['club_id']),
                        str(r['club_name_to_check']),
                        str(r['finished']),
                        str(r['first_Rank']),
                        str(r['final_rank']),
                        str(r['percentile']),
                        str(r['victories']),
                        str(r['victories_perc']),
                        str(r['ts']),
                        str(r['tr']),
                    
                        str(r['created_at']),
                        str(r['updated_at']),
                        str(r['deleted_at']),
                        ])
                print(data_to_upload)

                query = f"""
                        INSERT INTO {table_name} (
                        id, event_id, fencer_id, fencer_name_to_check, club_id, club_name_to_check,
                        finished, first_Rank, final_rank,
                        percentile, victories, victories_perc, ts, tr,
                        created_at, updated_at, deleted_at)
                        
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,
                                ?, ?, ?, ?, ?, ?, ?, ?)
                        """             
                cursor.executemany(query, data_to_upload)
                conn.commit()

            except sqlite3.Error as e:
                print(f'Error inserting offer: {e}')        
                conn.rollback()     
                
                