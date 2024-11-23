from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Configure MySQL connection
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            port=3306,
            user="sql12746980",
            password="HDrSwblqmu",
            database="sql12746980"
        )
        if connection.is_connected():
            return connection
        else:
            return None
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Connect to the database
    db = create_db_connection()
    
    if db is None:
        return jsonify({
            "status": "false",
            "message": "Could not connect to database!"
        }), 500

    try:
        # Validate user credentials
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT usertype, blood_group 
            FROM users 
            WHERE username=%s AND password=%s
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return jsonify({
                "status": "true",
                "usertype": user['usertype'],
                "blood_group": user['blood_group'],  # Include blood_group in the response
                "message": f"Welcome, {username}!"
            }), 200
        else:
            return jsonify({
                "status": "false",
                "message": "Invalid credentials!"
            }), 400
    except Error as e:
        return jsonify({
            "status": "false",
            "message": f"Database query error: {str(e)}"
        }), 500
    finally:
        if db.is_connected():
            cursor.close()  # Close cursor
            db.close()  # Close connection

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
