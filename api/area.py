# UK Area API
from flask import request, jsonify, Blueprint
from endpoints.endpoints import EndPoints
from library import api_cache_decorator
area = Blueprint('area', __name__)


@area.route('/api/v1/crime', methods=['POST'])
@api_cache_decorator
def crime(cache):
    if not(cache is None):
        return cache

    crime_data = request.get_json()
    if 'postcode' in crime_data:
        postcode = crime_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().agents(postcode=postcode)


@area.route('/api/v1/demographics', methods=['POST'])
@api_cache_decorator
def demographics(cache):
    if not(cache is None):
        return cache

    demo_data = request.get_json()
    if 'postcode' in demo_data:
        postcode = demo_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().demographics(postcode=postcode)


@area.route('/api/v1/schools', methods=['POST'])
@api_cache_decorator
def schools(cache):
    if not(cache is None):
        return cache

    schools_data = request.get_json()
    if 'postcode' in schools_data:
        postcode = schools_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().schools(postcode=postcode)


@area.route('/api/v1/restaurants', methods=['POST'])
@api_cache_decorator
def restaurants(cache):
    if not(cache is None):
        return cache

    rest_data = request.get_json()
    if 'postcode' in rest_data:
        postcode = rest_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().restaurants(postcode=postcode)


@area.route('/api/v1/politics', methods=['POST'])
@api_cache_decorator
def politics(cache):
    if not(cache is None):
        return cache

    politic_data = request.get_json()
    if 'postcode' in politic_data:
        postcode = politic_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().politics(postcode=postcode)


@area.route('/api/v1/area-type', methods=['POST'])
@api_cache_decorator
def area_type(cache):
    if not(cache is None):
        return cache

    area_data = request.get_json()
    if 'postcode' in area_data:
        postcode = area_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().area_type(postcode=postcode)
