from functools import lru_cache
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    
    # -- App Data --
    DATA = './data'
    UPLOADS = DATA + '/uploads'
    RESULTS = DATA + '/results'


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()