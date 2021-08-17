# from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
# from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy
# import pymysql
# import psycopg2
# import mod as m
# import json
# import postgis
# import xlrd
from operator import truediv
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import pymysql
import psycopg2
import mod as m
import json
import postgis
import smtplib, ssl
from email.mime.text import MIMEText

get_geom = "ST_AsGeoJSON(ST_Transform(geom, '+proj=tmerc +lat_0=0 +lon_0=19 +k=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs', 4326)) as geom"
db = SQLAlchemy(session_options={'autocommit': True})

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://surnatpol:sopiwihojo@matrix.umcs.pl:5432/surnatpol"
app.config['SECRET_KEY'] = 'test'
db.init_app(app)

db

@app.route('/send_mail/<mail>', methods=['GET', 'POST'])
def mail(mail):
    conn = db.session.connection()
    if request.method == "POST":
        email = mail
        if ((conn.execute(""" select exists (select 1 from mails where mail = '{}') """.format(email)).first()[0]) is True):
            return "wiadomość została wysłana"
        else:
            conn.execute(""" insert into mails (mail) values ('{}') """.format(email))
            return "wiadomość została wysłana, mail dodano do bazy"
    else:
         return "stand by"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/choice')
def choice():
    return render_template('choice.html')

#dodanie wyników do bazy, wysłanie maila
###################################################################################################################################

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    conn = db.session.connection()
    if request.method == "POST":
        email = request.form['mail']
        conn.execute(""" insert into kontakty values ({}) """.format(email))
    return render_template('kontakty.html')
    
#nauka
####################################################################################################################################

@app.route('/learn')
def learn():
    return render_template('wybornauki.html')

@app.route('/learn/coal', methods=['GET', 'POST'])
def learn_coal():
    conn = db.session.connection()

    w_kamienny = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="wegiel_kamienny", connection=conn) 
    w_brunatny = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="wegiel_brunatny", connection=conn)

    k_kamienny = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_wegiel_kamienny", connection=conn)
    k_brunatny = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_wegiel_brunatny", connection=conn)

    wegle = [w_kamienny, k_kamienny, w_brunatny, k_brunatny]
    return render_template('naukawegiel.html', dane = wegle)


@app.route('/learn/oil', methods=['GET', 'POST'])
def learn_oil():
    conn = db.session.connection()

    k_torf = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_torf", connection=conn)

    ropa = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, uwagi, grupa", table="ropa_naftowa", connection=conn) 
    k_ropa = m.WGS_json_from_db(columns="id, kopalnia, grupa", table="kopalnie_ropa_naftowa", connection=conn)

    ropa_torf = [k_torf, ropa, k_ropa]
    return render_template('naukatorfropa.html', dane = ropa_torf)


@app.route('/learn/gas', methods=['GET', 'POST'])
def learn_gas():
    conn = db.session.connection()

    gaz = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, uwagi, grupa", table="gaz_ziemny", connection=conn)
    k_gaz = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_gaz_ziemny", connection=conn)

    gazy = [gaz, k_gaz]
    return render_template('naukagaz.html', dane = gazy)


@app.route('/learn/ores', methods=['GET', 'POST'])
def learn_ores():
    conn = db.session.connection()

    copper = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_miedzi", connection=conn)
    k_copper = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_miedz", connection=conn)

    silver = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_srebra", connection=conn)

    iron = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_zelaza", connection=conn)

    gold = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_zlota", connection=conn)
    k_gold = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_zloto", connection=conn)

    ores = [iron, silver, copper, k_copper, gold, k_gold]
    return render_template('naukarudy.html', dane = ores)


@app.route('/learn/tin', methods=['GET', 'POST'])
def learn_tin():
    conn = db.session.connection()

    cyna = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="cyna", connection=conn)
    cynk = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_cynk_olow", connection=conn)
    k_cyna = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_cyna", connection=conn)

    cyna_olow = [cynk, cyna, k_cyna]
    return render_template('naukacynaolow.html', dane = cyna_olow)


