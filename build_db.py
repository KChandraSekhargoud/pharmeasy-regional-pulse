import sqlite3
import pandas as pd

def build_database():
    conn = sqlite3.connect('pharmeasy.db')
    pd.read_csv('regions_master.csv').to_sql('regions_master', conn, if_exists='replace', index=False)
    pd.read_csv('orders_clean.csv').to_sql('orders_clean', conn, if_exists='replace', index=False)
    conn.close()
    print("Database pharmeasy.db built successfully.")

if __name__ == "__main__":
    build_database()