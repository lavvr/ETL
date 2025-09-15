import logging
#логирование отдеьным классом
#база данных
#Airflow


from clients import FileClient, DatabaseClient
from processors import TextProcessor
from config import *
from utils import logger

"""Main module."""
def app():
    
    client = FileClient()
    processor = TextProcessor()

    logging.info("ETL process has started")

    try:
        raw_data = client.read(RAW_DATA_PATH)
        logging.info(f"Extracted {len(raw_data)} lines from {RAW_DATA_PATH}.")
    except Exception as e:
        logging.error(f"ETL process failed on extraction stage: {str(e)}")
        raise

    try:
        processed_data = processor.process(raw_data)
        logging.info(f"Transformed {len(processed_data)} lines.")
    except Exception as e:
        logging.error(f"ETL process failed on transforming stage: {str(e)}")
        raise

    try:
        client.write(PROCESSED_DATA_PATH, processed_data)
        logging.info(f"Loaded {len(raw_data)} lines in {PROCESSED_DATA_PATH}.")
    except Exception as e:
        logging.error(f"ETL process failed on loading stage: {str(e)}")
        raise

    logging.info("ETL process successfully completed")


def app_db():
    logger.info("Starting DATABASE ETL process")
    
    file_client = FileClient()
    db_client = DatabaseClient(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
    )

    processor = TextProcessor()

    try:
        
        raw_data = file_client.read(RAW_DATA_PATH)
        logger.info(f"Extracted {len(raw_data)} lines from file")
        
        
        processed_data = processor.process(raw_data)
        logger.info(f"Transformed {len(processed_data)} lines")
        
        db_data = []
        for i, (raw_line, processed_line) in enumerate(zip(raw_data, processed_data), 1):
            db_data.append({
                "id": i,
                "raw_content": raw_line.strip(),
                "processed_content": processed_line.strip(),
                "source_file": RAW_DATA_PATH.name
            })
        
        with db_client:
            db_client.create_table(
                "etl_results",
                """
                id INTEGER PRIMARY KEY,
                raw_content TEXT NOT NULL,
                processed_content TEXT NOT NULL,
                source_file TEXT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                """
            )
            
            inserted_count = db_client.load_data("etl_results", db_data)
        
    except Exception as e:
        logger.error(f"DATABASE ETL process failed: {str(e)}", exc_info=True)
        raise

    logger.info("DATABASE ETL process successfully completed")