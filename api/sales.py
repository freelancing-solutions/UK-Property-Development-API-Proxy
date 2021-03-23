import os
from flask import Flask, request, make_response, jsonify, render_template, Blueprint
from endpoints.endpoints import EndPoints

sales = Blueprint('sales', __name__)


@sales.route('/api/v1/valuation-sale', methods=['POST'])
def valuation_sale():
    """
     post-body:        postcode, internal_area, property_type, construction_date, bedrooms,
                       bathrooms, finish_quality, outdoor_space, off_street_parking
    :return:
    """
    valuation_data = request.get_json()
    if 'postcode' in valuation_data:
        postcode = valuation_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'internal_area' in valuation_data:
        internal_area = valuation_data['internal_area']
    else:
        return jsonify({'status': 'failure', 'message': 'internal_area is required'}), 500

    if 'property_type' in valuation_data:
        property_type = valuation_data['property_type']
    else:
        return jsonify({'status': 'failure', 'message': 'property_type is required'}), 500

    if 'construction_date' in valuation_data:
        construction_date = valuation_data['construction_date']
    else:
        return jsonify({'status': 'failure', 'message': 'construction_date is required'}), 500

    if 'bedrooms' in valuation_data:
        bedrooms = int(valuation_data['bedrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bedrooms is required'}), 500

    if 'bathrooms' in valuation_data:
        bathrooms = int(valuation_data['bathrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bathrooms is required'}), 500

    if 'finish_quality' in valuation_data:
        finish_quality = valuation_data['finish_quality']
    else:
        return jsonify({'status': 'failure', 'message': 'finish_quality is required'}), 500

    if 'outdoor_space' in valuation_data:
        outdoor_space = valuation_data['outdoor_space']
    else:
        return jsonify({'status': 'failure', 'message': 'outdoor_space is required'}), 500

    if 'off_street_parking' in valuation_data:
        off_street_parking = valuation_data['off_street_parking']
    else:
        return jsonify({'status': 'failure', 'message': 'off_street_parking is required'}), 500

    return EndPoints().valuation_sale(postcode=postcode, internal_area=internal_area, property_type=property_type,
                                      construction_date=construction_date, bedrooms=bedrooms, bathrooms=bathrooms,
                                      finish_quality=finish_quality, outdoor_space=outdoor_space,
                                      off_street_parking=off_street_parking)


@sales.route('/api/v1/prices', methods=['POST'])
def prices():
    prices_data = request.get_json()

    if 'postcode' in prices_data:
        postcode = prices_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'bedrooms' in prices_data:
        bedrooms = int(prices_data['bedrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().prices(postcode=postcode, bedrooms=bedrooms)


@sales.route('/api/v1/prices-per-sqf', methods=['POST'])
def price_per_sqf():
    """
        given postcode : return prices-per-sqf
    :return:
    """
    prices_data = request.get_json()
    if 'postcode' in prices_data:
        postcode = prices_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().prices_per_sqf(postcode=postcode)


@sales.route('/api/v1/sold-prices', methods=['POST'])
def sold_prices():
    """
        given postcode, property_type, max_age
    :return: sold prices
    """
    sold_prices_data = request.get_json()
    if 'postcode' in sold_prices_data:
        postcode = sold_prices_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'property_type' in sold_prices_data:
        property_type = sold_prices_data['property_type']
    else:
        return jsonify({'status': 'failure', 'message': 'property_type is required'}), 500

    if 'max_age' in sold_prices_data:
        max_age = sold_prices_data['max_age']
    else:
        return jsonify({'status': 'failure', 'message': 'max_age is required'}), 500

    return EndPoints().sold_prices(postcode=postcode, property_type=property_type, max_age=max_age)


@sales.route('/api/v1/sold-prices-per-sqf', methods=['POST'])
def sold_prices_per_sqf():
    sold_prices_data = request.get_json()
    if 'postcode' in sold_prices_data:
        postcode = sold_prices_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().sold_prices_per_sqf(postcode=postcode)


@sales.route('/api/v1/growth', methods=['POST'])
def growth():
    growth_data = request.get_json()
    if 'postcode' in growth_data:
        postcode = growth_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().growth(postcode=postcode)


@sales.route('/api/v1/postcode-key-stats', methods=['POST'])
def postcode_stats():
    postcode_stats_data = request.get_json()
    if 'postcode' in postcode_stats_data:
        region = postcode_stats_data['region']
    else:
        return jsonify({'status': 'failure', 'message': 'region is required'}), 500

    return EndPoints().postcode_key_stats(region=region)


@sales.route('/api/v1/sourced-properties', methods=['POST'])
def sourced_properties():
    sourced_data = request.get_json()
    if 'property_list' in sourced_data:
        property_list = sourced_data['property_list']
    else:
        return jsonify({'status': 'failure', 'message': 'property_list is required'}), 500

    if 'postcode' in sourced_data:
        postcode = sourced_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'radius' in sourced_data:
        radius = int(sourced_data['radius'])

        if 'results' in sourced_data:
            results = int(sourced_data['results'])

            return EndPoints().sourced_properties(property_list=property_list, postcode=postcode,
                                                  radius=radius, results=results)

        return EndPoints().sourced_properties(property_list=property_list, postcode=postcode,
                                              radius=radius)

    return EndPoints().sourced_properties(property_list=property_list, postcode=postcode)


@sales.route('/api/v1/property-info', methods=['POST'])
def property_info():
    property_info_data = request.get_json()
    if 'property_id' in property_info_data:
        property_id = property_info_data['property_id']
    else:
        return jsonify({'status': 'failure', 'message': 'property_id is required'}), 500

    return EndPoints().property_info(property_id=property_id)


@sales.route('/api/v1/development-gdv', methods=['POST'])
def development_gdv():
    development_gdv_data = request.get_json()
    if 'postcode' in development_gdv_data:
        postcode = development_gdv_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'flat_2' in development_gdv_data:
        flat_2 = development_gdv_data['flat_2']
    else:
        return jsonify({'status': 'failure', 'message': 'flat_2 is required'}), 500

    if 'flat_1' in development_gdv_data:
        flat_1 = development_gdv_data['flat_1']
    else:
        return jsonify({'status': 'failure', 'message': 'flat_1 is required'}), 500

    if 'finish_quality' in development_gdv_data:
        finish_quality = development_gdv_data['finish_quality']
    else:
        return jsonify({'status': 'failure', 'message': 'finish_quality is required'}), 500

    return EndPoints().development_gdv(postcode=postcode, flat_2=flat_2, flat_1=flat_1)
