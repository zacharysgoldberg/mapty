from flask import Blueprint, request, jsonify
from app import app
from app.utils.read_csv import read_csv_and_insert
from ..utils.gps import coords_by_address, tsp_path
import os
import logging

bp = Blueprint("orders", __name__, url_prefix="/order")

# Set up logging
logging.basicConfig(level=logging.WARNING)


@bp.route('/find-path', methods=['POST', 'OPTIONS', 'GET'])
def find_path():
    if request.method == 'POST':
        data = request.json
        points = data.get('points', [])

        # Process points to convert them to a format suitable for tsp_path function
        coordinates = [[point['lat'], point['lng']] for point in points]

        # Calculate shortest path
        path, distance = tsp_path(coordinates)
        
        # return jsonify({'path': path, 'distance': distance})
        return jsonify({'path': path, 'distance': distance})
    
    elif request.method == 'OPTIONS':
        # Handle CORS preflight request
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST',
        }
        return ('', 204, headers)
        
    # For simulating drone only    
    elif request.method == 'GET':
        file_path = os.path.join(os.path.dirname(__file__), 'orders.csv')
        try:
            orders: list = read_csv_and_insert(file_path)
            addresses: list = [order.address for order in orders]
            coords: list = [coords_by_address(address) for address in addresses]
            path, dist = tsp_path(coords)
            logging.warning('\n\nPath: %s, Distance: %s\n', path, dist)
            return jsonify({
                'path': path, 
                'distance': dist,
                'addresses': addresses
            })
        except FileNotFoundError as e:
            logging.error(e)
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            logging.error('An error occurred: %s', e)
            return jsonify({'error': 'An error occurred while processing your request.'}), 500   
    
