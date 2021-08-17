from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import pymysql
import psycopg2
import json
import postgis

#podawanie danych pobieranych z kursora jako słowników

def rows_as_dicts(cursor):
    col_names = [i[0] for i in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor]

def WGS_json_from_db(*, columns, table, connection):
    get_geom = "ST_AsGeoJSON(ST_Transform(geom, '+proj=tmerc +lat_0=0 +lon_0=19 +k=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs', 4326)) as geom"
    dane = rows_as_dicts(connection.execute("""select {}, {} from {}""".format(columns, get_geom, table)).cursor)
    dane = json.dumps(dane)
    return dane

def get_questions(*, group, table, connection):
    if(group == "all"):
        questions = rows_as_dicts(connection.execute("""select pytanie, odp_p, odp_n, grupa from {}""".format(table)).cursor)
    else:
        questions = rows_as_dicts(connection.execute("""select pytanie, odp_p, odp_n from {} where grupa = '{}' """.format(table, group)).cursor)

    # for question in questions:
    #     questions[0]["odp_p"] = questions[0]["odp_p"].split("#")
    #     questions[0]["odp_n"] = questions[0]["odp_n"].split("#")

    questions = json.dumps(questions)
    return questions