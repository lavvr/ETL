from abc import ABC
from typing import List

import psycopg2

from utils.logger import logger
from config import db_consts


class BaseClient(ABC):
    def __init__(self):
        self.logger = logger
        
    def read(self, *args, **kwargs):
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

    # def __init__(self, 
    #              dbname=DB_NAME,
    #              user=USER,
    #              password=PASSWORD,
    #              host=HOST,
    #              port=PORT): Либо оставить так, либо все таки через класс в конфиге, не знаю в общем
        
    def __init__(self, **connection_params: dict):
        
        self.connection_params = db_consts.db_params

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

    def read(self, query: str) -> List[str]:
        if self.connection is None:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)

                if cursor.description:
                    columns = [desc[0] for desc in cursor.description if desc[0] != "id"]
                    results = []

                    for row in cursor.fetchall():
                        results.append(row[1] + ' ' + str(row[2]))
                        self.logger.info("Query has made successfully")

                    return results, columns

                else:
                    cursor.commit()
                    return []
            
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Query execution has failed: {str(e)}")
            raise       
    
    def write(self, table: str, data: tuple) -> None:

        if not data:
            self.logger.warning("There is no data to load")
            return 0

        columns = data[1]
        columns_str = ", ".join(columns)
        placeholders= ", ".join(["%s"] * len(columns))
        

        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        # values = [tuple(item[col] for col in columns) for item in data]
        values = [tuple(row.split()) for row in data[0]]
        print(type(data), type(data[0]), values, data[0], len(data[0]))

        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(query, values)
                self.connection.commit()
                self.logger.info(f"Successfully inserted {len(values)} rows.")

        except psycopg2.Error as e:
            self.logger.error(f"Data load process has failed: {str(e)}")
            raise

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
    


 

