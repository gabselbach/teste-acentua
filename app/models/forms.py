from flask_wtf import Form
from wtforms import TextField

class TextoForm(Form):
    titulo = TextField('titulo')
    texto = TextField('texto')