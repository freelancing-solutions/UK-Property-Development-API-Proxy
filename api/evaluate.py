# UK Property Evaluation API

from flask import request, jsonify, Blueprint
from endpoints.endpoints import EndPoints
from library import api_cache_decorator

evaluate = Blueprint('evaluate', __name__)



@evaluate.route('/api/v1/planning', methods=['POST'])
@api_cache_decorator
def planning(cache: any) -> tuple:
    if not (cache is None):
        return cache
    planning_data: dict = request.get_json()
    if 'postcode' in planning_data and not (planning_data['postcode'] == ""):
        postcode: str = planning_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'decision_rating' in planning_data and not (planning_data['decision_rating'] == ""):
        decision_rating: str = planning_data['decision_rating']
    else:
        return jsonify({'status': 'failure', 'message': 'decision_rating is required'}), 500

    if 'category' in planning_data and not (planning_data['category'] == ""):
        category: str = planning_data['category']
    else:
        return jsonify({'status': 'failure', 'message': 'category is required'}), 500

    if 'max_age_decision' in planning_data and not (planning_data['max_age_decision'] == ""):
        max_age_decision: int = int(planning_data['max_age_decision'])
    else:
        return jsonify({'status': 'failure', 'message': 'max_age_decision is required'}), 500

    if 'results' in planning_data and not (planning_data['results'] == ""):
        results: int = int(planning_data['results'])
    else:
        return jsonify({'status': 'failure', 'message': 'results is required'}), 500

    return EndPoints().planning(postcode=postcode, decision_rating=decision_rating, category=category,
                                max_age_decision=max_age_decision, results=results)


@evaluate.route('/api/v1/freehold-titles', methods=['POST'])
@api_cache_decorator
def freehold_title(cache: any) -> tuple:
    if not (cache is None):
        return cache
    freehold_data: dict = request.get_json()
    if 'postcode' in freehold_data and not (freehold_data['postcode'] == ""):
        postcode: str = freehold_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    return EndPoints().freehold_titles(postcode=postcode)


@evaluate.route('/api/v1/title-info', methods=['POST'])
@api_cache_decorator
def title_info(cache: any) -> tuple:
    if not (cache is None):
        return cache
    title_data: dict = request.get_json()
    if 'title' in title_data and not (title_data['title'] == ""):
        title: str = title_data['title']
    else:
        return jsonify({'status': 'failure', 'message': 'title is required'}), 500

    return EndPoints().title_info(title=title)


@evaluate.route('/api/v1/stamp-duty', methods=['POST'])
@api_cache_decorator
def stamp_duty(cache: any) -> tuple:
    if not (cache is None):
        return cache
    stamp_data: dict = request.get_json()
    if 'value' in stamp_data and not (stamp_data['value'] == ""):
        value: int = int(stamp_data['value'])
    else:
        return jsonify({'status': 'failure', 'message': 'value is required'}), 500
    if 'country' in stamp_data and not (stamp_data['country'] == ""):
        country: str = stamp_data['country']
    else:
        return jsonify({'status': 'failure', 'message': 'country is required'}), 500

    if 'additional' in stamp_data and not (stamp_data['additional'] == ""):
        additional: int = int(stamp_data['additional'])
    else:
        return jsonify({'status': 'failure', 'message': 'additional is required'}), 500

    return EndPoints().stamp_duty(value=value, country=country, additional=additional)


@evaluate.route('/api/v1/green-belt', methods=['POST'])
@api_cache_decorator
def green_belt(cache: any) -> tuple:
    if not (cache is None):
        return cache
    green_belt_data: dict = request.get_json()
    if 'postcode' in green_belt_data and not (green_belt_data['postcode'] == ""):
        postcode: str = green_belt_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().green_belt(postcode=postcode)


@evaluate.route('/api/v1/national-park', methods=['POST'])
@api_cache_decorator
def national_park(cache: any) -> tuple:
    if not (cache is None):
        return cache
    national_park_data: dict = request.get_json()
    if 'postcode' in national_park_data and not (national_park_data['postcode'] == ""):
        postcode: str = national_park_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().national_park(postcode=postcode)


