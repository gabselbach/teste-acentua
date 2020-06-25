import os
from flask import render_template
from app import app
from app.models.forms import TextoForm
from urllib import request
from flask_cors import CORS


cors = CORS(app, resource={r"/*":{"origins": "*"}})

@app.route('/')
def index():
    return render_template('base.html')
@app.route('/teste')
def teste():
    texto = 'bla'
    titulo = 'new'
    return render_template('mostraconteudo.html',texto=texto,titulo=titulo)
    # your code
    # return a response


@app.route('/novo')
def novo():
    #form = TextoForm()
    return render_template('index.html')