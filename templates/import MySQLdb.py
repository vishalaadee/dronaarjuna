import MySQLdb
from flask import Flask,render_template,request,url_for,session,redirect
from flask.sessions import NullSession
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app= Flask(__name__)
app.secret_key = 'dbms'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='vishal29'
app.config['MYSQL_DB']='placement'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template("Sindex.html")


@app.route('/student_login/',methods=['GET','POST'])
def student_login():
    msg = ''
    if request.method == 'POST' and 'USN' in request.form and 'student_password' in request.form:
        USN = request.form['USN']
        student_password = request.form['student_password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_table WHERE USN = %s AND student_password = %s', (USN,student_password))
        mysql.connection.autocommit(True)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['USN'] = account['USN']
            return render_template('inside_student.html')
        else:
            msg = 'Incorrect username/password!'
    return render_template('Vstudent_login.html', msg='')
@app.route('/student_login/home')
def home():
   session.pop('loggedin', None)
   session.pop('USN', None)
   return render_template('inside_student.html')

@app.route('/student_register/', methods=['GET', 'POST'])
def student_register():
    msg = ''
    if request.method == 'POST' and 'USN' in request.form and 'student_name' in request.form and 'branch' in request.form and 'semester' in request.form and 'student_password' in request.form and 'student_email' in request.form:
        USN = request.form['USN']
        student_name=request.form['student_name']
        branch=request.form['branch']
        semester=request.form['semester']
        student_password = request.form['student_password']
        student_email = request.form['student_email']
                
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_table WHERE USN = %s', (USN,))
        account = cursor.fetchone()
        if account:
            msg = 'USN already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', student_email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', USN):
            msg = 'USN must contain only characters and numbers!'
        elif not USN or not student_password or not student_email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO student_table VALUES ( %s, %s, %s, %s, %s, %s)', (USN,student_name,semester,branch,student_email,student_password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('Vstudent_register.html', msg=msg)




if __name__ == '__main__':
    app.run(debug=True)
