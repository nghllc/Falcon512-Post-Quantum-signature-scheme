from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mydatabase'
app.config['MYSQL_HOST'] = 'mysql'
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users''')
    rv = cur.fetchall()
    return str(rv)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)