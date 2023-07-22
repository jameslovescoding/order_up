from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import (
    db,
    Employee,
    Menu,
    MenuItem,
    MenuItemType,
    Table,
    Order,
    OrderDetail
)
from ..forms import (
    TableAssignmentForm
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.routing import BaseConverter


session = db.session

bp = Blueprint("orders", __name__, url_prefix="")

@bp.route("/", methods=['GET', 'POST'])
@login_required
def index():
    table_assign_form = TableAssignmentForm()
    if table_assign_form.is_submitted():
        # print("submitted")
        table_id = table_assign_form.data["tables"]
        employee_id = table_assign_form.data["servers"]
        # print(f'{table_id}, {employee_id}')
        return redirect(f'/assign_table/{table_id}/{employee_id}')
    # Get the tables and open orders
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.finished == False)
    busy_table_ids = [order.table_id for order in open_orders]
    open_tables = [table for table in tables if table.id not in busy_table_ids]
    table_assign_form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]
    employees = Employee.query.order_by(Employee.id).all()
    table_assign_form.servers.choices = [(e.id, e.name) for e in employees]
    return render_template("orders.html",
                           is_anonymous=current_user.is_anonymous,
                           table_assign_form=table_assign_form,
                           open_orders=open_orders)



@bp.route("assign_table/<int:table_id>/<int:employee_id>")
@login_required
def assign_table(table_id, employee_id):
    # did not verify table with table_id and employee with employee_id exist
    new_order = Order(employee_id=employee_id,
                      table_id=table_id,
                      finished=False)
    session.add(new_order)
    session.commit()
    return redirect(url_for('orders.index'))



@bp.route("close_table/<int:order_id>")
@login_required
def close_table(order_id):
    order_id_query = db.session.query(Order).get(order_id)
    print(order_id_query)
    order_id_query.finished=True
    session.commit()
    return redirect(url_for('orders.index'))



@bp.route("add_to_order/<int:order_id>/<list:order_details>")
@login_required
def add_to_order(order_id, order_details):
    order_details = list(map(lambda str: int(str), order_details))
    for menu_item_id in order_details:
        new_order_detail = OrderDetail(order_id=order_id,
                               menu_item_id=menu_item_id)
        session.add(new_order_detail)
    session.commit()
    return redirect(url_for('orders.index'))