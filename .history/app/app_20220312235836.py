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
app.config['MYSQL_DB']='Online_Course'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template(""../templates/Sindex.html)


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
@app.route('/student_login/course/', methods=['GET', 'POST'])
def course(): 
    msg = ''
    if request.method == 'POST' and 'domain_id' in request.form :
        domain_id=request.form['domain_id']    
        domain_id=int(domain_id)   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
        cursor.execute('SELECT course_id,course_name FROM course_table WHERE domain_id = %s', (domain_id,))  
        data = cursor.fetchall()
        return render_template('output_table.html',value=data)
        #msg = 'You have successfully entered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form correctly!'
    return render_template('output_table.html')      
    #return render_template("output_table.html",value=Domain_ID) 
@app.route('/student_login/Domain_ids/', methods=['GET', 'POST'])
def Domain_ids(): 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)              
    cursor.execute("select domain_id,domain_name from domain_table") 
    data = cursor.fetchall() #data from database 
    return render_template("Domain_ids.html", value=data) 
@app.route('/student_login/project_ids/Course_ids/', methods=['GET', 'POST'])
def Course_ids(): 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
    cursor.execute("select course_id,domain_id,course_name from course_table") 
    data = cursor.fetchall() #data from database 
    return render_template("Course_ids.html", value=data) 
@app.route('/student_login/project_ids/Instructor_ids/', methods=['GET', 'POST'])
def Instructor_ids(): 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
        
    cursor.execute("select instructor_id,instructor_name,instructor_email from instructor_table") 
    data = cursor.fetchall() #data from database 
    return render_template("Instructor_ids.html", value=data) 

@app.route('/student_login/project_ids/', methods=['GET', 'POST'])
def project_ids(): 
    msg = ''
    if request.method == 'POST' and 'USN' in request.form and 'student_password' in request.form :
        USN=request.form['USN'] 
        student_password=request.form['student_password']   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student_table WHERE USN = %s AND student_password = %s', (USN,student_password))
        mysql.connection.autocommit(True)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['USN'] = account['USN']
            cursor.execute('SELECT project_id,course_id,instructor_id,eval1,eval2,eval3,grade,project_link FROM evaluation_table WHERE USN = %s', (USN,))  
            data = cursor.fetchall() 
            return render_template('project_output_table.html',value=data)
        
        else:
            msg = 'Incorrect usn/password!'
        #msg = 'You have successfully entered!'
    elif request.method == 'POST':
        msg = 'Project id not found!'
    return render_template('project_output_table.html')      

@app.route('/student_login/add_project/', methods=['GET', 'POST'])
def add_project(): 
    msg = ''
    if request.method == 'POST' and 'course_id' in request.form and 'USN' in request.form:
        course_id = request.form['course_id']
        USN=request.form['USN']
        course_id=int(course_id)        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM evaluation_table WHERE course_id = %s', (course_id,))
        account = cursor.fetchone()
        if account:
            msg = 'course already added!'
        else:
            cursor.execute('INSERT INTO evaluation_table VALUES ( NULL,%s, %s,NULL,NULL,NULL,NULL,0,NULL)', (USN,course_id,))
            mysql.connection.commit()
            msg = 'You have successfully added this course!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('project_add.html', msg=msg)
@app.route('/student_login/add', methods=['GET', 'POST'])
def add():
    msg = ''
    if request.method == 'POST' and 'domain_id' in request.form and 'course_name' in request.form:
        domain_id = request.form['domain_id']
        course_name=request.form['course_name']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM course_table WHERE course_name = %s', (course_name,))
        account = cursor.fetchone()
        if account:
            msg = 'course already exists!'
        else:
            cursor.execute('INSERT INTO course_table VALUES ( NULL,%s, %s)', (domain_id,course_name,))
            mysql.connection.commit()
            msg = 'You have successfully added this course!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('add_course.html', msg=msg)
@app.route('/student_login/Project_submit', methods=['GET', 'POST'])
def Project_submit():
    msg = ''
    if request.method == 'POST' and 'project_id' in request.form and 'Project_link' in request.form :
        project_id = request.form['project_id'] 
        project_id = int(project_id)               
        Project_link=request.form['Project_link']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Project_link FROM evaluation_table WHERE project_id = %s', (project_id,))
        account = cursor.fetchone()
        if account:
            cursor.execute('UPDATE evaluation_table SET Project_link = %s WHERE project_id = %s', (Project_link,project_id,))
            mysql.connection.commit()
            msg = 'Submitted !'
        else:
            cursor.execute('UPDATE evaluation_table SET Project_link = %s WHERE project_id = %s', (Project_link,project_id,))
            mysql.connection.commit()
            msg = 'You have successfully submitted'    
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('project.html', msg=msg)

@app.route('/instructor_login/',methods=['GET','POST'])
def instructor_login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'Instructor_password' in request.form:
        username = request.form['username']
        Instructor_password = request.form['Instructor_password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM instructor_table WHERE username = %s AND Instructor_password = %s', (username,Instructor_password))
        mysql.connection.autocommit(True)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            return render_template('inside_instructor.html')
        else:
            msg = 'Incorrect username/password!'
    return render_template('Vinstructor_login.html', msg='')
@app.route('/instructor_login/i_home')
def i_home():
   session.pop('loggedin', None)
   session.pop('username', None)
   return render_template('inside_instructor.html')

