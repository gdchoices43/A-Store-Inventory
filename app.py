import datetime
import csv
import os
import sys
from collections import OrderedDict

from peewee import *

db = SqliteDatabase("inventory.db")


# Remembered how this was done from the "Using Databases in Python" Treehouse course
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


# Remembered how this was done from the "Using Databases in Python" Treehouse course
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
                # it took me awhile to figure this out, it was Jennifer Nordell who pointed out that it's all about
                # what happens in the "except" for the products being only shown if they are the most recently
                # updated product
                    # product_record = Product.get(product_name=row['product_name'])
                    # product_record.product_name = row['product_name']
                    # product_record.product_quantity = row['product_quantity']
                    # product_record.product_price = row['product_price']
                    # product_record.date_updated = row['date_updated']
                    # product_record.save()


# Remembered how this was done from the "Using Databases in Python" Treehouse course
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Remembered how this was done from the "Using Databases in Python" Treehouse course
def menu():
    clear()
    while True:
        choice = None
        print("=" * 36)
        print("   --- STORE INVENTORY MENU ---")
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
        elif choice not in menu_dict:
            print("\nINVALID INPUT. See menu options\n")


# Remembered how this was done from the "Using Databases in Python" Treehouse course,
# well part of it anyway
def view_product():
    """View Products In Inventory"""
    clear()
    while True:
        try:
            id_search = int(input("\nENTER PRODUCT ID #: "))
        except ValueError:
            print("\nINVALID INPUT. TRY AGAIN")
        else:
            try:
                # Seen a conversation between Danielle Gabriszeski and Jennifer Nordell about this solution
                # This part here below in particular was what I didn't have that changed this whole function
                # to work correctly "product = Product.get(id_search)" is what I had originally
                product = Product.get_by_id(id_search)
            except Product.DoesNotExist:
                print("\nINVALID ID #. TRY AGAIN")
            else:
                print("=" * 36)
                print()
                print("Product Search Results:\n")
                print(f"Product ID: {product.product_id}\n"
                      f"Product Name: {product.product_name}\n"
                      f"Product Price: {product.product_price} (cents)\n"
                      f"Product Quantity: {product.product_quantity}\n"
                      f"Last Updated:", product.date_updated.strftime("%m/%d/%Y"), "\n")
                print("=" * 36)
                print()
                print("d) Delete Product")
                print("c) Continue Search")
                print("x) Return To Main Menu")
                print()
                print("=" * 36)
                choice = input("    ENTER AN OPTION: ").lower().strip()
                if choice == "x":
                    clear()
                    menu()
                elif choice == "d":
                    delete(product)
                elif choice == "c":
                    view_product()
                else:
                    print("\nINVALID INPUT. TRY AGAIN\n")
                    view_product()


def delete(product):
    if input("\nVerify You Want To 'DELETE' This Product. (y/n) ").lower() != "n":
        Product.delete_instance(product)
        print("\nThe Product Has Been Deleted!\n")
        clear()
        menu()


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
        product_quantity = input("\nProduct Quantity: ")
        try:
            product_quantity = str(int(product_quantity))
            break
        except ValueError:
            print("\nINVALID INPUT. USE NUMBERS ONLY")
            continue
    while True:
        product_price = input("\nProduct Price: ex(1.99=199)cents: ").strip()
        try:
            float(product_price)
            break
        except ValueError:
            print("\nINVALID INPUT. TRY AGAIN")
            continue
    product_updated = datetime.datetime.today()
    today = product_updated.strftime("%m/%d/%Y")
    print("=" * 36)
    print(f"\nPlease Double Check The Information:"
          f"\n"
          f"\nProduct Name: {product_name}"
          f"\nProduct Price: {product_price}"
          f"\nProduct Quantity: {product_quantity}"
          f"\n")
    print("=" * 36)
    if input("\nSave To Inventory? (y/n) ").lower() == "y":
        # Got the solution on the website below on how to use the correct format to add items to csv file
        # I knew most of it but there were a few things I picked up from the explanation
        # https://www.kite.com/python/answers/how-to-append-to-a-csv-file-in-python
        with open("inventory.csv", "a") as new_file:
            new_file.write("\n"+product_name+","+product_price+","+product_quantity+","+today)
            print("\nProduct Successfully Saved To Inventory!\n")
            load_csv()
            menu()


# Found an explanation on the link below on how to do this the right way
# https://www.programiz.com/python-programming/writing-csv-files
def backup_inventory():
    """Backup Store Inventory"""
    if input("Backup The Inventory? (y/n) ").lower() == "y":
        with open("backup.csv", "w", newline="") as backup_file:
            fieldnames = ["product_name", "product_price", "product_quantity", "date_updated"]
            backup_writer = csv.DictWriter(backup_file, fieldnames=fieldnames)
            backup_writer.writeheader()
            backup_csv = Product.select().order_by(Product.product_id.asc())
            for product in backup_csv:
                # Jennifer Nordell gave me a hint that the price needed to be turned into a str in this part of the
                # backup_inventory function. Before when backing up the inventory there was no decimal in
                # the price of the new backup.csv file
                backup_writer.writerow({
                    "product_name": product.product_name,
                    "product_price": str("$" + "{}".format(product.product_price / 100)),
                    "product_quantity": product.product_quantity,
                    "date_updated": product.date_updated.strftime("%m/%d/%Y")
                })
            print("\nThe Store Inventory Was Backed Up Successfully!\n")


def exit_program():
    """Exit Store Inventory"""
    print("\nExiting Store Inventory....")
    sys.exit()


menu_dict = OrderedDict([
    ("v", view_product),
    ("a", add_new_product),
    ("b", backup_inventory),
    ("x", exit_program)
])


if __name__ == "__main__":
    initializer()
    load_csv()
    menu()
