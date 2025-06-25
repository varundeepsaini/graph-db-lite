import os
from dotenv import load_dotenv

load_dotenv()

def get_save_file_path() -> str:
    return os.getenv('SAVE_FILE_PATH', '/Users/graphs.json') 