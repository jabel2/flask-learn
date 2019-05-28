from flask import Flask, g, request, redirect, jsonify, session, render_template, url_for
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ThisSecret'

def connect_db():
    sql = sqlite3.connect('/home/abel/Desktop/Flask/flask-learn/data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1> The ID is {}.  The name is {}. The location is {}.</h1>'.format(results[0]['id'], results[0]['name'], results[0]['location'])

#webform
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template("/form.html")
    else:
        name = request.form['name']
        location = request.form['location']
        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()
        return redirect(url_for('home', name=name, location=location))


@app.route('/')
def index():
    return '<h1>Hello</h1>'

@app.route('/home', methods= ['GET', 'POST'], defaults={'name' : 'Default'})
@app.route('/home/<name>')
def home(name):
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()

    return render_template('home.html', name=name, display=False, results=results)

if __name__ == '__main__':
    app.run()
