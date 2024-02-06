from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    # Add database columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    missions = db.relationship('Mission', back_populates='planet', cascade='all, delete-orphan')

    # Add serialization rules
    serialize_rules = ['-missions.planet']

    def __repr__(self) -> str:
        return f"<Planet {self.name}>"


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    # Add database columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String)

    # Add relationship
    missions = db.relationship(
        'Mission', 
        back_populates='scientist',
        cascade='all, delete-orphan'  # delete the mission if the scientist is deleted
    )

    # Add serialization rules
    serialize_rules = ['-missions.scientist']

    @validates('name', 'field_of_study')
    def validate_name_fos(self, key, new_value):
        if new_value is None:
            raise ValueError(f'{key} cannot be null')
        if len(new_value) == 0:
            raise ValueError(f'{key} must have at least one char')
        return new_value

    def __repr__(self) -> str:
        return f"<Scientist {self.name}>"


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    # Add database columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    # Add relationships
    scientist = db.relationship('Scientist', back_populates='missions')
    planet = db.relationship('Planet', back_populates='missions')

    # Add serialization rules
    serialize_rules = ['-scientist.missions', '-planet.missions']

    @validates('name', 'scientist_id', 'planet_id')
    def validate_fields(self, key, new_value):
        if new_value is None:
            raise ValueError(f'{key} cannot be null')
        return new_value

    def __repr__(self) -> str:
        return f"<Mission {self.name} {self.scientist_id} {self.planet_id}>"
