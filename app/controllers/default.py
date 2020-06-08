import os
from flask_cors import CORS
from flask import render_template
from app import app
from app.models.forms import TextoForm
from urllib import request

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

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()