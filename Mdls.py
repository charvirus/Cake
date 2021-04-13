from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DEFAULT']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)


class Patient(db.Model):
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key = True)
    gender_concept_id = db.Column(db.Integer)
    birth_datetime = db.Column(db.TIMESTAMP)
    race_concept_id = db.Column(db.Integer)
    ethnicity_source_value = db.Column(db.String)


class Death(db.Model):
    __tablename__ = 'death'
    person_id = db.Column(db.Integer, primary_key = True)
    death_date = db.Column(db.TIMESTAMP)
    cause_source_value = db.Column(db.Integer)


class Visit(db.Model):
    __tablename__ = 'visit_occurrence'
    visit_occurrence_id = db.Column(db.Integer, primary_key = True)
    person_id = db.Column(db.Integer)
    visit_concept_id = db.Column(db.Integer)
    visit_start_datetime = db.Column(db.TIMESTAMP)
    visit_end_datetime = db.Column(db.TIMESTAMP)


class Condition(db.Model):
    __tablename__ = 'condition_occurrence'
    person_id = db.Column(db.Integer, primary_key = True)
    condition_concept_id = db.Column(db.Integer)
    condition_start_datetime = db.Column(db.TIMESTAMP)
    condition_end_datetime = db.Column(db.TIMESTAMP)
    visit_occurrence_id = db.Column(db.Integer)


class Drug(db.Model):
    __tablename__ = 'drug_exposure'
    person_id = db.Column(db.Integer)
    drug_concept_id = db.Column(db.Integer, primary_key = True)
    drug_exposure_start_datetime = db.Column(db.TIMESTAMP)
    drug_exposure_end_datetime = db.Column(db.TIMESTAMP)
    visit_occurrence_id = db.Column(db.Integer)
