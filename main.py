from flask import Flask, request, jsonify
import requests
import pymysql
from pymysql.cursors import DictCursor
import os

if os.environ.get("HOST"):
    HOST = os.environ.get("HOST")
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")
    DATABASE = os.environ.get("DATABASE")
else:
    from user_credentials import HOST, USER, PASSWORD, DATABASE

# create connection with mysql
conn = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)
with conn.cursor() as setup_cursor:
    setup_cursor.execute("""
    CREATE TABLE IF NOT EXISTS wifi_entries (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        password VARCHAR(255),
        downvotes INT NOT NULL DEFAULT 0,
        upvotes INT NOT NULL DEFAULT 0
    );
    """)
    conn.commit()

app = Flask(__name__)

app.route("login", methods = ["POST"])

def login():
    cursor = conn.cursor()
    name = request.args.get("name")
    email = request.args.get("email")
    role = request.args.get("role")
    community_id = request.args.get("community_id")

    cursor.execute("INSERT INTO users (name, email, role, community_id) VALUES (%s,%s,%s,%s);", (name, email, role, community_id))
    return jsonify("message", "successfully created user"), 201

if __name__ == "__main__":
    app.run(debug=True)



    



