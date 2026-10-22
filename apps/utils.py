from datetime import datetime
import os
import json
import pandas as pd
from tqdm import tqdm
import unicodedata
import requests

from config import Config

class Utilities:
    
    def __init__(self) -> None: 
        self.cf = Config()  


    @staticmethod
    def generate_timestamp() -> str:
        current_datetime = datetime.now()
        full_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        date_to_save = current_datetime.strftime("%Y%m%d_%H%M%S")
                
        return full_datetime, date_to_save
    
    def normalize_name(self, name):
        parts = name.split()
        normalized_parts = [part.capitalize() for part in parts]
        normalized_name = " ".join(normalized_parts)
        
        return normalized_name