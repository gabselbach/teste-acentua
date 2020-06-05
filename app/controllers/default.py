import os
from app import app
from flask_cors import CORS

cors = CORS(app, resource={r"/*":{"origins": "*"}})


@app.route('/')
def hello_world():
    return 'Hello, World!'

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()