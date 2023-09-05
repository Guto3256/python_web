from flask import Flask
from flask import render_template

app = Flask("meu app")

posts = [
    {
        "titulo": "Minha Primeira Postagem",
        "texto": "Texto do meu primeiro post"
    },
    {
        "titulo": "Minha Segunda Postagem",
        "texto": "Texto do meu segundo post"
    }
]

@app.route('/')
def exibir_entradas():
    entradas = posts
    return render_template('exibir_entradas.html', entradas=entradas)