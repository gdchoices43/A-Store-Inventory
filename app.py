from datetime import datetime
import csv
import os
import sys
from collections import OrderedDict

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=255, unique=False)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db


def load_csv():
    with open("inventory.csv") as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)
        for row in rows[1:]:
            Product.create(
                product_name=row[0],
                product_price=strip_price(row[1]),
                product_quantity=row[2],
                date_updated=datetime.strptime(row[3], "%m/%d/%Y")
            )


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def strip_price(price):
    return price.strip("$").replace(".", "")


def menu():
    choice = None
    while choice != "x":
        print("\n\nSTORE INVENTORY DATABASE")
        print("=" * 22)
        print("ENTER 'x' TO EXIT.")
        print("=" * 22)
        print()
        for key, value in menu_dict.items():
            print("{}) {}".format(key, value.__doc__))
        print()
        print("=" * 22)
        choice = input("ENTER AN OPTION: ").lower()
        if choice in menu_dict.keys():
            clear()
            menu_dict[choice]()
        elif choice not in menu_dict:
            print("\nINVALID OPTION. TRY AGAIN.")
            continue
        else:
            print("EXITING STORE INVENTORY...")
            sys.exit()


def view_product():
    """View/Search products"""


def add_new_product():
    """Add New Products"""


def backup_inventory():
    """Backup Inventory"""


menu_dict = OrderedDict([
    ("V:", view_product),
    ("A:", add_new_product),
    ("B:", backup_inventory)
])


if __name__ == "__main__":
    db.connect()
    db.create_tables([Product], safe=True)
    menu()
