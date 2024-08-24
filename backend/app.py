from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="mysql-service",  # Name of the MySQL service in Kubernetes
    user="root",
    password="your-password",
    database="notes_db"
)

@app.route('/notes', methods=['GET'])
def get_notes():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    cursor.close()
    return jsonify(notes)

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    note = data.get('note')

    if not note:
        return jsonify({"error": "Note content is required"}), 400

    cursor = db.cursor()
    cursor.execute("INSERT INTO notes (content) VALUES (%s)", (note,))
    db.commit()
    cursor.close()

    return jsonify({"message": "Note added successfully"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
