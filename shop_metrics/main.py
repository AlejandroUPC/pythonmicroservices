from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaConsumer
from json import loads
import datetime
from multiprocessing import Process
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db_shop_metrics/shop_metrics'
CORS(app)

db = SQLAlchemy(app)


class ShopMetrics(db.Model):
    supermarket_id = db.Column(
        db.Integer, primary_key=True, autoincrement=False)
    total_volume = db.Column(db.Integer)
    total_tx = db.Column(db.Float, default=0)
    last_tx = db.Column(
        db.DateTime, default=datetime.datetime.utcnow)
    n_cash_payment = db.Column(db.Integer)
    n_card_payment = db.Column(db.Integer)


def _insertShopMetrics(json_data):
    get_sp = ShopMetrics.query.filter_by(
        supermarket_id=json_data['sp_owner']).first()
    if get_sp:
        get_sp.total_volume += json_data['price']
        get_sp.total_tx += 1
        if json_data['pay_method'] == 1:
            get_sp.n_cash_payment += 1
        else:
            get_sp.n_card_payment += 1
        db.session.add(get_sp)
        db.session.commit()
    else:
        cash_p = 0
        card_p = 0
        if json_data['pay_method'] == 1:
            cash_p = 1
            card_p = 0
        else:
            cash_p = 0
            card_p = 1

        new_user = ShopMetrics(
            supermarket_id=json_data['sp_owner'], total_volume=json_data['price'], total_tx=1, 
            n_cash_payment=cash_p, n_card_payment=card_p)
        db.session.add(new_user)
        db.session.commit()


def kafka_consumer() -> None:
    print('Kafka has started to listen on the shop_metrics')
    try:
        transaction_consumer = KafkaConsumer('transaction_record', bootstrap_servers=[
            'kafka_broker:29092'], enable_auto_commit=True,
            group_id='shop_metrics', value_deserializer=lambda x: loads(x.decode('utf-8')))
        for msg in transaction_consumer:
            try:
                _insertShopMetrics(msg.value)
            except Exception as e:
                print(f'Error inserting data {e}')
    except Exception as e:
        print(f'Error on  Kafka Consumer\n {e}')


if __name__ == '__main__':
    print(' Starting from __main__')
    thread_kafka = Process(target=kafka_consumer)
    thread_kafka.start()
    app.run(debug=True, host='0.0.0.0')
