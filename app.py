from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'darshan.cj4oqcie8m6x.ap-south-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Local_1234567'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'darshan'  # Replace with your database name

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sys_config")  # Query the sys_config table
    data = cur.fetchall()  # Fetch all data from the table
    cur.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)


