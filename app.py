from flask import Flask
from api import api


app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(api)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)