import datetime
from collections import OrderedDict
import csv
import os

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = AutoField(primary_key=True)
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(datetime.datetime.now())

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)
    db.close()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def read_csv():
    # Opening the inventory.csv file
    with open("inventory.csv") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        product_row = list(reader)


def menu():
    # Setting our choice variable to None
    choice = None
    # Starting the while loop to see if the user has chosen "x" to quit
    while choice != "x":
        clear()
        # We print out this message to let them know they can type "x" to quit
        print("="*22)
        print("Enter 'x' to Exit.\n")
        # Loop through each item in our dictionary, the key and the value
        for key, value in user_menu.items():
            # Then we are gonna print out the key and the values ex: key= A)  value= Add an entry
            print("{}) {}".format(key, value.__doc__))
        # Asking the user to choose an option,we also lowercase it and strip it
        print("=" * 22)
        choice = input("\nEnter an OPTION: ").lower().strip()
        # We check if it's "x" if it's not "x" we come back to our menu, we find the function
        # they have selected and we run it
        if choice in user_menu:
            clear()
            user_menu[choice]()


def view():
    """View product details"""


def add_new_product():
    """Add new product"""


def backup_data():
    """Backup Database"""


user_menu = OrderedDict([
    ("v", view),
    ("a", add_new_product),
    ("b", backup_data),
])


if __name__ == "__main__":
    initialize()
    backup_data()

