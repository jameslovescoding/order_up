from dotenv import load_dotenv
load_dotenv()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.
from app import app, db
from app.models import (
    Employee,
    Menu,
    MenuItem,
    MenuItemType,
    Table,
    Order,
    OrderDetail
)


with app.app_context():
    db.drop_all()
    db.create_all()

    # create employee acount

    employee1 = Employee(name="Margot", employee_number=1111, password="password1")
    employee2 = Employee(name="James", employee_number=2222, password="password2")
    employee3 = Employee(name="Smith", employee_number=3333, password="password3")

    db.session.add(employee1)
    db.session.add(employee2)
    db.session.add(employee3)

    # menus

    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")

    dinner = Menu(name="Dinner")

    chicken_kiev = MenuItem(name="Chicken Kiev", price=14.50, type=entrees, menu=dinner)
    eggplant_parmesan = MenuItem(name="Eggplant Parmesan", price=12.50, type=entrees, menu=dinner)
    french_fries = MenuItem(name="French Fries", price=6.50, type=sides, menu=dinner)
    deep_fried_onions = MenuItem(name="Deep-fried Onions", price=7.50, type=sides, menu=dinner)
    iced_tea = MenuItem(name="Iced Tea", price=2.5, type=beverages, menu=dinner)
    diet_coke = MenuItem(name="Diet Coke", price=2.3, type=beverages, menu=dinner)

    db.session.add(dinner)

    # tables

    for i in range(1, 11):
        table = Table(number=i, capacity=i)
        db.session.add(table)

    db.session.commit()