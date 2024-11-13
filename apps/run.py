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
  
        
    def something(self) -> None:
        
        pass