from flask import Flask
from api import api
# from flask_cors import CORS


app = Flask(__name__)
# CORS(app)
app.config.from_object('config')
app.register_blueprint(api)

    