@evaluate.route('/api/v1/aobn', methods=['POST'])
@api_cache_decorator
def aobn(cache: any) -> tuple:
    if not (cache is None):
        return cache
    aobn_data: dict = request.get_json()
    if 'postcode' in aobn_data and not (aobn_data['postcode'] == ""):
        postcode: str = aobn_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().aonb(postcode=postcode)


@evaluate.route('/api/v1/flood-risk', methods=['POST'])
@api_cache_decorator
def flood_risk(cache: any) -> tuple:
    if not (cache is None):
        return cache
    flood_data: dict = request.get_json()
    if 'postcode' in flood_data and not (flood_data['postcode'] == ""):
        postcode: str = flood_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().flood_risk(postcode=postcode)


@evaluate.route('/api/v1/internet-speed', methods=['POST'])
@api_cache_decorator
def internet_speed(cache: any) -> tuple:
    if not (cache is None):
        return cache
    internet_data: dict = request.get_json()
    if 'postcode' in internet_data and not (internet_data['postcode'] == ""):
        postcode: str = internet_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().internet_speed(postcode=postcode)


@evaluate.route('/api/v1/build-cost', methods=["POST"])
@api_cache_decorator
def build_cost(cache: any) -> tuple:
    if not (cache is None):
        return cache

    build_cost_data: dict = request.get_json()
    if 'postcode' in build_cost_data and not (build_cost_data['postcode'] == ""):
        postcode: str = build_cost_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    if 'property_type' in build_cost_data and not (build_cost_data['property_type'] == ""):
        property_type: str = build_cost_data['property_type']
    else:
        return jsonify({'status': 'failure', 'message': 'property_type is required'}), 500

    if 'internal_area' in build_cost_data and not (build_cost_data['internal_area'] == ""):
        internal_area: int = int(build_cost_data['internal_area'])
    else:
        return jsonify({'status': 'failure', 'message': 'internal_area is required'}), 500

    if 'finish_quality' in build_cost_data and not (build_cost_data['finish_quality'] == ""):
        finish_quality: str = build_cost_data['finish_quality']
    else:
        return jsonify({'status': 'failure', 'message': 'finish_quality is required'}), 500
    return EndPoints().build_cost(postcode=postcode, property_type=property_type, internal_area=internal_area,
                                  finish_quality=finish_quality)


@evaluate.route('/api/v1/ptal', methods=['POST'])
@api_cache_decorator
def ptal(cache: any) -> tuple:
    if not (cache is None):
        return cache

    ptal_data: dict = request.get_json()
    if 'postcode' in ptal_data and not (ptal_data['postcode'] == ""):
        postcode: str = ptal_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().ptal(postcode=postcode)


@evaluate.route('/api/v1/council-tax', methods=['POST'])
@api_cache_decorator
def council_tax(cache: any) -> tuple:
    if not (cache is None):
        return cache

    council_data: dict = request.get_json()
    if 'postcode' in council_data and not (council_data['postcode'] == ""):
        postcode: str = council_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().council_tax(postcode=postcode)


@evaluate.route('/api/v1/floor-areas', methods=['POST'])
@api_cache_decorator
def floor_areas(cache: any) -> tuple:
    if not (cache is None):
        return cache

    floor_data: dict = request.get_json()
    if 'postcode' in floor_data and not (floor_data['postcode'] == ""):
        postcode: str = floor_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500
    return EndPoints().floor_areas(postcode=postcode)


@evaluate.route('/api/v1/listed-buildings', methods=['POST'])
@api_cache_decorator
def listed_buildings(cache: any) -> tuple:
    if not (cache is None):
        return cache

    listed_data: dict = request.get_json()
    if 'postcode' in listed_data and not (listed_data['postcode'] == ""):
        postcode: str = listed_data['postcode']
    else:
        return jsonify({'status': 'failure', 'message': 'postcode is required'}), 500

    if 'grade' in listed_data and not (listed_data['grade'] == ""):
        grade: str = listed_data['grade']
    else:
        return jsonify({'status': 'failure', 'message': 'grade is required'}), 500

    if 'listed_after' in listed_data and not (listed_data['listed_after'] == ""):
        listed_after: int = int(listed_data['listed_after'])
    else:
        return jsonify({'status': 'failure', 'message': 'listed_after is required'}), 500

    return EndPoints().listed_buildings(postcode=postcode, grade=grade, listed_after=listed_after)
