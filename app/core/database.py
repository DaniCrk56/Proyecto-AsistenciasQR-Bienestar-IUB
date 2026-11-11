
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

    def get_connection(self):
        try:
            return psycopg2.connect(
                self.database_url,
                cursor_factory=RealDictCursor
            )
        except Exception as e:
            print(f"Error de conexión a la BD: {e}")
            return None
