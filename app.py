import datetime

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = None
    product_name = None
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(datetime.datetime.now())

    class Meta:
        database = db


if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
