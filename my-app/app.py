from flask import Flask, jsonify
import os
import pymysql
from pymongo import MongoClient

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "v1.0")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-svc.database.svc.cluster.local")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASS = os.getenv("MYSQL_PASS", "RootPassword123")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://rootadmin:MongoPassword123@mongodb-svc.database.svc.cluster.local:27017/?authSource=admin")

@app.route("/")
def home():
    mysql_status = "Disconnected"
    mongo_status = "Disconnected"

    # MySQL Check
    try:
        conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASS, connect_timeout=2)
        mysql_status = "Connected"
        conn.close()
    except Exception as e:
        mysql_status = f"Error: {str(e)}"

    # Mongo Check
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        mongo_status = "Connected"
        client.close()
    except Exception as e:
        mongo_status = f"Error: {str(e)}"

    return jsonify({
        "version": VERSION,
        "message": f"Hello from App Version {VERSION}!",
        "mysql_database": mysql_status,
        "mongo_database": mongo_status
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
