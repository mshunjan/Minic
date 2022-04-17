from pydantic import BaseSettings
from functools import lru_cache
import os 

class Settings(BaseSettings):
    
    # -- App Data --
    DATA: str = './data'
    UPLOADS: str = DATA + '/uploads'
    RESULTS: str = DATA + '/results'

    MPA_DB: str = './metaphlan_db'

    for directory in [DATA, UPLOADS, RESULTS, MPA_DB]:
        if not os.path.isdir(directory):
            os.mkdir(directory)

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()