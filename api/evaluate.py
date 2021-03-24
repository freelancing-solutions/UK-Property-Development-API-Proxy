# UK Property Evaluation API

from flask import request, jsonify, Blueprint
from endpoints.endpoints import EndPoints
from cachetools import cached, TTLCache

evaluate = Blueprint('evaluate', __name__)


@evaluate.route('/api/v1/planning', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def planning():
    planning_data = request.get_json()
    if 'postcode' in planning_data:
        postcode = planning_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'decision_rating' in planning_data:
        decision_rating = planning_data['decision_rating']
    else:
        return jsonify({'status': 'failure', 'message': 'decision_rating is required'}), 500

    if 'category' in planning_data:
        category = planning_data['category']
    else:
        return jsonify({'status': 'failure', 'message': 'category is required'}), 500

    if 'max_age_decision' in planning_data:
        max_age_decision = int(planning_data['max_age_decision'])
    else:
        return jsonify({'status': 'failure', 'message': 'max_age_decision is required'}), 500

    if 'results' in planning_data:
        results = int(planning_data['results'])
    else:
        return jsonify({'status': 'failure', 'message': 'results is required'}), 500

    return EndPoints().planning(postcode=postcode, decision_rating=decision_rating, category=category,
                                max_age_decision=max_age_decision, results=results)


@evaluate.route('/api/v1/freehold-titles', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def freehold_title():
    freehold_data = request.get_json()
    if 'postcode' in freehold_data:
        postcode = freehold_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().freehold_titles(postcode=postcode)


@evaluate.route('/api/v1/title-info', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def title_info():
    title_data = request.get_json()
    if 'title' in title_data:
        title = title_data['title']
    else:
        return jsonify({'status': 'failure', 'message': 'title is required'}), 500

    return EndPoints().title_info(title=title)


@evaluate.route('/api/v1/stamp-duty', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def stamp_duty():
    stamp_data = request.get_json()
    if 'value' in stamp_data:
        value = stamp_data['value']
    else:
        return jsonify({'status': 'failure', 'message': 'value is required'}), 500
    if 'country' in stamp_data:
        country = stamp_data['country']
    else:
        return jsonify({'status': 'failure', 'message': 'country is required'}), 500

    if 'additional' in stamp_data:
        additional = stamp_data['additional']
    else:
        return jsonify({'status': 'failure', 'message': 'additional is required'}), 500

    return EndPoints().stamp_duty(value=value, country=country, additional=additional)


@evaluate.route('/api/v1/green-belt', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def green_belt():
    green_belt = request.get_json()
    if 'postcode' in green_belt:
        postcode = green_belt['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().green_belt(postcode=postcode)


@evaluate.route('/api/v1/national-park', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def national_park():
    national_park = request.get_json()
    if 'postcode' in national_park:
        postcode = national_park['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().national_park(postcode=postcode)


@evaluate.route('/api/v1/aobn', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def aonb():
    anb_data = request.get_json()
    if 'postcode' in anb_data:
        postcode = anb_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().aonb(postcode=postcode)


@evaluate.route('/api/v1/flood-risk', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def flood_risk():
    flood_data = request.get_json()
    if 'postcode' in flood_data:
        postcode = flood_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().flood_risk(postcode=postcode)


@evaluate.route('/api/v1/internet-speed', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def internet_speed():
    internet_data = request.get_json()
    if 'postcode' in internet_data:
        postcode = internet_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().internet_speed(postcode=postcode)


@evaluate.route('/api/v1/build-cost', methods=["POST"])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def build_cost():
    build_cost_data = request.get_json()
    if 'postcode' in build_cost_data:
        postcode = build_cost_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    if 'property_type' in build_cost_data:
        property_type = build_cost_data['property_type']
    else:
        return jsonify({'status': 'failure', 'message': 'property_type is required'}), 500

    if 'internal_area' in build_cost_data:
        internal_area = build_cost_data['internal_area']
    else:
        return jsonify({'status': 'failure', 'message': 'internal_area is required'}), 500

    if 'finish_quality' in build_cost_data['finish_quality']:
        finish_quality = build_cost_data['finish_quality']
    else:
        return jsonify({'status': 'failure', 'message': 'finish_quality is required'}), 500

    return EndPoints().build_cost(postcode=postcode, property_type=property_type, internal_area=internal_area,
                                  finish_quality=finish_quality)


@evaluate.route('/api/v1/ptal', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def ptal():
    ptal_data = request.get_json()
    if 'postcode' in ptal_data:
        postcode = ptal_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().ptal(postcode=postcode)


@evaluate.route('/api/v1/council-tax', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def council_tax():
    council_data = request.get_json()
    if 'postcode' in council_data:
        postcode = council_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().council_tax(postcode=postcode)


@evaluate.route('/api/v1/floor-areas', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def floor_areas():
    floor_data = request.get_json()
    if 'postcode' in floor_data:
        postcode = floor_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().floor_areas(postcode=postcode)


@evaluate.route('/api/v1/listed-buildings', methods=['POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=43200))
def listed_buildings():
    listed_data = request.get_json()
    if 'postcode' in listed_data:
        postcode = listed_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'grade' in listed_data:
        grade = listed_data['grade']
    else:
        return jsonify({'status': 'failure', 'message': 'grade is required'}), 500

    if 'listed_after' in listed_data:
        listed_after = listed_data['listed_after']
    else:
        return jsonify({'status': 'failure', 'message': 'listed_after is required'}), 500

    return EndPoints().listed_buildings(postcode=postcode, grade=grade, listed_after=listed_after)