@app.route('/learn/sulfur', methods=['GET', 'POST'])
def learn_sulfur():
    conn = db.session.connection()

    siarka = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="siarka", connection=conn)
    k_siarka = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_siarka", connection=conn)

    siarki = [siarka, k_siarka]
    return render_template('naukasiarka.html', dane = siarki)


@app.route('/learn/salt', methods=['GET', 'POST'])
def learn_salt():
    conn = db.session.connection()

    s_kam = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="sol_kamienna", connection=conn)
    k_s_kam = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_sol_kamienna", connection=conn)

    s_pot = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="sol_potasowa", connection=conn)
    k_s_pot = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_sol_potasowa", connection=conn)

    sole = [s_kam, k_s_kam, s_pot, k_s_pot]
    return render_template('naukasol.html', dane = sole)


@app.route('/learn/limestone', methods=['GET', 'POST'])
def learn_limestone():
    conn = db.session.connection()

    wap_marg = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="wapienie_margle", connection=conn)
    k_wap_marg = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_wapienie_margle", connection=conn)

    stones = [wap_marg, k_wap_marg]
    return render_template('naukawapieniemargle.html', dane = stones)


@app.route('/learn/plaster', methods=['GET', 'POST'])
def learn_plaster():
    conn = db.session.connection()

    glina = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="gliny", connection=conn)
    k_glina = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_gliny", connection=conn)

    gips = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="gips_anhydryt", connection=conn)
    k_gips = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_gips_anhydryt", connection=conn)

    gliny = [glina, k_glina, gips, k_gips]
    return render_template('naukaglinygips.html', dane = gliny)


@app.route('/learn/sand', methods=['GET', 'POST'])
def learn_sand():
    conn = db.session.connection()

    piasek = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="piaski_zwiry", connection=conn)
    k_piasek = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_piaski_zwiry", connection=conn)

    sands = [piasek, k_piasek]
    return render_template('naukapiaskizwiry.html', dane = sands)


@app.route('/learn/water', methods=['GET', 'POST'])
def learn_water():
    conn = db.session.connection()

    wody_l = m.WGS_json_from_db(columns="id, grupa", table="wody_lecznicze", connection=conn)
    wody_t = m.WGS_json_from_db(columns="id, grupa", table="wody_termalne", connection=conn)
    solanki = m.WGS_json_from_db(columns="id, grupa", table="solanki", connection=conn)

    wody = [wody_l, wody_t, solanki]
    return render_template('naukawody.html', dane = wody)


@app.route('/learn/industry', methods=['GET', 'POST'])
def learn_industry():
    conn = db.session.connection()

    ok_prze = m.WGS_json_from_db(columns="id, nazwa", table="okregi_przemyslowe_polska", connection=conn)

    przem = [ok_prze]
    return render_template('naukaokregi.html', dane = przem)

@app.route('/learn/oze')
def learn_oze():
    return render_template('naukaoze.html')

#test
########################################################################################################

@app.route('/test')
def test():
    return render_template('wybortest.html')

@app.route('/test/end', methods=['GET', 'POST'])
def test_end():
    conn = db.session.connection()
    pytania = m.get_questions(table="pytania", group="all", connection=conn)
    return render_template('testEND.html', dane = pytania)

@app.route('/test/chem', methods=['GET', 'POST'])
def test_chem():
    conn = db.session.connection()
    pytania = m.get_questions(table="pytania", group='c', connection=conn)
    return render_template('test_chem.html', dane = pytania)

@app.route('/test/ener', methods=['GET', 'POST'])
def test_ener():
    conn = db.session.connection()
    pytania = m.get_questions(table="pytania", group='e', connection=conn)
    return render_template('test_ener.html', dane = pytania)

@app.route('/test/met', methods=['GET', 'POST'])
def test_met():
    conn = db.session.connection()
    pytania = m.get_questions(table="pytania", group='m', connection=conn)
    return render_template('test_met.html', dane = pytania)

