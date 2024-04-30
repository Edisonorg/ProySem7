from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb

app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'EdisonOrga'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbproysem7'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')   

@app.route('/admin')
def admin():
    if 'logueado' not in session or session['logueado'] is False:
        return render_template('index.html', mensaje="Acceso denegado. Inicie sesión primero.")

   
    user_id = session.get('id')

    
    connection = mysql.connection.cursor()

    
    query = "SELECT * FROM `tickets`;"
    connection.execute(query, (user_id,))

 
    tickets = connection.fetchall()
    connection.close()

    return render_template("admin.html", tickets=tickets)  

@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
       
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE correo = %s AND password = %s', (_correo, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account['id']

            return render_template("admin.html")
        else:
            return render_template('index.html',mensaje="Usuario O Contraseña Incorrectas")

    
if __name__ == '__main__':
   app.secret_key = "llave"
   app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
