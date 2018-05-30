import sqlite3
from flask import Flask, render_template, g, request
app = Flask(__name__)

#alchemy
DATABASE = 'test.db'

#connects to given sqlie db file
def connect_to_database():
    return sqlite3.connect(DATABASE)

#retrieves db to perform CRUD and queries
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

#ensures closure of db connections and webpage components
@app.teardown_request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#default homepage, routed from home and the base url
@app.route("/")
@app.route("/home")
def home():
    pagetest = {'type' : 'Tester'}
    return render_template('index.html', pagetype=pagetest)

#default sql insertion page. This should use a input sanitizer and not this code for anything safety critical
@app.route("/insert", methods=["GET","POST"])
def insert():
    errortext = ''
    if request.method == "POST":
        conn = get_db()
        sql_data = request.form['sql']
        try:
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(c.fetchall())
            c.execute(sql_data)
            errortext = c.fetchall()
            print(c.fetchall())
            conn.commit()
        except sqlite3.OperationalError:
            errortext = 'that seems to be invalid sql, please try again'

    return render_template('insert.html', errortext=errortext)


#runs servlet, debug=true if you want to test running code
if __name__ == "__main__":
    app.run(debug=True)
