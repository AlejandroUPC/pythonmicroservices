from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaConsumer
from json import loads
import datetime
from multiprocessing import Process
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db_cust_metrics/customer_metrics'
CORS(app)
print(__name__)
db = SQLAlchemy(app)


class CustomerMetrics(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    total_tx = db.Column(db.Integer)
    last_month_volume = db.Column(db.Float)
    current_month = db.Column(
        db.Integer, default=datetime.datetime.today().month)
    current_year = db.Column(
        db.Integer, default=datetime.datetime.today().year)
    n_cash_payment = db.Column(db.Integer)
    n_card_payment = db.Column(db.Integer)


def _insertCustomerMetrics(json_data):
    get_user = CustomerMetrics.query.filter_by(
        customer_id=json_data['customer_id']).first()
    if get_user:
        get_user.total_tx += json_data['price']
        if __is_current_month(get_user.current_year, get_user.current_month):
            print('We are in the same month! Updating')
            get_user.last_month_volume += json_data['price']
        else:
            get_user.last_month_volume = json_data['price']
        if json_data['pay_method'] == 1:
            get_user.n_cash_payment += 1
        else:
            get_user.n_card_payment += 1
        print(f'AFTER \n {get_user}')
        db.session.add(get_user)
        db.session.commit()
    else:
        print('This is a new user')
        cash_p = 0
        card_p = 0
        if json_data['pay_method'] == 1:
            cash_p = 1
            card_p = 0
        else:
            cash_p = 0
            card_p = 1

        new_user = CustomerMetrics(
            customer_id=json_data['customer_id'], total_tx=json_data['price'], n_cash_payment=cash_p, n_card_payment=card_p,
            last_month_volume = json_data['price'])
        print(new_user)
        db.session.add(new_user)
        db.session.commit()


def __is_current_month(dt_year: int, dt_month: int) -> bool:
    current_dt = datetime.datetime.now()
    if (dt_year == current_dt.year) & (dt_month == current_dt.month):
        return True
    return False


def kafka_consumer() -> None:
    print('Kafka has started to listen')
    try:
        transaction_consumer = KafkaConsumer('transaction_record', bootstrap_servers=[
            'kafka_broker:29092'], enable_auto_commit=True,
            group_id='client_metrics', value_deserializer=lambda x: loads(x.decode('utf-8')))
        for msg in transaction_consumer:
            try:
                _insertCustomerMetrics(msg.value)
            except Exception as e:
                print(f'Error inserting data {e}')
    except Exception as e:
        print(f'Error on  Kafka Consumer\n {e}')


if __name__ == '__main__':
    print(' Starting from __main__')
    thread_kafka = Process(target=kafka_consumer)
    thread_kafka.start()
    app.run(debug=True, host='0.0.0.0')
