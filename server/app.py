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
        scis = Scientist.query.all()
        dicts = []
        for sci in scis:
            dicts.append(sci.to_dict(rules=['-missions']))
        return dicts, 200
        # return [s.to_dict(rules=['-missions']) for s in Scientist.query.all()], 200
    elif request.method == 'POST':
        json_data = request.get_json()

        try:
            new_sci = Scientist(
                name=json_data.get('name'),
                field_of_study=json_data.get('field_of_study')
            )
        except ValueError as e:
            return {"errors": ["validation errors"]}, 400
        
        db.session.add(new_sci)
        db.session.commit()
        return new_sci.to_dict(rules=['-missions']), 201

@app.route('/scientists/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def scientist_by_id(id):
    sci = Scientist.query.filter(Scientist.id == id).first()

    if sci is None:
        return {"error": "Scientist not found"}, 404
    
    if request.method == 'GET':
        return sci.to_dict(), 200
    elif request.method == 'PATCH':
        json_data = request.get_json()

        try:
            for key, value in json_data.items():
                setattr(sci, key, value)  # sci.key = value
        except ValueError as e:
            return {"errors": ["validation errors"]}, 400
        
        db.session.add(sci)
        db.session.commit()

        return sci.to_dict(rules=['-missions']), 202
    elif request.method == 'DELETE':
        db.session.delete(sci)
        db.session.commit()
        return {}, 204

@app.route('/planets', methods=['GET'])
def all_planets():
    return [p.to_dict(rules=['-missions']) for p in Planet.query.all()]

@app.route('/missions', methods=['POST'])
def all_missions():
    json_data = request.get_json()
    
    try:
        new_mission = Mission(
            name=json_data.get('name'),
            scientist_id=json_data.get('scientist_id'),
            planet_id=json_data.get('planet_id')
        )
    except ValueError as e:
        return {"errors": ["validation errors"]}, 400
    
    db.session.add(new_mission)
    db.session.commit()

    return new_mission.to_dict(), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
