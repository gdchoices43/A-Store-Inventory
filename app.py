import datetime
from collections import OrderedDict
import csv
import os

from peewee import *

# Initializing the database and name
db = SqliteDatabase("inventory.db")


# Create Product Model for our app
class Product(Model):
    # Setting the attributes to the proper fields for the Product Model
    product_id = AutoField(primary_key=True)
    product_name = TextField()
    product_quantity = IntegerField(default=0)
    product_price = IntegerField()
    date_updated = DateTimeField(datetime.datetime.now())

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)


# Function to clear the screen for cleaner readability after each action
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def read_csv():
    # Opening and reading the inventory.csv file
    with open("inventory.csv", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        products = list(reader)
        for product in products:
            add_new_product(product)


def menu():
    # Setting our choice variable to None
    choice = None
    # Starting the while loop to see if the user has chosen "x" to quit
    clear()
    while choice != "x":
        print("="*22)
        # We print out this message to let them know they can type "x" to quit
        print("ENTER 'x' TO EXIT.")
        print("="*22)
        print()
        # Loop through each item in our dictionary, the key and the value
        for key, value in user_menu.items():
            # Then we are gonna print out the key and the values ex: key= A)  value= Add an entry
            print("{}) {}".format(key, value.__doc__))
        # Asking the user to choose an option,we also lowercase it
        print()
        print("=" * 22)
        choice = input("ENTER AN OPTION [v/a/b]: ").lower()
        # We check if it's "x" if it's not "x" we come back to our menu, we find the function
        # they have selected and we run it
        if choice in user_menu.keys():
            clear()
            user_menu[choice]()
        elif choice != "x":
            print("\nThat's not a valid option, Try Again")
            print()


def add_new_product():
    """Add new product"""


def view():
    """View products"""
    clear()
    products = Product.select().order_by(Product.date_updated.desc())
    product_unmatched = True
    while product_unmatched:
        product_search = int(input("Select a Product ID to view: "))
        for product in products:
            if product_search == product.product_id:
                print(f"Product ID#: {product.product_id}"
                      f"Last Updated: {datetime.datetime.strptime(product.date_updated, '%d-%m-%Y')}"
                      f"Product Name: {product.product_name}"
                      f"Product Quantity: {product.product_quantity}"
                      f"Product Price: {product.product_price} cents")
                return
            else:
                print("The product ID you entered does not match any in the database!")
                return product_search


def backup_data():
    """Backup Database"""


user_menu = OrderedDict([
    ("v", view),
    ("a", add_new_product),
    ("b", backup_data),
])


if __name__ == "__main__":
    initialize()
    read_csv()
    menu()
    backup_data()
