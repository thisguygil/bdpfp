from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os

# Initialize the Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Local MySQL connection details and CSV file path for testing
local_username = ""
local_password = ""
local_connection_string = f"mysql+pymysql://{local_username}:{local_password}@localhost"

# Define the MySQL connection string
mysql_connection_string = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@mysql-service"

# Initialize the database engine
engine = create_engine(mysql_connection_string)

@app.route('/search', methods=['POST'])
def search():
    # Get the search query from the request
    data = request.json
    search_query = data['query']
    
    # Connect to the MySQL server and execute the search query
    with engine.connect() as connection:
        connection.execute(text("USE twitter"))
        sql_query = text("SELECT * FROM tweets WHERE MATCH(content) AGAINST(:search_query IN NATURAL LANGUAGE MODE) OR author LIKE :match_author")
        result = connection.execute(sql_query, {'search_query': search_query, 'match_author': f"%{search_query}%"}).mappings().all()
    
    # Convert the result to a list of dictionaries and return it as JSON
    tweets = [dict(row) for row in result]
    return jsonify(tweets)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
