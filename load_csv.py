import mysql.connector
import pandas as pd

host = "localhost"
user = "nishuz"
password = 
database_name = "EB_Database"

connection = mysql.connector.connect(
    host = host,
    user = user,
    password = password
)

cursor = connection.cursor()

cursor.execute(f"DROP DATABASE IF EXISTS {database_name};")
cursor.execute(f"CREATE DATABASE {database_name};")
cursor.execute(f"USE {database_name};")

table_names = ['EB_Redemption_Details', 'EB_Purchase_Details']
csv_files = ['redemption_data.csv', 'purchase_data.csv']

for table_name, csv_file in zip(table_names, csv_files):
    df = pd.read_csv(csv_file)
    
    cleaned_columns = [col.replace(' ', '_').replace('.', '') for col in df.columns]
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'`{col}` TEXT' for col in cleaned_columns])});"
    cursor.execute(create_table_query)

    for _, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(insert_query, tuple(row))

connection.commit()
cursor.close()
connection.close()
print("Data imported successfully!")
