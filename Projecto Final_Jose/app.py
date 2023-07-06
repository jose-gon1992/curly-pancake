import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bcrypt = Bcrypt(app)



def connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Basicamente isto vai obrigar a que o user esteja registado
# extende a funcionalidade da function based view WRAPPER FUNCTION
def login_necessario(f):
    @wraps(f)
    def funcao_decorator(*args, **kwargs):
        if not bool(session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return funcao_decorator




@app.route('/paineladm', methods=["GET","POST"])
@login_necessario
def padm():
    
    conn = connection()
    if request.method=="POST":
        conn.execute("UPDATE users SET role = ? WHERE id=?",(request.form['role'],request.form['iduser']))
        conn.commit()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('paineladm.html',users=users)
   

@app.route('/sobre')
@login_necessario
def sobre():
   
    return render_template('sobre.html')
   

@app.route('/analise')
@login_necessario
def analise():
    return render_template('analysis.html')

@app.route('/game/<int:id>/')
@login_necessario
def game(id):
    
    con = connection()
    cur = con.cursor()
    cur2 = con.cursor()
    cur.execute( f"Select * from perguntas where fk_id_jogo = {id}" )
    perguntas = cur.fetchall()
    
    
    perguntas_respostas = {}
    for pergunta in perguntas:
        id_pergunta = pergunta[0]
        pergunta_str = pergunta[1]
        
        cur2.execute(f"Select * from respostas where fk_id_pergunta = {id_pergunta}")
        respostas = cur2.fetchall()
        respostas_possiveis = {}
        for resposta in respostas:
            res = str(resposta[2])
            id_resposta = resposta[0]
            resposta = resposta[1]

            respostas_possiveis[id_resposta] = (resposta, res)
            
        perguntas_respostas[id_pergunta] = { 
            pergunta_str : respostas_possiveis 
        }
    print(perguntas_respostas)
    con.close()
    return render_template('game.html', perguntas_respostas = perguntas_respostas, id=id )

    
@app.route('/')
@login_necessario
def index():
    
    con = connection()
    cur = con.cursor()

    cur.execute('SELECT * FROM jogos')
    jogos = cur.fetchall()

    jogos_to_display = {}

    for jogo in jogos:
        jogos_to_display[jogo[0]] = jogo[1]
        print(f"id jogo: {jogo[0]} nome jogo: {jogo[1]}")
    print(jogos_to_display)
    con.close()
    return render_template('home.html', jogos=jogos_to_display)
    


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        password = request.form['password']
        conn = connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?',
                            (request.form['username'],)).fetchone()
        conn.close()
        if user and bcrypt.check_password_hash(user["password"], password):
            session["user"] = user["username"].lower()
            session["role"] = user["role"]
            return redirect(url_for('index'))
        else:
            flash("Incorrect username or password!")
    return render_template('login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        errors = []
        username = request.form['username'].lower()
        password = request.form['password']

        conn = connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?',
                            (username,)).fetchone()
        conn.close()

        if user:
            errors.append("Utilizador {} já existe!".format(username))

        if len(username) < 3 or len(username) > 20:
            errors.append("Utilizador deve ter 3 a 20 letras!")
        if len(password) < 5 or len(password) > 20:
            errors.append("Password deve ter 5 a 20 letras!")
        if request.form["g-recaptcha-response"] == "":
            errors.append("Prove que não é um robo!")

        if len(errors) > 0:
            for error in errors:
                flash(error)

        if len(errors) < 1:
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            conn = connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, password))
            conn.commit()
            conn.close()
            session["user"] = username
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route("/logout")
@login_necessario
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
