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
        return [s.to_dict(rules=['-missions']) for s in scientists], 200
    elif request.method == 'POST':
        json_data = request.get_json()

        try:
            new_sci = Scientist(
                name=json_data.get('name'),
                field_of_study=json_data.get('field_of_study')
            )
        except ValueError as e:
            return {'error': str(e)}, 400

        print(new_sci.id)  # None
        db.session.add(new_sci)
        db.session.commit()
        print(new_sci.id)  # 6 (or whatever the next id is)

        return new_sci.to_dict(rules=['-missions']), 201

@app.route('/scientists/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def scientist_by_id(id):
    scientist = Scientist.query.filter(Scientist.id == id).first()

    if scientist is None:
        return {'error': 'scientist not found'}, 404

    if request.method == 'GET':
        return scientist.to_dict(), 200
    elif request.method == 'PATCH':
        json_data = request.get_json()

        try:
            for field in json_data:
                setattr(scientist, field, json_data[field])
        except ValueError as e:
            return {'error': str(e)}, 400
        
        db.session.add(scientist)
        db.session.commit()

        return scientist.to_dict(rules=['-missions']), 202
    elif request.method == 'DELETE':
        db.session.delete(scientist)
        db.session.commit()
        return {}, 204
    
@app.route('/planets')
def all_planets():
    planets = Planet.query.all()
    return [p.to_dict(rules=['-missions']) for p in planets], 200

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
        return {'error': str(e)}, 400
    
    db.session.add(new_mission)
    db.session.commit()
    return new_mission.to_dict(), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
