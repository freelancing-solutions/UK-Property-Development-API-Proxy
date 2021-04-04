# UK Area API
from flask import request, jsonify, Blueprint
from endpoints.endpoints import EndPoints
from library import api_cache_decorator
area = Blueprint('area', __name__)


@area.route('/api/v1/crime', methods=['POST'])
@api_cache_decorator
def crime(cache: any) -> tuple:
    if not(cache is None):
        return cache

    crime_data: dict = request.get_json()
    if 'postcode' in crime_data and not(crime_data['postcode'] is None):
        postcode: str = crime_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().agents(postcode=postcode)


@area.route('/api/v1/demographics', methods=['POST'])
@api_cache_decorator
def demographics(cache: any) -> tuple:
    if not(cache is None):
        return cache

    demo_data: dict = request.get_json()
    if 'postcode' in demo_data and not (demo_data['postcode']  == ""):
        postcode: str = demo_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().demographics(postcode=postcode)


@area.route('/api/v1/schools', methods=['POST'])
@api_cache_decorator
def schools(cache: any) -> tuple:
    if not(cache is None):
        return cache

    schools_data: dict = request.get_json()
    if 'postcode' in schools_data and not(schools_data['postcode']  == ""):
        postcode: str = schools_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().schools(postcode=postcode)


@area.route('/api/v1/restaurants', methods=['POST'])
@api_cache_decorator
def restaurants(cache: any) -> tuple:
    if not(cache is None):
        return cache

    rest_data: dict = request.get_json()
    if 'postcode' in rest_data and not(rest_data['postcode']  == ""):
        postcode: str = rest_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().restaurants(postcode=postcode)


@area.route('/api/v1/politics', methods=['POST'])
@api_cache_decorator
def politics(cache: any) -> tuple:
    if not(cache is None):
        return cache

    politic_data: dict = request.get_json()
    if 'postcode' in politic_data and not (politic_data['postcode']  == ""):
        postcode: str = politic_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().politics(postcode=postcode)


@area.route('/api/v1/area-type', methods=['POST'])
@api_cache_decorator
def area_type(cache: any) -> tuple:
    if not(cache is None):
        return cache

    area_data: dict = request.get_json()
    if 'postcode' in area_data and not (area_data['postcode']  == ""):
        postcode: str = area_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().area_type(postcode=postcode)
