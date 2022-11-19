from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from utils.schemas import OrderBase, Orders
from models import Order
from utils.gps import coords_by_address, tsp_path
import logging


bp = Blueprint("orders", __name__, url_prefix="/orders")


@bp.route('')
def orders():
    return render_template('index.html')


@bp.route('/find-path', methods=['POST'])
def find_path():
    orders = request.get_json()['orders']
    # logging.warning('=========================')
    # logging.warning(orders)
    for order in orders:
        order_found = Order.find(Order.id == order['id']).all()
        if not order_found:
            new_order = Order(
                id=order['id'],
                input_type=order['inputType'],
                order_date=order['date'[:10]],
                order_time=order['time'],
                coords=order['coords']
            )

            new_order.save()
            new_order.expire(120)

    pks = Order.all_pks()
    orders = [order for order in pks]
    # addresses = [Order.get(pk).address for pk in orders]
    # coords = [coords_by_address(order) for order in addresses]
    coords = [list(map(float, Order.get(pk).coords)) for pk in orders]
    path, dist = tsp_path(coords)
    logging.warning('=========================')
    logging.warning(path)

    # return jsonify({'orders': orders, 'path': (optimal_path, dist)})
    return render_template('index.html', path=path)


@bp.route('/delete-orders')
def delete_orders():
    pks = Order.all_pks()
    orders = [order for order in pks]
    for order in orders:
        Order.delete(order)
    return
