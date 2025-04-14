from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
import sqlite3
from pathlib import Path
import streamlit as st

class DatabaseManager:
    SQLITE = "SQLITE_CONNECTION"
    MYSQL = "MYSQL_CONNECTION"
    
    def __init__(self):
        self.connection = None
        self.db_type = None
    
    @staticmethod
    @st.cache_resource(ttl="2h")
    def connect_sqlite(db_path):
        print(f"Connecting to SQLite database at: {db_path}")
        db_creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=db_creator))
    
    @staticmethod
    @st.cache_resource(ttl="2h")
    def connect_mysql(host, user, password, db_name):
        if not all([host, user, password, db_name]):
            raise ValueError("All MySQL connection parameters are required")
            
        connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"
        return SQLDatabase(create_engine(connection_string))
    
    def get_connection(self, db_type, **kwargs):
        self.db_type = db_type
        
        if db_type == self.SQLITE:
            parent_dir = Path(__file__).parent
            db_path = kwargs.get('db_path', parent_dir / "company.db")
            self.connection = self.connect_sqlite(db_path)
            
        elif db_type == self.MYSQL:
            self.connection = self.connect_mysql(
                kwargs.get('host'),
                kwargs.get('user'),
                kwargs.get('password'),
                kwargs.get('db_name')
            )
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
            
        return self.connection