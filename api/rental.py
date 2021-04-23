# UK Property Rentals API's
from flask import request, jsonify, Blueprint
from endpoints.endpoints import EndPoints
from library import api_cache_decorator

rental = Blueprint('rental', __name__)



@rental.route('/api/v1/valuation-rent', methods=['POST'])
@api_cache_decorator
def valuation_rent(cache: any) -> tuple:
    """
        Arguments:
            postcode, internal_area, property_type, construction_date, bedrooms, bathrooms,
            finish_quality, outdoor_space, off_street_parking

        :return:
    """
    if not (cache is None):
        return cache
    valuation_rent_data: dict = request.get_json()

    if 'postcode' in valuation_rent_data:
        postcode: str = valuation_rent_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'internal_area' in valuation_rent_data:
        internal_area: int = int(valuation_rent_data['internal_area'])
    else:
        return jsonify({'status': 'failure', 'message': 'internal_area is required'}), 500

    if 'property_type' in valuation_rent_data:
        property_type: str = valuation_rent_data['property_type']
    else:
        return jsonify({'status': 'failure', 'message': 'property_type is required'}), 500

    if 'construction_date' in valuation_rent_data:
        construction_date: str = valuation_rent_data['construction_date']
    else:
        return jsonify({'status': 'failure', 'message': 'construction_date is required'}), 500

    if 'bedrooms' in valuation_rent_data:
        bedrooms: int = int(valuation_rent_data['bedrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bedrooms is required'}), 500

    if 'bathrooms' in valuation_rent_data:
        bathrooms: int = int(valuation_rent_data['bathrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bathrooms is required'}), 500

    if 'finish_quality' in valuation_rent_data:
        finish_quality: str = valuation_rent_data['finish_quality']
    else:
        return jsonify({'status': 'failure', 'message': 'finish_quality is required'}), 500

    if 'outdoor_space' in valuation_rent_data:
        outdoor_space: str = valuation_rent_data['outdoor_space']
    else:
        return jsonify({'status': 'failure', 'message': 'outdoor_space is required'}), 500

    if 'off_street_parking' in valuation_rent_data:
        off_street_parking: str = valuation_rent_data['off_street_parking']
    else:
        return jsonify({'status': 'failure', 'message': 'off_street_parking is required'}), 500

    return EndPoints().valuation_rent(postcode, internal_area, property_type, construction_date, bedrooms, bathrooms
                                      , finish_quality, outdoor_space, off_street_parking)


@rental.route('/api/v1/rents', methods=['POST'])
@api_cache_decorator
def rents(cache: any) -> tuple:
    """
        args:
            postcode: str
            bedrooms: int
    :return: tuple
    """
    if not(cache is None):
        return cache
    rents_data: dict = request.get_json()
    if 'postcode' in rents_data:
        postcode: str = rents_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    if 'bedrooms' in rents_data:
        bedrooms: int = int(rents_data['bedrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().rents(postcode=postcode, bedrooms=bedrooms)


@rental.route('/api/v1/rents-hmo', methods=['POST'])
@api_cache_decorator
def rents_hmo(cache: any) -> tuple:
    """
        args: postcode: str
    :return:
    """
    if not(cache is None):
        return cache
    rents_hmo_data: dict = request.get_json()
    if 'postcode' in rents_hmo_data:
        postcode: str = rents_hmo_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().rents_hmo(postcode=postcode)


@rental.route('/api/v1/yields', methods=['POST'])
@api_cache_decorator
def yields(cache: any) -> tuple:
    """
        args: postcode: str , bedrooms: int
    :return:
    """
    if not(cache is None):
        return cache

    yields_data: dict = request.get_json()
    if 'postcode' in yields_data:
        postcode: str = yields_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    if 'bedrooms' in yields_data:
        bedrooms: int = int(yields_data['bedrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bedrooms is required'}), 500

    return EndPoints().yields(postcode=postcode, bedrooms=bedrooms)


@rental.route('/api/v1/demand-rent', methods=['POST'])
@api_cache_decorator
def demand_rent(cache: any) -> tuple:
    if not(cache is None):
        return cache
    demand_rent_data: dict = request.get_json()
    if 'postcode' in demand_rent_data:
        postcode: str = demand_rent_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().demand_rent(postcode=postcode)


@rental.route('/api/v1/lha-rent', methods=['POST'])
@api_cache_decorator
def lha_rent(cache: any) -> tuple:
    if not(cache is None):
        return cache

    lha_data: dict = request.get_json()
    if 'postcode' in lha_data:
        postcode: str = lha_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'bedrooms' in lha_data:
        bedrooms: int = int(lha_data['bedrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bedrooms is required'}), 500

    return EndPoints().lha_rate(postcode=postcode, bedrooms=bedrooms)
