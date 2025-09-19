from abc import ABC
from typing import List

import psycopg2

from utils.logger import logger
from config import DB_NAME, USER, PASSWORD, HOST, PORT

class BaseClient(ABC):
    def read(self, *args):
        pass

    def write(self, *args):
        pass

class FileClient(BaseClient):
    def __init__(self):
        self.logger = logger

    def read(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()

    def write(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(data)

class DatabaseClient(BaseClient):

    def __init__(self, 
                 dbname=DB_NAME,
                 user=USER,
                 password=PASSWORD,
                 host=HOST,
                 port=PORT):
        
        self.connection_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }

        self.connection = None
        self.logger = logger

    def connect(self) -> None:
        
        try:

            self.connection = psycopg2.connect(**self.connection_params)

        except Exception as e:
            logger.error('Cannot connect to database')
            raise
    
    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            self.logger.info("Connection has been closed")

    def execute(self, query: str) -> List[str]:
        if self.connection is None:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)

                if cursor.description:
                    columns = [desc[0] for desc in cursor.description if desc[0] != "id"]
                    results = []

                    for row in cursor.fetchall():
                        results.append(', '.join([row[1] + ' ' + str(row[2])]))
                        self.logger.info("Query has made successfully")

                    return results, columns

                else:
                    cursor.commit()
                    return []
            
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Query execution has failed: {str(e)}")
            raise       
    
    def load_data(self, table: str, data: tuple) -> None:

        if not data:
            self.logger.warning("There is no data to load")
            return 0

        columns = data[0]
        columns_str = ", ".join(columns)
        placeholders= ", ".join(["%s"] * len(columns))
        

        query = f"INSERT INTO {table} COLUMNS ({columns_str}) VALUES ({placeholders})"
        # values = [tuple(item[col] for col in columns) for item in data]
        values = data[1]

        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(query, values)
                self.connection.commit()
                self.logger.info(f"Successfully inserted {len(data)} rows.")

        except psycopg2.Error as e:
            self.logger.error(f"Data load process has failed: {str(e)}")
            raise

    
    # def update_data(self, query:str, params:=None):
    
    #     self.logger.info(f"Updating data with query: {query}")
        
    #     if self.connection is None:
    #         self.connect()
        
    #     try:
    #         with self.connection.cursor() as cursor:
    #             cursor.execute(query, params)
    #             self.connection.commit()
    #             updated_count = cursor.rowcount
    #             self.logger.info(f"Updated {updated_count} rows")
    #             return updated_count
    #     except psycopg2.Error as e:
    #         self.connection.rollback()
    #         self.logger.error(f"Data update failed: {str(e)}", exc_info=True)
    #         raise
    
    def create_table(self, table_name: str, schema: str) -> None:
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        self.logger.info(f"Creating table {table_name}")
        self.execute(query)

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self):
        self.disconnect()
        return self
    


 