@app.route('/instructor_register/', methods=['GET', 'POST'])
def instructor_register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'instructor_name' in request.form and 'instructor_designation' in request.form and 'instructor_email' in request.form and 'instructor_password' in request.form :
        username = request.form['username']
        instructor_name=request.form['instructor_name']
        instructor_designation=request.form['instructor_designation']
        instructor_email=request.form['instructor_email']
        instructor_password = request.form['instructor_password']
                
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM instructor_table WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'username already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', instructor_email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not instructor_password or not instructor_email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO instructor_table VALUES (NULL, %s, %s, %s, %s, %s)', (instructor_name,instructor_designation,instructor_email,instructor_password,username))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('Vinstructor_register.html', msg=msg)
@app.route('/instructor_login/scout/', methods=['GET', 'POST'])
def scout(): 
    msg = ''
    if request.method == 'POST' and 'domain_id' in request.form :
        domain_id=request.form['domain_id']
        domain_id=int(domain_id)       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
        cursor.execute('SELECT e.USN,e.project_id,e.course_id FROM evaluation_table e INNER JOIN course_table c ON e.course_id=c.course_id INNER JOIN domain_table d ON d.domain_id=c.domain_id WHERE d.domain_id = %s and e.instructor_id=0', (domain_id,))  
        data1 = cursor.fetchall()
        cursor.execute('SELECT s.student_name,s.student_email FROM student_table s INNER JOIN evaluation_table e ON s.USN=e.USN INNER JOIN course_table c ON e.course_id=c.course_id INNER JOIN domain_table d ON d.domain_id=c.domain_id WHERE d.domain_id = %s and e.instructor_id=0', (domain_id,))  
        data = cursor.fetchall()
        return render_template('output_scout_table.html',data=data1,data1=data)
        #msg = 'You have successfully entered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form correctly!'
    return render_template('output_scout_table.html')      

@app.route('/instructor_login/add_student', methods=['GET', 'POST'])
def add_student():
    msg = ''
    if request.method == 'POST' and 'project_id' in request.form and 'instructor_id' in request.form:
        project_id = request.form['project_id'] 
        id=int(project_id)
        instructor_id=request.form['instructor_id']
        iid=int(instructor_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT instructor_id FROM evaluation_table WHERE project_id = %s', (id,))
        account = cursor.fetchone()
        if account:
            cursor.execute('UPDATE evaluation_table SET instructor_id = %s WHERE project_id = %s', (iid,id))
            mysql.connection.commit()
            
            msg = 'Instructor assigned !'
        else:
            msg = 'Enter Valid P-ID !'    
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('add_instructor.html', msg=msg)

@app.route('/instructor_login/Evaluate', methods=['GET', 'POST'])
def Evaluate():
    msg = ''
    if request.method == 'POST' and 'project_id' in request.form and 'eval1' in request.form and 'eval2' in request.form and 'eval3' in request.form:
        eval1=request.form['eval1']
        eval2=request.form['eval2']
        eval3=request.form['eval3']
        grade=0
        project_id=request.form['project_id']
        id=int(project_id)    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT USN FROM evaluation_table WHERE project_id = %s', (id,))
        account = cursor.fetchone()
        if account:
            
            if eval2=='0' and eval3=='0' and grade=='0':
                cursor.execute('UPDATE evaluation_table SET eval1=%s WHERE project_id =%s', (eval1,id,))
                mysql.connection.commit()
            elif eval3=='0' and grade=='0':
                cursor.execute('UPDATE evaluation_table SET eval1=%s,eval2=%s WHERE project_id =%s', (eval1,eval2,id,))
                mysql.connection.commit()
            elif grade=='0':
                cursor.execute('UPDATE evaluation_table SET eval1=%s,eval2=%s,eval3=%s WHERE project_id =%s', (eval1,eval2,eval3,id,))
                mysql.connection.commit()
            else:
                marks=((int(eval1) + int(eval2) + int(eval3))/60)*100
                if marks>40 and marks<51:
                    grade='E'
                elif marks>50 and marks<61:
                    grade='D'
                elif marks>60 and marks<65:
                    grade='C'
                elif marks>64 and marks<75:
                    grade='B'
                elif marks>74 and marks<90:
                    grade='A'
                elif marks>89 and marks<101:
                    grade='S'
                else:
                    grade='F'
                
                cursor.execute('UPDATE evaluation_table SET eval1=%s,eval2 = %s,eval3 = %s,grade=%s WHERE project_id =%s', (eval1,eval2,eval3,grade,id,))
                mysql.connection.commit()
            msg = 'Marks assigned !'
        else:
            msg = 'Error !'    
    elif request.method == 'POST':
        msg = 'Please fill ot the form!'
    return render_template('add_marks.html', msg=msg)
@app.route('/instructor_login/view_submission/', methods=['GET', 'POST'])
def view_submission(): 
    msg = ''
    if request.method == 'POST' and 'instructor_id' in request.form :
        instructor_id=request.form['instructor_id']       
        id=int(instructor_id)      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
        cursor.execute('SELECT USN,project_id,project_link,eval1,eval2,eval3,grade FROM evaluation_table WHERE instructor_id = %s', (id,))  
        data = cursor.fetchall()
        return render_template('view_submission.html',data=data)
        #msg = 'You have successfully entered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form correctly!'
    return render_template('view_submission.html')      
@app.route('/instructor_login/delete_project', methods=['GET', 'POST'])
def delete_project():
    msg = ''
    if request.method == 'POST' and 'project_id' in request.form :
        project_id = request.form['project_id'] 
        id=int(project_id)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT Course_id FROM evaluation_table WHERE project_id = %s', (id,))
        account = cursor.fetchone()
        if account:
            cursor.execute('DELETE FROM evaluation_table WHERE Project_id = %s', (id,))
            mysql.connection.commit()
            
            msg = 'deletion done !'
        else:
            msg = 'Error !'    
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('del_proj.html', msg=msg)




if __name__ == '__main__':
    app.run(debug=True)
