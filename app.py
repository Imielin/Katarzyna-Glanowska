from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text
import statistics
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from numpy import genfromtxt
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
#config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'app.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)
db.drop_all()

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=';', dtype=str)
    print(data.tolist())
    return data.tolist()

Base = declarative_base()

class Adult_Base(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    __tablename__ = 'ADULTS_TABLE'
    ID = Column(Integer, primary_key=True, nullable=False)
    AGE = Column(Integer)
    WORKCLASS = Column(String)
    EDUCATION = Column(String)
    MARTIAL_STATUS = Column(String)
    OCCUPATION = Column(String)
    RELATIONSHIP = Column(String)
    RACE = Column(String)
    SEX = Column(String)
    HOURS_PER_WEEK = Column(Integer)
    NATIVE_COUNTRY = Column(String)
    INCOME = Column(String)

    def __init__(self,AGE,WORKCLASS,EDUCATION,MARTIAL_STATUS,OCCUPATION,RELATIONSHIP,RACE,SEX,HOURS_PER_WEEK,NATIVE_COUNTRY,INCOME):
        self.AGE = AGE
        self.WORKCLASS = WORKCLASS
        self.EDUCATION = EDUCATION
        self.MARTIAL_STATUS = MARTIAL_STATUS
        self.OCCUPATION = OCCUPATION
        self.RELATIONSHIP = RELATIONSHIP
        self.RACE = RACE
        self.SEX = SEX
        self.HOURS_PER_WEEK = HOURS_PER_WEEK
        self.NATIVE_COUNTRY = NATIVE_COUNTRY
        self.INCOME = INCOME


'''
db.create_all()
'''

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Adult_Base).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Adult_Base).all()

    # Some simple statistics for sample questions
    f_age = []
    f_martial_status = []
    f_hours_per_week = []
    f_income = []
    f_above_50k = 0
    m_age = []
    m_martial_status = []
    m_hours_per_week = []
    m_income = []
    m_above_50k = 0


    for el in fd_list:
        if(el.SEX==' Female'):
            f_age.append(int(el.AGE))
            f_martial_status.append(el.MARTIAL_STATUS)
            f_hours_per_week.append(el.HOURS_PER_WEEK)
            f_income.append(el.INCOME)
        elif(el.SEX==' Male'):
            m_age.append(int(el.AGE))
            m_martial_status.append(el.MARTIAL_STATUS)
            m_hours_per_week.append(el.HOURS_PER_WEEK)
            m_income.append(el.INCOME)
        else:
            print("Error")

    for el in f_income:
        if(el == ' >50K'):
            f_above_50k = f_above_50k +1


    for el in m_income:
        if (el == ' >50K'):
            m_above_50k = m_above_50k + 1

    if len(f_age) > 0:
        f_mean_age = statistics.mean(f_age)
    else:
        f_mean_age = 0

    if len(m_age) > 0:
        m_mean_age = statistics.mean(m_age)
    else:
        m_mean_age = 0

    if len(f_hours_per_week) > 0:
        f_mean_hours_per_week = statistics.mean(f_hours_per_week)
    else:
        f_mean_hours_per_week = 0

    if len(m_hours_per_week) > 0:
        m_mean_hours_per_week = statistics.mean(m_hours_per_week)
    else:
        m_mean_hours_per_week = 0

    # Prepare data for google charts
    data = [['Women', len(f_age)], ['Men', len(m_age)]]
    data_mean_age = [['Women', f_mean_age], ['Men', m_mean_age]]
    data_mean_hours = [['Women', f_mean_hours_per_week], ['Men', m_mean_hours_per_week]]
    data_above_50k = [['Women', f_above_50k], ['Men', m_above_50k]]

    return render_template('result.html', data=data, data_mean_age = data_mean_age, data_mean_hours = data_mean_hours, data_above_50k = data_above_50k)


@app.route("/result1", methods=['POST'])
def show_result1():
    # Get data from FORM
    attribute = request.form['sel']
    if(str(attribute) == 'AGE'):
        atr_list = db.session.query(Adult_Base.AGE).all()
    elif(str(attribute) == 'WORKCLASS'):
        atr_list = db.session.query(Adult_Base.WORKCLASS).all()
    elif (str(attribute) == 'EDUCATION'):
        atr_list = db.session.query(Adult_Base.EDUCATION).all()
    elif (str(attribute) == 'OCCUPATION'):
        atr_list = db.session.query(Adult_Base.OCCUPATION).all()
    elif (str(attribute) == 'RELATIONSHIP'):
        atr_list = db.session.query(Adult_Base.RELATIONSHIP).all()
    elif (str(attribute) == 'RACE'):
        atr_list = db.session.query(Adult_Base.RACE).all()
    elif (str(attribute) == 'HOURS_PER_WEEK'):
        atr_list = db.session.query(Adult_Base.HOURS_PER_WEEK).all()
    elif (str(attribute) == 'SEX'):
        atr_list = db.session.query(Adult_Base.SEX).all()
    elif (str(attribute) == 'NATIVE_COUNTRY'):
        atr_list = db.session.query(Adult_Base.NATIVE_COUNTRY).all()
    else:
        atr_list = db.session.query(Adult_Base.SEX).all()

    income_list = db.session.query(Adult_Base.INCOME).all()
    dict = {}

    for i in range(len(atr_list)):
        if(income_list[i] == income_list[7]):

            if(str(atr_list[i]) in dict):
                value1 = dict[str(atr_list[i])]
                value2 = value1+1
                temporary_dict ={str(atr_list[i]): int(value2)}
                dict.update(temporary_dict)
                temporary_dict.clear()
            else:
                value = 1
                temporary_dict = {str(atr_list[i]): int(value)}
                dict.update(temporary_dict)
                temporary_dict.clear()
    length = int(len(dict))
    tab = [[ 0 ]*2 for i in range(length)]

    licznik = 0
    for (string, n) in dict.items():
        length = (len(string))

        if(length <=5):
            str1 = string[1:(length-2)]
        else:
            str1 = string[3:(length - 3)]
        tab[licznik][0] = str(str1)
        tab[licznik][1] = n
        licznik = licznik+1


    return render_template('result1.html', tab=tab)


if __name__ == "__main__":
    # Create the database
    engine = create_engine('sqlite:///formdata.db')

    # Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    if not (engine.dialect.has_table(engine.connect(), "ADULTS_TABLE")):
        Base.metadata.create_all(engine)

        file_name = "adult1.csv"
        data = Load_Data(file_name)

        for i in data:
            record = Adult_Base(**{
                'AGE': int(i[0]),
                'WORKCLASS': i[1],
                'EDUCATION': i[2],
                'MARTIAL_STATUS': i[3],
                'OCCUPATION': i[4],
                'RELATIONSHIP': i[5],
                'RACE': i[6],
                'SEX': i[7],
                'HOURS_PER_WEEK': int(i[8]),
                'NATIVE_COUNTRY': i[9],
                'INCOME': i[10]
            })
            s.add(record)  # Add all the records
        s.commit()  # Attempt to commit all the records

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    s.close()  # Close the connection