@app.route('/test/skal', methods=['GET', 'POST'])
def test_skal():
    conn = db.session.connection()
    pytania = m.get_questions(table="pytania", group='s', connection=conn)
    return render_template('test_skal.html', dane = pytania)

@app.route('/test/wodysol', methods=['GET', 'POST'])
def test_wodysol():
    conn = db.session.connection()
    pytania = m.get_questions(table="pytania", group='w', connection=conn)
    return render_template('test_wodysol.html', dane = pytania)

#mapa
###########################################################################

@app.route('/map', methods=['GET', 'POST'])
def map():
    conn = db.session.connection()
    
    wody_l = m.WGS_json_from_db(columns="id, grupa", table="wody_lecznicze", connection=conn)
    wody_t = m.WGS_json_from_db(columns="id, grupa", table="wody_termalne", connection=conn)
    solanki = m.WGS_json_from_db(columns="id, grupa", table="solanki", connection=conn)
    wody = [wody_l, wody_t, solanki]

    ok_prze = m.WGS_json_from_db(columns="id, nazwa", table="okregi_przemyslowe_polska", connection=conn)
    przem = [ok_prze]

    # piasek = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="piaski_zwiry", connection=conn)
    # k_piasek = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_piaski_zwiry", connection=conn)
    # sands = [piasek, k_piasek]

    glina = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="gliny", connection=conn)
    k_glina = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_gliny", connection=conn)
    gips = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="gips_anhydryt", connection=conn)
    k_gips = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_gips_anhydryt", connection=conn)
    gliny = [glina, k_glina, gips, k_gips]

    wap_marg = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="wapienie_margle", connection=conn)
    k_wap_marg = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_wapienie_margle", connection=conn)
    stones = [wap_marg, k_wap_marg]

    s_kam = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="sol_kamienna", connection=conn)
    k_s_kam = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_sol_kamienna", connection=conn)
    s_pot = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="sol_potasowa", connection=conn)
    k_s_pot = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_sol_potasowa", connection=conn)
    sole = [s_kam, k_s_kam, s_pot, k_s_pot]

    siarka = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="siarka", connection=conn)
    k_siarka = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_siarka", connection=conn)
    siarki = [siarka, k_siarka]

    cyna = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="cyna", connection=conn)
    cynk = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_cynk_olow", connection=conn)
    k_cyna = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_cyna", connection=conn)
    cyna_olow = [cynk, cyna, k_cyna]

    copper = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_miedzi", connection=conn)
    k_copper = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_miedz", connection=conn)
    silver = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_srebra", connection=conn)
    iron = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_zelaza", connection=conn)
    gold = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="ruda_zlota", connection=conn)
    k_gold = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_zloto", connection=conn)
    ores = [iron, silver, copper, k_copper, gold, k_gold]

    gaz = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, uwagi, grupa", table="gaz_ziemny", connection=conn)
    k_gaz = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_gaz_ziemny", connection=conn)
    gazy = [gaz, k_gaz]

    k_torf = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_torf", connection=conn)
    ropa = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, uwagi, grupa", table="ropa_naftowa", connection=conn) 
    k_ropa = m.WGS_json_from_db(columns="id, kopalnia, grupa", table="kopalnie_ropa_naftowa", connection=conn)
    ropa_torf = [k_torf, ropa, k_ropa]

    w_kamienny = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="wegiel_kamienny", connection=conn) 
    w_brunatny = m.WGS_json_from_db(columns="id, nazwa, pow, czynne, lokal, uwagi, grupa", table="wegiel_brunatny", connection=conn)
    k_kamienny = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_wegiel_kamienny", connection=conn)
    k_brunatny = m.WGS_json_from_db(columns="id, kopalnie, grupa", table="kopalnie_wegiel_brunatny", connection=conn)
    wegle = [w_kamienny, k_kamienny, w_brunatny, k_brunatny]

    full_data = [wody, przem, gliny, stones, sole, siarki, cyna_olow, ores, gazy, ropa_torf, wegle]

    return render_template('sandbox.html', dane = full_data)

###########################################################################

if __name__ == "__main__":
    app.run(host= '192.168.1.6')