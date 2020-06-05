import os
from app import app
from flask_cors import CORS

cors = CORS(app, resource={r"/*":{"origins": "*"}})


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/novo')
def hello_world():
    return 'Ola mundo cruel!'

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()