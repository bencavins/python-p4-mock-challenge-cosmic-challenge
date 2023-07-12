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

@app.get('/scientists')
def get_all_scientists():
    scientists = Scientist.query.all()
    data = [s.to_dict(rules=('-missions',)) for s in scientists]
    return make_response(
        jsonify(data),
        200
    )

@app.get('/planets')
def get_all_planets():
    planets = Planet.query.all()
    data = [p.to_dict(rules=('-missions',)) for p in planets]
    return make_response(
        jsonify(data),
        200
    )

@app.get('/scientists/<int:id>')
def get_scientist_by_id(id):
    scientist = Scientist.query.filter(
        Scientist.id == id
    ).first()

    if not scientist:
        return make_response(
            jsonify({"error": "Scientist not found"}), 
            404
        )
    
    return make_response(
        jsonify(scientist.to_dict()),
        200
    )

@app.post('/scientists')
def post_scientists():
    data = request.get_json()
    new_scientist = Scientist(
        name=data.get('name'),
        field_of_study=data.get('field_of_study')
    )
    db.session.add(new_scientist)
    db.session.commit()
    return make_response(
        jsonify(new_scientist.to_dict()),
        201
    )

@app.post('/missions')
def post_missions():
    data = request.get_json()
    from models import MissionError
    try:
        new_mission = Mission(
            name=data.get('name'),
            planet_id=data.get('planet_id'),
            scientist_id=data.get('scientist_id')
        )
    except MissionError:
        return make_response(
            jsonify({'error': 'validation errors'}),
            400
        )

    db.session.add(new_mission)
    db.session.commit()
    return make_response(
        jsonify(new_mission.to_dict()),
        201
    )

@app.patch('/scientists/<int:id>')
def patch_scientists_by_id(id):
    scientist = Scientist.query.filter(
        Scientist.id == id
    ).first()

    if not scientist:
        return make_response(
            jsonify({"error": "Scientist not found"}),
            404
        )
    
    data = request.get_json()
    for field in data:
        setattr(scientist, field, data[field])  # scientist[field] = data[field]
    db.session.add(scientist)
    db.session.commit()

    return make_response(
        jsonify(scientist.to_dict()),
        200
    )

@app.delete('/scientists/<int:id>')
def delete_scientist_by_id(id):
    scientist = Scientist.query.filter(
        Scientist.id == id
    ).first()

    if not scientist:
        return make_response(
            jsonify({"error": "Scientist not found"}),
            404
        )
    
    db.session.delete(scientist)
    db.session.commit()

    return make_response(
        jsonify({}),
        200
    )

if __name__ == '__main__':
    app.run(port=5555, debug=True)
