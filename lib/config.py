class DBConstants():
    def __init__(self,
            HOST="localhost",
            USER="postgres",
            PASSWORD="hard_password",
            DB_NAME="etl_database",
            PORT=5432):
        
        self.db_params = {
        'host':HOST,
        'user':USER,
        'password':PASSWORD,
        'dbname':DB_NAME,
        'port':PORT
        }
        


db_consts = DBConstants()



RAW_DATA_PATH = "../data/raw/text.txt"
PROCESSED_DATA_PATH = "../data/processed/processed_text.txt"




#config все что с бдшкой, в один класс.