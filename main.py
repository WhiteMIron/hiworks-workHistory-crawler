from hiworks_crawler import hiworks_crawler
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    id = os.environ.get('id')
    password = os.environ.get('password')
    
    hiworks_crawler(id, password)