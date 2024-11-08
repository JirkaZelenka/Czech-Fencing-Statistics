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
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    city VARCHAR(255) NOT NULL,
                    country VARCHAR(255) NOT NULL,
                    
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """,
            "tournaments": 
                    """ 
                    CREATE TABLE IF NOT EXISTS tournaments (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    city VARCHAR(255) NOT NULL,
                    type VARCHAR(255) NOT NULL,
                    
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """,
            "fencers": 
                    """ 
                    CREATE TABLE IF NOT EXISTS fencers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    club_id REFERENCES clubs (id),
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
                    id SERIAL PRIMARY KEY,
                    event_id REFERENCES events (id),
                    fencer_id REFERENCES fencers (id),
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
                    id SERIAL PRIMARY KEY,
                    tournament_id REFERENCES tournaments (id),
                    date VARCHAR(255) NOT NULL,
                    gender VARCHAR(255) NOT NULL,
                    finished VARCHAR(255) NOT NULL,
                    
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    deleted_at datetime NOT NULL
                    ); 
                    """,   
            "duels": 
                    """ 
                    CREATE TABLE IF NOT EXISTS duels (
                    id SERIAL PRIMARY KEY,
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