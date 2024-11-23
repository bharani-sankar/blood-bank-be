from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure MySQL connection
db = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    port=3306,
    user="sql12746980",
    password="HDrSwblqmu",
    database="sql12746980"
)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
