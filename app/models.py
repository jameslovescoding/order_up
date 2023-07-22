from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Float, Boolean
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    employee_number = Column(Integer, unique=True, nullable=False)
    hashed_password = Column(String(255),  nullable=False)
    # Employee and Order is one-to-many
    orders = relationship("Order", back_populates="employee")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Menu(db.Model):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    # Menu and MenuItem is one-to-many
    items = relationship("MenuItem", back_populates="menu")

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    menu_type_id = Column(Integer, ForeignKey("menu_item_types.id"), nullable=False)
    # MenuItem and MenuItemType is many-to-one
    menu = relationship("Menu", back_populates="items")
    # MenuItem and Menu is many-to-one
    type = relationship("MenuItemType", back_populates="same_type_items")

class MenuItemType(db.Model):
    __tablename__ = 'menu_item_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    # MenuItemType and MenuItem is one-to-many
    same_type_items = relationship("MenuItem", back_populates="type")

class Table(db.Model):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    # Table and Order is one-to-many
    orders = relationship("Order", back_populates="table")

class Order(db.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    finished = Column(Boolean, nullable=False)
    # Order and Employee is many-to-one
    employee = relationship("Employee", back_populates="orders")
    # Order and Table is many-to-one
    table = relationship("Table", back_populates="orders")
    # Order and OrderDetail is one-to-many
    details = relationship("OrderDetail", back_populates="order")

class OrderDetail(db.Model):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    # OrderDetail and Order is many-to-one
    order = relationship("Order", back_populates="details")