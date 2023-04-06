from flask import Flask, jsonify, request, json, render_template
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy as db
from datetime import *
import inspect
import atexit
from sqlalchemy import create_engine, TIMESTAMP, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from apscheduler.schedulers.background import BackgroundScheduler
from googlesheetswork import *
from external_api_cbr import *


service = get_service_sacc()
googlework =GoogleSheetWork(service_result = service)

# соединение с базой данных.
engine = create_engine('postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(user=os.environ.get('POSTGRES_USER'), passwd=os.environ.get('POSTGRES_PASSWORD'), host=os.environ.get('POSTGRES_HOST'), port=5432, db=os.environ.get('POSTGRES_DB')))

if not database_exists(engine.url):
    create_database(engine.url)         # если БД не создана, создать по указанной конфигурации в engine.

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()               # базовый класс модели
Base.query = session.query_property()

def get_data_google():
    sheet = service.spreadsheets()
    result = sheet.values().batchGet(spreadsheetId=googlework.SPREADSHEET_ID, ranges=["data_list"]).execute()['valueRanges'][0]
    return result['values']

import models

def save_data_to_db():
    answer = get_data_google()
    result = slice_list(result_list=answer)
    orders = models.OrderInfo.query.all()
    curs_dollar = get_dollar_rate()
    print('do work!')
    if not orders:
        for elem in result:
            inx = result.index(elem) + 1
            price_rub = round(curs_dollar * int(elem[2]))
            make_insert = insert_data(elem, inx, price_rub)
        return 'Ok'
    else:
        del_res = delete_data()
        for elem in result:
            inx = result.index(elem) + 1
            price_rub = round(curs_dollar * int(elem[2]))
            make_insert = insert_data(elem, inx, price_rub)
        return 'delete and Ok'

def insert_data(elem, inx, price_rub):
    kwargs = {'number_table': inx, 'number_order':int(elem[1]), 'date': elem[3], 'price_rub': price_rub, 'price_usd': int(elem[2])}
    row_instance = models.OrderInfo(**kwargs)
    session.add(row_instance)
    session.commit()
    return 'insert Ok'

def delete_data():
    num_rows_deleted = session.query(models.OrderInfo).delete()
    session.commit()
    return 'delete commit OK'

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

client = app.test_client()


@app.before_first_request
def init_scheduler():
    """ Процесс периодического запроса к googlesheets. """
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(save_data_to_db, 'interval', seconds=25, max_instances=1)
    sched.start()


@app.route('/', methods = ['GET'])
def get_start():
    """ Показать данные из базы данных в html форме. """
    return render_template('index.html')


@app.route('/data', methods = ['GET'])
def get_result():
    """ Получить данные из базы данных. """
    cast = models.OrderInfo.query.all()
    result = [data_model.to_dict(only=('number_table','number_order', 'date', 'price_usd', 'price_rub')) for data_model in cast]
    sorted_result = sorted(result, key=lambda d: d['number_table'])
    return jsonify(sorted_result)


@app.teardown_appcontext
def shutdown_session(ecxeption=None):
    session.remove()


first_req = client.get('/')             # старт маршрута через тестовый клиент flask для периодического обновления.


if __name__=='__main__':
    app.run()

