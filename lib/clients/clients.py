import psycopg2

from ..utils.logger import logger
from config import DB_NAME, USER, PASSWORD, HOST, PORT

class FileClient:
    def __init__(self):
        self.logger = logger

    def read(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    
    def write(self, filepath, data):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(data)

class DatabaseClient:

    def __init__(self, 
                 dbname=DB_NAME,
                 usr=USER,
                 password=PASSWORD,
                 host=HOST,
                 port=PORT):
        
        self.connection_params = {
            'dbname': dbname,
            'usr': usr,
            'password': password,
            'host': host,
            'port': port
        }

        self.connection = None
        self.logger = logger

    def connect(self):
        
        try:

            self.connection = psycopg2.connect(**self.connection_params)

        except Exception as e:
            logger.error('Cannot connect to database')
            raise
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.logger.info("Connection has been closed")

    def execute(self, query):
        if self.connection is None:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)

            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                results = []

                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                    self.logger.info("Query has made successfully")

                return results

            else:
                cursor.commit()
                return []
            
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Query execution has failed: {str(e)}", exc_info=True)
            raise       
    
    def load_data(self, table, data):

        if not data:
            self.logger.warning("There is no data to load")
            return 0

        columns = list(data[0].keys())
        columns_str = ", ".join(columns)
        placeholders= ", ".join(["%s"] * len(columns))

        query = f"INSERT INTO {table} COLUMNS ({columns_str}) VALUES ({placeholders})"
        values = [tuple(item[col] for col in columns) for item in data]

        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(query, values)
                self.connection.commit()
                self.logger.info(f"Successfully inserted {len(data)} rows.")

        except psycopg2.Error as e:
            self.logger.error(f"Data load process has failed: {str(e)}", exc_info=True)
            raise

    
    def update_data(self, query, params=None):
    
        self.logger.info(f"Updating data with query: {query}")
        
        if self.connection is None:
            self.connect()
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                updated_count = cursor.rowcount
                self.logger.info(f"Updated {updated_count} rows")
                return updated_count
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Data update failed: {str(e)}", exc_info=True)
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
    


 

