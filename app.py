import datetime
import csv
import os
import sys
from collections import OrderedDict

from peewee import *

db = SqliteDatabase("inventory.db")


# Remembered how this was done from the "Using Databases in Python" course
class Product(Model):
    # Jennifer Nordell pointed me in the right direction on using AutoField, I was using PrimaryKeyField
    product_id = AutoField()
    # Jennifer Nordell gave me a hint that my product_name needed to be unique, which I had spaced out on
    product_name = CharField(unique=True, max_length=50)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db


# Remembered how this was done from the "Using Databases in Python" course
def initializer():
    db.connect()
    db.create_tables([Product], safe=True)
    db.close()


def load_csv():
    with open("inventory.csv") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")
        rows = list(reader)
        for row in rows:
            row["product_price"] = float(row["product_price"].replace("$", "")) * 100
            row["product_quantity"] = int(row["product_quantity"])
            row["date_updated"] = datetime.datetime.strptime(row["date_updated"], "%m/%d/%Y")
            try:
                Product.create(
                    product_name=row["product_name"],
                    product_price=row["product_price"],
                    product_quantity=row["product_quantity"],
                    date_updated=row["date_updated"]
                ).save()
            except IntegrityError:
                product_record = Product.get(product_name=row["product_name"])
                if product_record.date_updated <= row['date_updated']:
                    product_record.product_price = row['product_price']
                    product_record.product_quantity = row['product_quantity']
                    product_record.date_updated = row['date_updated']
                    product_record.save()
                # This was my original except IntegrityError, this wasn't working so I changed it to the above
                # it took me awhile to figure this out
                    # product_record = Product.get(product_name=row['product_name'])
                    # product_record.product_name = row['product_name']
                    # product_record.product_quantity = row['product_quantity']
                    # product_record.product_price = row['product_price']
                    # product_record.date_updated = row['date_updated']
                    # product_record.save()


# Remembered how this was done from the "Using Databases in Python" course
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Remembered how this was done from the "Using Databases in Python" course
def menu():
    clear()
    while True:
        choice = None
        print("=" * 36)
        print("   --- STORE INVENTORY MENU ---")
        print("=" * 36)
        print("        ENTER 'x' TO EXIT")
        print("=" * 36)
        print()
        for key, value in menu_dict.items():
            print("{}) {}".format(key, value.__doc__))
        print()
        print("=" * 36)
        choice = input("       ENTER AN OPTION: ").lower().strip()
        if choice in menu_dict:
            clear()
            menu_dict[choice]()
        elif choice == "x":
            print("\n\nEXITING STORE INVENTORY...  Goodbye!")
            sys.exit()
        elif choice not in menu_dict:
            print("\nINVALID INPUT. See menu options")


def view_product():
    """View Products In Inventory"""
    items = Product.select().order_by(Product.product_id.asc())
    for product in items:
        clear()
        print("\n")
        print(f"Product ID: {product.product_id}\n"
              f"Product Name: {product.product_name}\n"
              f"Product Price: {product.product_price} (cents)\n"
              f"Product Quantity: {product.product_quantity}\n"
              f"Last Updated:", product.date_updated.strftime("%m/%d/%Y"), "\n")
        print("=" * 36)
        print()
        print("Enter) For Next Product")
        print("d) Delete Product")
        print("x) Return To Main Menu")
        print()
        print("=" * 36)
        choice = input("ENTER AN OPTION: ").lower().strip()
        if choice == "x":
            clear()
            break
        elif choice == "d":
            delete(product)


# Was struggling with this search/delete functions. Found the solution from a fellow Pythonista on GitHub.com
# https://github.com/daniellerg/CSV_Inventory_App/blob/main/app.py
# Was during the weekend and had nobody to ask on slack
def delete(product):
    if input("\nVerify You Want To 'DELETE' This Product. (Y/N)").lower() != "N":
        product.delete_instance()
        print("\nThe Product Has Been Deleted!")


# Was struggling with this search/delete functions. Found the solution from a fellow Pythonista on GitHub.com
# https://github.com/daniellerg/CSV_Inventory_App/blob/main/app.py
# Was during the weekend and had nobody to ask on slack
def search_inventory():
    """Search by Product ID"""
    clear()
    while True:
        try:
            id_search = int(input("\nENTER PRODUCT ID #: "))
        except ValueError:
            print("\nINVALID INPUT. TRY AGAIN")
        else:
            try:
                product = Product.get_by_id(id_search)
            except Product.DoesNotExist:
                print("INVALID ID #. TRY AGAIN")
            else:
                clear()
                print("\n")
                print(f"Product ID: {product.product_id}\n"
                      f"Product Name: {product.product_name}\n"
                      f"Product Price: {product.product_price} (cents)\n"
                      f"Product Quantity: {product.product_quantity}\n"
                      f"Last Updated:", product.date_updated.strftime("%m/%d/%Y"), "\n")
                break


def add_new_product():
    """Add Products to Inventory"""
    clear()
    print("=" * 36)
    print("PRESS ctrl+d WHEN FINISHED")
    print("=" * 36)
    print("\n")
    while True:
        product_name = input("Product Name: ")
        try:
            if not product_name or product_name == "":
                raise ValueError("\nPLEASE ENTER A VALID NAME")
        except ValueError as err:
            print(err)
        else:
            break
    while True:
        product_price = input("\nProduct Price: ex(1.99=199)cents: ").strip()
        try:
            float(product_price*100)
            break
        except ValueError:
            print("\nINVALID INPUT. TRY AGAIN")
            continue
    while True:
        product_quantity = input("\nProduct Quantity: ")
        try:
            product_quantity = str(int(product_quantity))
            break
        except ValueError:
            print("\nINVALID INPUT. USE NUMBERS ONLY")
            continue
    product_updated = datetime.datetime.today()
    today = product_updated.strftime("%m/%d/%Y")
    print(f"\nPlease Check The Information Input:"
          f"\n"
          f"\nProduct Name: {product_name}"
          f"\nProduct Price: {product_price}"
          f"\nProduct Quantity: {product_quantity}"
          f"\n")
    print("=" * 36)
    if input("\nSave To Inventory? (y/n) ").lower() == "y":
        with open("inventory.csv", "a") as new_file:
            new_file.write("\n"+product_name+","+product_price+","+product_quantity+","+today)
            print("\nProduct Successfully Saved To Inventory!\n")
            print("=" * 36)
            load_csv()


def backup_inventory():
    """Backup Store Inventory"""


menu_dict = OrderedDict([
    ("v", view_product),
    ("a", add_new_product),
    ("b", backup_inventory),
    ("s", search_inventory)
])


if __name__ == "__main__":
    initializer()
    load_csv()
    menu()
