#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/scientists')
def all_scientists():
    scis = Scientist.query.all()
    dicts = []
    for sci in scis:
        dicts.append(sci.to_dict(rules=['-missions']))
    return dicts, 200
    # return [s.to_dict(rules=['-missions']) for s in Scientist.query.all()], 200

@app.route('/scientists/<int:id>')
def scientist_by_id(id):
    sci = Scientist.query.filter(Scientist.id == id).first()

    if sci is None:
        return {"error": "Scientist not found"}, 404
    
    return sci.to_dict(), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
