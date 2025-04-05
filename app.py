
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

DB_NAME = 'licenses.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mt5_id TEXT NOT NULL,
            license_type TEXT NOT NULL,
            expiration DATE NOT NULL
        )
        ''')

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM licenses")
        data = cur.fetchall()
    return render_template('index.html', licenses=data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    mt5_id = request.form['mt5_id']
    license_type = request.form['license_type']
    days = {'Access': 30, 'Elite': 90, 'Legacy': 3650}.get(license_type, 30)
    expiration = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO licenses (name, mt5_id, license_type, expiration) VALUES (?, ?, ?, ?)",
                     (name, mt5_id, license_type, expiration))
    return redirect('/')

@app.route('/delete/<int:license_id>')
def delete(license_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM licenses WHERE id = ?", (license_id,))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
