import datetime
from collections import OrderedDict
import csv
import os

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = PrimaryKeyField()
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(datetime.datetime.now())

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)
    read_csv()
    menu()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def read_csv():
    with open("inventory.csv", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        rows = list(reader)
        for row in rows:
            row["product_price"] = int(row["product_price"].replace("$", "").replace(".", ""))
            row["product_quantity"] = int(row["product_quantity"])
            row["date_updated"] = (datetime.datetime.strptime(row["date_updated"], "%m/%d/%Y"))
            try:
                Product.create(
                    product_name=row["product_name"],
                    product_price=row["product_price"],
                    product_quantity=row["product_quantity"],
                    date_updtaed=row["date_updated"]).save()
            except IntegrityError:
                product_record = Product.get(product_name=row["product_name"])
                product_record.product_name = row["product_name"]
                product_record.product_price = row["product_price"]
                product_record.product_quantity = row["product_quantity"]
                product_record.date_updated = row["date_updated"]
                product_record.save()
                if product_record != row["product_name"]:
                    product_record.update(product_record.date_updated)


def menu():
    choice = None
    while choice != "x":
        print("="*22)
        print("ENTER 'x' TO EXIT.")
        print("="*22)
        print()
        for key, value in user_menu.items():
            print("{}) {}".format(key, value.__doc__))
        print()
        print("=" * 22)
        choice = input("ENTER AN OPTION: ").lower()
        if choice in user_menu.keys():
            clear()
            user_menu[choice]()
        elif choice not in user_menu:
            print("\nINVALID OPTION. TRY AGAIN.")
            continue


def add_new_product():
    """Add New Product"""


def view_products(search_query=None):
    """View Product Entries"""
    clear()
    products = Product.select().order_by(Product.product_id.desc())
    if search_query:
        products = Product.select().where(Product.product_id == search_query)
        for product in products:
            clear()
            print("="*22)
            print(
                f"Product ID#: {product.product_id}"
                f"Product Name: {product.product_name}"
                f"Product Quantity: {product.product_quantity}"
                f"Product Price: {product.product_price} cents"
                f"Last Updated: {product.date_updated.strftime('%d-%m-%Y')}")
            print("="*22)
            print("\n")
            print("n) Next Product")
            print("x) Main Menu")
            print("\n")
            option = input("\nENTER AN OPTION: ")
            if option == "x":
                break
            elif option == "n":
                clear()
            else:
                print("INVALID OPTION. TRY AGAIN")
                continue


def backup_data():
    """Backup Database"""


user_menu = OrderedDict([
    ("v", view_products),
    ("a", add_new_product),
    ("b", backup_data),
])


if __name__ == "__main__":
    initialize()
