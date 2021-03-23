# UK Area API
from cachetools import cached, LRUCache, TTLCache
from flask import request, jsonify, Blueprint
from endpoints.endpoints import EndPoints

area = Blueprint('area', __name__)


@area.route('/api/v1/crime', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def crime():
    crime_data = request.get_json()
    if 'postcode' in crime_data:
        postcode = crime_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().agents(postcode=postcode)


@area.route('/api/v1/demographics', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def demographics():
    demo_data = request.get_json()
    if 'postcode' in demo_data:
        postcode = demo_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().demographics(postcode=postcode)


@area.route('/api/v1/schools', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def schools():
    schools_data = request.get_json()
    if 'postcode' in schools_data:
        postcode = schools_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().schools(postcode=postcode)


@area.route('/api/v1/restaurants', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def restaurants():
    rest_data = request.get_json()
    if 'postcode' in rest_data:
        postcode = rest_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().restaurants(postcode=postcode)


@area.route('/api/v1/politics', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def politics():
    politic_data = request.get_json()
    if 'postcode' in politic_data:
        postcode = politic_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().politics(postcode=postcode)


@area.route('/api/v1/area-type', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def area_type():
    area_data = request.get_json()
    if 'postcode' in area_data:
        postcode = area_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().area_type(postcode=postcode)
