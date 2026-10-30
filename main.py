from flask import Flask, request, jsonify
import pymysql
from pymysql.cursors import DictCursor

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="welcome123",
    database="spotlight"
)

app = Flask(__name__)

@app.route("/signup", methods=["POST"])
def signup():
    cursor = conn.cursor()
    name = request.args.get("name")
    email = request.args.get("email")
    role = request.args.get("role")
    password = request.args.get("password")
    community_id = request.args.get("community_id")

    if not email or "@" not in email:
        return jsonify({"message": "Valid email is required"}), 400

    # Extract username from email (e.g., 'alex' from 'alex@example.com')
    username = email.split("@")[0]

    # Save username alongside name, email, role, community_id, and password
    cursor.execute(
        "INSERT INTO users (name, username, email, role, community_id, password) VALUES (%s, %s, %s, %s, %s, %s);",
        (name, username, email, role, community_id, password)
    )
    conn.commit()
    cursor.close()
    
    return jsonify({"message": "successfully created user", "username": username}), 201


@app.route("/login", methods=["POST"])
def login():
    cursor = conn.cursor(DictCursor)
    username = request.args.get("username")
    password = request.args.get("password")

    cursor.execute("SELECT password FROM users WHERE username = %s;", (username,))
    password_input = cursor.fetchone()
    cursor.close()

    if not password_input:
        return jsonify({"message": "username provided does not match any username in database"}), 400

    if password_input["password"] == password:
        return jsonify({"message": "successfully logged in!"}), 200
        
    return jsonify({"message": "wrong password"}), 401


if __name__ == "__main__":
    app.run(debug=True)