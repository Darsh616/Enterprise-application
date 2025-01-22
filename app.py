import os
from flask import Flask, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration for MySQL 
app.config['MYSQL_HOST'] = 'darshan.cj4oqcie8m6x.ap-south-1.rds.amazonaws.com'  # If it's a local IP address
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Local_1234567'
app.config['MYSQL_DB'] = 'darshan'

mysql = MySQL(app)

@app.route('/')
def index():
    try:
        # Get a cursor object from the connection
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM sys_config")
        data = cur.fetchall()

        # Render the index.html page and pass the data
        return render_template('index.html', data=data)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
