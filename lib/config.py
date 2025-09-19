class DBConstants():
    def __init__(self,
            HOST="localhost",
            USER="postgres",
            PASSWORD="hard_password",
            DB_NAME="etl_database",
            PORT=5432):
        
        self.db_params = {
        self.host:HOST,
        self.user:USER,
        self.password:PASSWORD,
        self.db_name:DB_NAME,
        self.port:PORT
        }
        


db_consts = DBConstants()



RAW_DATA_PATH = "../data/raw/text.txt"
PROCESSED_DATA_PATH = "../data/processed/processed_text.txt"




#config все что с бдшкой, в один класс.