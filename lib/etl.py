import logging
#логирование отдеьным классом
#база данных
#Airflow


from clients import FileClient, DatabaseClient
from processors import TextProcessor
from config import *
from utils.logger import logger

"""Main module."""
class App():
    def handle(place, processor=None):

        if place == 'textf':
            app()

        else:
            app_db()

def app() -> None:
    
    client = FileClient()
    processor = TextProcessor()

    logger.info("ETL process has started")

    try:
        raw_data = client.read(RAW_DATA_PATH)
        logger.info(f"Extracted {len(raw_data)} lines from {RAW_DATA_PATH}.")
    except Exception as e:
        logger.error(f"ETL process failed on extraction stage: {str(e)}")
        raise

    try:
        processed_data = processor.process(raw_data)
        logger.info(f"Transformed {len(processed_data)} lines.")
    except Exception as e:
        logger.error(f"ETL process failed on transforming stage: {str(e)}")
        raise

    try:
        client.write(PROCESSED_DATA_PATH, processed_data)
        logger.info(f"Loaded {len(raw_data)} lines in {PROCESSED_DATA_PATH}.")
    except Exception as e:
        logger.error(f"ETL process failed on loading stage: {str(e)}")
        raise

    logger.info("ETL process successfully completed")


def app_db() -> None:
    logger.info("Starting DATABASE ETL process")
    
    db_client = DatabaseClient(**db_consts.db_params)

    processor = TextProcessor()
    try:
        db_client.connect()
        logger.info("Successfully connected")

    except Exception as e:
        logger.error(f"Something went wrong during connection to database: {e}")

    try:
        raw_data, columns = db_client.read("select * from users")
        logger.info(f"Extracted {len(raw_data)} lines from file")

    except Exception as e:
        logger.error(f"ETL process failed on extraction stage: {str(e)}")
        raise

    try:
        
        processed_data = processor.process(raw_data)
        logger.info(f"Transformed {len(processed_data)} lines")
    except Exception as e:
        logger.error(f"ETL process failed on transforming stage: {str(e)}")
        raise
    try:
        full_data = (processed_data, columns)
        db_client.write(table="users", data=full_data)

    except Exception as e:
        logger.error(f"ETL process failed on loading stage: {str(e)}")
        raise
    
    try:
        db_client.disconnect()

    except Exception as e:
        logger.error(f"Something went wrong during disconnection to db: {e}")  
        
    #     with db_client:
    #         db_client.create_table(
    #             "etl_results",
    #             """
    #             id INTEGER PRIMARY KEY,
    #             raw_content TEXT NOT NULL,
    #             processed_content TEXT NOT NULL,
    #             source_file TEXT,
    #             processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #             """
    #         )
            
    #         inserted_count = db_client.load_data("etl_results", db_data)
        

    logger.info("DATABASE ETL process successfully completed")


    #класс c методом 