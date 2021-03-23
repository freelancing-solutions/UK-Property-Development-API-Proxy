# UK Property Rentals API's
import os
from flask import Flask, request, make_response, jsonify, render_template, Blueprint
from endpoints.endpoints import EndPoints

rental = Blueprint('rental', __name__)


@rental.route('/api/v1/valuation-rent', methods=['POST'])
def valuation_rent():
    """
        Arguments:
            postcode, internal_area, property_type, construction_date, bedrooms, bathrooms,
            finish_quality, outdoor_space, off_street_parking

        :return:
    """

    valuation_rent_data = request.get_json()

    if 'postcode' in valuation_rent_data:
        postcode = valuation_rent_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'internal_area' in valuation_rent_data:
        internal_area = valuation_rent_data['internal_area']
    else:
        return jsonify({'status': 'failure', 'message': 'internal_area is required'}), 500

    if 'property_type' in valuation_rent_data:
        property_type = valuation_rent_data['property_type']
    else:
        return jsonify({'status': 'failure', 'message': 'property_type is required'}), 500

    if 'construction_date' in valuation_rent_data:
        construction_date = valuation_rent_data['construction_date']
    else:
        return jsonify({'status': 'failure', 'message': 'construction_date is required'}), 500

    if 'bedrooms' in valuation_rent_data:
        bedrooms = int(valuation_rent_data['bedrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bedrooms is required'}), 500

    if 'bathrooms' in valuation_rent_data:
        bathrooms = int(valuation_rent_data['bathrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bathrooms is required'}), 500

    if 'finish_quality' in valuation_rent_data:
        finish_quality = valuation_rent_data['finish_quality']
    else:
        return jsonify({'status': 'failure', 'message': 'finish_quality is required'}), 500

    if 'outdoor_space' in valuation_rent_data:
        outdoor_space = valuation_rent_data['outdoor_space']
    else:
        return jsonify({'status': 'failure', 'message': 'outdoor_space is required'}), 500

    if 'off_street_parking' in valuation_rent_data:
        off_street_parking = valuation_rent_data['off_street_parking']
    else:
        return jsonify({'status': 'failure', 'message': 'off_street_parking is required'}), 500

    return EndPoints().valuation_rent(postcode, internal_area, property_type, construction_date, bedrooms, bathrooms
                                      , finish_quality, outdoor_space, off_street_parking)


@rental.route('/api/v1/rents', methods=['POST'])
def rents():
    """
        args:
            postcode: str
            bedrooms: int
    :return:
    """
    rents_data = request.get_json()
    if 'postcode' in rents_data:
        postcode = rents_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'bedrooms' in rents_data:
        bedrooms = rents_data['bedrooms']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().rents(postcode=postcode, bedrooms=bedrooms)


@rental.route('/api/v1/rents-hmo', methods=['POST'])
def rents_hmo():
    """
        args: postcode: str
    :return:
    """
    rents_hmo_data = request.get_json()
    if 'postcode' in rents_hmo_data:
        postcode = rents_hmo_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().rents_hmo(postcode=postcode)


@rental.route('/api/v1/yields', methods=['POST'])
def yields():
    """
        args: postcode: str , bedrooms: int
    :return:
    """
    yields_data = request.get_json()
    if 'postcode' in yields_data:
        postcode = yields_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    if 'bedrooms' in yields_data:
        bedrooms = int(yields_data['bedrooms'])
    else:
        return jsonify({'status': 'failure', 'message': 'bedrooms is required'}), 500

    return EndPoints().yields(postcode=postcode, bedrooms=bedrooms)


@rental.route('/api/v1/demand-rent', methods=['POST'])
def demand_rent():
    demand_rent_data = request.get_json()
    if 'postcode' in demand_rent_data:
        postcode = demand_rent_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().demand_rent(postcode=postcode)


@rental.route('/api/v1/lha-rent', methods=['POST'])
def lha_rent():
    lha_data = request.get_json()
    if 'postcode' in lha_data:
        postcode = lha_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'bedrooms' in lha_data:
        bedrooms = lha_data['bedrooms']
    else:
        return jsonify({'status': 'failure', 'message': 'bedrooms is required'}), 500

    return EndPoints().lha_rate(postcode=postcode, bedrooms=bedrooms)
