from dotenv import load_dotenv
import os

class Config:
    
    def __init__(self):
        load_dotenv()
        
        self.project_path = os.getenv("PROJECT_PATH") 
        self.db_name = os.getenv("DB_NAME") 
