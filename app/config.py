import os
import urllib.parse

class Config:
    # Retrieve DB creds from env
    DB_SERVER = os.getenv('DB_SERVER', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'SmartVendorDB')
    DB_USER = os.getenv('DB_USER', 'sa')
    DB_PASS = os.getenv('DB_PASS', 'YourStrongPassword123')
    
    # Construct Connection String
    params = urllib.parse.quote_plus(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={DB_SERVER};'
        f'DATABASE={DB_NAME};'
        f'UID={DB_USER};'
        f'PWD={DB_PASS};'
    )
    
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False