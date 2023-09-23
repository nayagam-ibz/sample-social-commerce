from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config["MYSQL_CURSORCLASS"]="DictCursor"
app.config['MYSQL_DB'] = 'testDB'
app.secret_key = 'super secret key'
mysql = MySQL(app)

@app.route('/')
@app.route('/sign_in', methods=['GET', 'POST'])

def login():
  msg = ''
  if request.method == 'POST' and 'login' in request.form:
    email = request.form['email'];
    password = request.form['password'];
    try:
      cur = mysql.connection.cursor()
      cur.execute('select * from users where email=%s and password=%s', [email, password])
      res = cur.fetchone()
      if res:
        session['loggedin'] = True
        session['email'] = res['email']
        session['name'] = res['name']
        flash('You were successfully logged in')
        return redirect(url_for('home'))
      else:
        flash('Incorrect email and password')
        return render_template("login.html", msg = msg)
    except Exception as e:
      print(e)
    finally:
      mysql.connection.commit()
      cur.close()
  return render_template('login.html', msg = msg)

@app.route('/sign_up', methods=['GET', 'POST'])
def registration():
  print("----------------------------------------------------------------0")
  if request.method == 'POST' and 'registration' in request.form:
    email = request.form['email']
    password = request.form['password']
    password_confirmation = request.form['password_confirmation']
    name = request.form['name']
    try:
      cur = mysql.connection.cursor()
      cur.execute('select * from users where email=%s', [email])
      res = cur.fetchone()
      if res:
        flash('Account already exists !')
      elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        flash('Invalid email address !')
      elif not email or not password or not name:
        flash('Please fill out the form !')
      else:
        cur.execute('INSERT INTO users VALUES (% s, % s, % s, %s)', (name, email, password, password_confirmation))
        flash('You have successfully registered !')
        return render_template("login.html")
    except Exception as e:
      print(e)
    finally:
      mysql.connection.commit()
      cur.close()
  return render_template("registration.html")


@app.route('/forgot_password')
def forgot_password():
  return render_template("forgot_password.html")

@app.route('/logout')
def logout():
  session.pop('loggedin', None)
  session.pop('id', None)
  session.pop('name', None)
  return redirect(url_for('login'))

@app.route('/home')
def home():
   return render_template("home.html")

if __name__ == '__main__':  
  
  app.run(debug=True)