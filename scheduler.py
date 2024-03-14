import random
import schedule
import time
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Stock
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config.from_pyfile('config.py')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


def update_stock_prices():
    with app.app_context():
        session = Session()
        stocks = session.query(Stock).all()
        for stock in stocks:
            new_price = stock.price * (1 + random.uniform(-0.10, 0.10))
            print(random.uniform(-0.10, 0.10))
            new_price = max(0.01, new_price)  # Ensure price doesn't go below 0.01
            stock.price = round(new_price, 2)  # Round to two decimal places
        session.commit()
        session.close()


def job():
    print("Updating stock prices...")
    update_stock_prices()


# Schedule the job to run every 15 minutes
schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
