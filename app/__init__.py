from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


from app.controllers import default

from app.controllers import processa