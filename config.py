from dotenv import load_dotenv
import os

class Config:
    
    def __init__(self):
        load_dotenv()
        
        self.project_path = os.getenv("PROJECT_PATH") 
        self.db_name = os.getenv("DB_NAME") 


        self.table_definitions={
            "clubs": 
                    """ 
                    CREATE TABLE IF NOT EXISTS clubs (
                    id TEXT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    registration_number INTEGER NOT NULL,
                    identification_number INTEGER NOT NULL,
                    country VARCHAR(255) NOT NULL,
                    city VARCHAR(255) NOT NULL,
                    city_part VARCHAR(255) NOT NULL,
                    street VARCHAR(255) NOT NULL,
                    contact_person VARCHAR(255) NOT NULL,    
                    email VARCHAR(255) NOT NULL,
                    phone VARCHAR(255) NOT NULL,
                    website VARCHAR(255) NOT NULL,
                      
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """,
            "tournaments": 
                    """ 
                    CREATE TABLE IF NOT EXISTS tournaments (
                    id TEXT PRIMARY KEY,
                    f_id VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    season_name VARCHAR(255) NOT NULL,
                    note_url VARCHAR(255) NOT NULL,
                    proposition_url VARCHAR(255) NOT NULL,
                    group_name VARCHAR(255) NOT NULL,
                    date VARCHAR(255) NOT NULL,
                    
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """,
            "fencers": 
                    """ 
                    CREATE TABLE IF NOT EXISTS fencers (
                    id TEXT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    club_id REFERENCES clubs (id),
                    f_id VARCHAR(255) NOT NULL,
                    country VARCHAR(255) NOT NULL,
                    gender VARCHAR(255) NOT NULL,
                    birthyear INTEGER NOT NULL,
                    
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """,
            "tournament_results": 
                    """ 
                    CREATE TABLE IF NOT EXISTS tournament_results (
                    id TEXT PRIMARY KEY,
                    event_id REFERENCES events (id),
                    fencer_id REFERENCES fencers (id),
                    fencer_name_to_check VARCHAR(255) NOT NULL,
                    club_id REFERENCES clubs (id),
                    club_name_to_check VARCHAR(255) NOT NULL,
                    finished VARCHAR(255) NOT NULL,
                    first_rank INTEGER NOT NULL,
                    final_rank INTEGER NOT NULL,
                    percentile FLOAT NOT NULL,
                    victories INTEGER NOT NULL,
                    victories_perc FLOAT NOT NULL,
                    ts INTEGER NOT NULL,
                    tr INTEGER NOT NULL,
                    
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """,
            "events": 
                    """ 
                    CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    f_id VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    tournament_id REFERENCES tournaments (id),
                    date VARCHAR(255) NOT NULL,
                    age_category VARCHAR(255) NOT NULL,
                    gender VARCHAR(255) NOT NULL,
                    discipline VARCHAR(255) NOT NULL,
                    type_id VARCHAR(255) NOT NULL,
                    fencers_count INTEGER NOT NULL,
                    results_url VARCHAR(255) NOT NULL,
                    is_processed BOOLEAN NOT NULL,
                    
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """,   
            "duels": 
                    """ 
                    CREATE TABLE IF NOT EXISTS duels (
                    id TEXT PRIMARY KEY,
                    event_id REFERENCES events (id),
                    type VARCHAR(255) NOT NULL,
                    winner_id REFERENCES fencers (id),
                    loser_id REFERENCES fencers (id),
                    winner_score INTEGER NOT NULL,
                    loser_score INTEGER NOT NULL,
                    
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """
        }