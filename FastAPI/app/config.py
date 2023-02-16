import os

DbConfig = dict(DB_FILEPATH=os.getenv("CSV_FILE", "./db/stock_db.csv"))
