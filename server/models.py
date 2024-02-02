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

    # Add relationship

    # Add serialization rules


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    # Add database columns
    id = db.Column(db.Integer, primary_key=True)

    # Add relationship

    # Add serialization rules


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    # Add database columns
    id = db.Column(db.Integer, primary_key=True)

    # Add relationships

    # Add serialization rules
