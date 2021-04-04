# UK Area API
from flask import request, jsonify, Blueprint
from endpoints.endpoints import EndPoints
from library import api_cache_decorator
automations_bp = Blueprint('automations', __name__)


@automations_bp.route('/api/v1/property-notifications', methods=['POST', 'GET'])
def property_notifications():
    if request.method == "GET":
        pass
    else:
        notifications_data = request.get_json()

        return jsonify({'status': 'success', 'message': 'notification user successfully received'}), 200


