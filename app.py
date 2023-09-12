from flask import Flask, g, render_template, request, session, abort, flash, redirect, url_for
from posts import posts
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pudim'

app.config.from_object(__name__)
DATABASE = "banco.bd"

def conectar():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.bd = conectar()

@app.teardown_request
def teardown_request(f):
    g.bd.close()

@app.route('/')
def exibir_entradas():
    sql = "SELECT id, titulo, texto, data_criacao FROM posts ORDER BY id DESC"
    resultado = g.bd.execute(sql)
    entradas = []

    for id, titulo, texto, data_criacao in resultado.fetchall():
        entradas.append({
            "id": id,
            "titulo": titulo,
            "texto": texto,
            "data_criacao": data_criacao

        })
    
    return render_template('exibir_entradas.html', entradas=entradas)

@app.route('/login', methods=["GET","POST"])
def login():
    erro = None
    if request.method == "POST": 
        if request.form['username'] == "admin" and request.form['password'] == "admin":
            session['logado'] = True
            flash('Login OK')
            return redirect(url_for('exibir_entradas'))
        erro = "Login e/ou senha inválidos"

    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.pop('logado')
    flash('Logout efetuado com sucesso')
    return redirect(url_for('exibir_entradas'))

@app.route('/inserir', methods=["POST"])
def inserir_entradas():
    if session['logado']:
        titulo = request.form['titulo']
        texto = request.form['texto']

        sql = "INSERT INTO posts (titulo, texto) VALUES (?, ?)"

        g.bd.execute(sql, [titulo, texto])
        g.bd.commit()

        flash("Post cadastrado com sucesso")
        return redirect(url_for('exibir_entradas'))

@app.route('/posts/<int:id>')
def exibir_entrada(id):
    try:
        sql = "SELECT id, titulo, texto, data_criacao FROM posts WHERE id = ?"
        resultado = g.bd.execute(sql, [id]).fetchone()

        entrada = {
            "id": resultado[0],
            "titulo": resultado[1],
            "texto": resultado[2],
            "data_criacao": resultado[3]
        }

        return render_template('exibir_entrada.html', entrada=entrada)
    except Exception:
        return redirect(url_for('exibir_entradas'))

        
