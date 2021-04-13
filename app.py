from flask import Flask, render_template
from flask_paginate import Pagination, get_page_parameter
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, TIMESTAMP
from Mdls import Patient, Death, Visit, Condition, Drug
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DEFAULT']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)

ROW_PER_PAGE = 20


@app.route('/patient/total')
def P_T():
    result = db.session.query(func.count('*')).select_from(Patient).scalar()
    print(result)
    return render_template('patient/total.html', result=result)


@app.route('/patient/gender')
def P_G():
    result = db.session.query(Patient.gender_concept_id, func.count(Patient.gender_concept_id)).group_by(
        Patient.gender_concept_id).all()
    print(result)
    return render_template('patient/gender.html', results=result)


@app.route('/patient/race')
def P_R():
    result = db.session.query(Patient.race_concept_id, func.count(Patient.race_concept_id)).group_by(
        Patient.race_concept_id).all()
    print(result)
    return render_template('patient/gender.html', results=result)


@app.route('/patient/ethnicity')
def P_E():
    result = db.session.query(Patient.ethnicity_source_value, func.count(Patient.ethnicity_source_value)).group_by(
        Patient.ethnicity_source_value).all()
    print(result)
    return render_template('patient/ethnicity.html', results=result)


@app.route('/patient/death')
def P_X():
    result = db.session.query(func.count('*')).select_from(Death).scalar()
    print(result)
    return render_template('patient/death.html', result=result)


@app.route('/visit/type')
def V_T():
    result = db.session.query(Visit.visit_concept_id, func.count(Visit.visit_concept_id)).group_by(
        Visit.visit_concept_id).all()
    print(result)
    return render_template('visit/type.html', results=result)


@app.route('/visit/gen')
def V_G():
    result = db.session.query(Patient.gender_concept_id, func.count(Visit.person_id)).filter(
        Patient.person_id == Visit.person_id).group_by(
        Patient.gender_concept_id).all()
    print(result)
    return render_template('visit/gender.html', results=result)


@app.route('/visit/race')
def V_R():
    result = db.session.query(Patient.race_concept_id, func.count(Visit.person_id)).filter(
        Patient.person_id == Visit.person_id).group_by(
        Patient.race_concept_id).all()
    print(result)
    return render_template('visit/race.html', results=result)


@app.route('/visit/ethnicity')
def V_E():
    result = db.session.query(Patient.ethnicity_source_value, func.count(Visit.person_id)).filter(
        Patient.person_id == Visit.person_id).group_by(
        Patient.ethnicity_source_value).all()
    print(result)
    return render_template('visit/ethnicity.html', results=result)


@app.route('/visit/age')
def V_A():
    result = db.session.query(func.date_trunc('decade', Patient.birth_datetime), func.count(Visit.person_id)).filter(
        Patient.person_id == Visit.person_id).group_by(
        func.date_trunc('decade', Patient.birth_datetime)).order_by(
        func.date_trunc('decade', Patient.birth_datetime)).all()
    print(result)
    return render_template('visit/age.html', results=result)


@app.route('/search/person/<type>/<id>')
def Sch_P(type, id):
    if type == 'gender':
        info = db.session.query(Patient.person_id, Patient.gender_concept_id, Patient.birth_datetime,
                                Patient.race_concept_id, Patient.ethnicity_source_value).filter(
            Patient.gender_concept_id == id).all()

        return render_template('search/person/result.html', results=info)
    elif type == 'race':
        info = db.session.query(Patient.person_id, Patient.gender_concept_id, Patient.birth_datetime,
                                Patient.race_concept_id, Patient.ethnicity_source_value).filter(
            Patient.race_concept_id == id).all()

        return render_template('search/person/result.html', results=info)
    elif type == 'ethnicity':
        info = db.session.query(Patient.person_id, Patient.gender_concept_id, Patient.birth_datetime,
                                Patient.race_concept_id, Patient.ethnicity_source_value).filter(
            Patient.ethnicity_source_value == id).all()

        return render_template('search/person/result.html', results=info)


@app.route('/search/visit/<id>')
def Sch_V(id):
    info = db.session.query(Visit.visit_occurrence_id, Visit.person_id, Visit.visit_concept_id,
                            Visit.visit_start_datetime, Visit.visit_end_datetime).filter(
        Visit.visit_concept_id == id).all()

    return render_template('search/Visit/result.html', results=info)


@app.route('/search/condition/<id>')
def Sch_C(id):
    info = db.session.query(Condition.person_id, Condition.condition_concept_id, Condition.condition_start_datetime,
                            Condition.condition_end_datetime, Condition.visit_occurrence_id).filter(
        Condition.condition_concept_id == id).all()

    return render_template('search/Condition/result.html', results=info)


@app.route('/search/drug/<id>')
def Sch_D(id):
    info = db.session.query(Drug.person_id, Drug.drug_concept_id, Drug.drug_exposure_start_datetime,
                            Drug.drug_exposure_end_datetime, Drug.visit_occurrence_id).filter(
        Drug.drug_concept_id == id).all()

    return render_template('search/Condition/result.html', results=info)


if __name__ == "__main__":
    app.run()
