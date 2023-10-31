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

@app.route('/scientists', methods=['GET', 'POST'])
def all_scientists():
    if request.method == 'GET':
        scientists = Scientist.query.all()
        body = [s.to_dict(rules=('-missions',)) for s in scientists]
        return body, 200
    elif request.method == 'POST':
        data = request.get_json()
        new_sci = Scientist(
            name=data.get('name'),
            field_of_study=data.get('field_of_study')
        )
        db.session.add(new_sci)
        db.session.commit()
        return new_sci.to_dict(rules=('-missions',)), 201

@app.route('/scientists/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def get_by_scientist(id):
    s = Scientist.query.filter(Scientist.id == id).first()

    if not s:
        return {"error": "Scientist not found"}, 404
    
    if request.method == 'GET':
        return s.to_dict(), 200
    elif request.method == 'PATCH':
        data = request.get_json()
        for field in data:
            # s.field = data[field] <- does not work!
            # setattr(obj, field (as a string), value)
            try:
                setattr(s, field, data[field])
            except ValueError as e:
                print(e)
                return {"errors": str(e)}, 400
        db.session.add(s)
        db.session.commit()
        return s.to_dict(rules=('-missions',)), 200
    elif request.method == 'DELETE':
        db.session.delete(s)
        db.session.commit()
        return {}, 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)
