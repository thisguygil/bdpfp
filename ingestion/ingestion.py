import pandas as pd
import os
import traceback
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Local MySQL connection details and CSV file path for testing
local_username = ""
local_password = ""
local_connection_string = f"mysql+pymysql://{local_username}:{local_password}@localhost"
local_csv_file_path = 'ingestion/tweets.csv'

# Define the MySQL connection string and the CSV file path
mysql_connection_string = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@mysql-service"
csv_file_path = 'tweets.csv'

# Initialize the database engine
engine = create_engine(mysql_connection_string)

def setup_database(engine):
    try:
        # Connect to the MySQL server (without specifying a database)
        with engine.connect() as conn:
            # Create and use the database if it does not exist
            conn.execute(text("CREATE DATABASE IF NOT EXISTS twitter"))
            conn.execute(text("USE twitter"))

            # Create the table if it does not exist
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS tweets (
                    tweet_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    author VARCHAR(255),
                    content LONGTEXT,
                    country VARCHAR(255),
                    date_time DATETIME,
                    id BIGINT,
                    language VARCHAR(50),
                    latitude FLOAT,
                    longitude FLOAT,
                    number_of_likes INT,
                    number_of_shares INT
                );
            """))

            # Add a full-text index on the content column for searching
            conn.execute(text("""
                ALTER TABLE tweets ADD FULLTEXT(content);
            """))
            print("Database and table setup completed successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred while setting up the database and table: {e}")
        traceback.print_exc()

# Call the database setup function
setup_database(engine)

def insert_data_from_csv(engine):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Convert the date_time column to datetime format
        df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%Y %H:%M')
        
        # Write the DataFrame to the SQL table
        df.to_sql('tweets', con=engine, schema='twitter', if_exists='append', index=False, method='multi')
        print("Data inserted into 'tweets' table successfully.")
    except Exception as e:
        print(f"An error occurred while inserting data from CSV: {e}")
        traceback.print_exc()

# Insert data into the database from the CSV file
insert_data_from_csv(engine)
