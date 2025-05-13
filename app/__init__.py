from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.sett import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ENGINE_OPTIONS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = SQLALCHEMY_ENGINE_OPTIONS

db = SQLAlchemy(app)

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db}
