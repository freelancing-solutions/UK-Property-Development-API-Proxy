# UK Area API
from flask import request, jsonify, Blueprint
from endpoints.endpoints import EndPoints
from library import api_cache_decorator
from library.config import Config
from store.store import AdminView

automations_bp = Blueprint('automations', __name__)



@automations_bp.route('/api/v1/property-notifications', methods=['POST', 'GET'])
def property_notifications():
    if request.method == "GET":
        return jsonify({'status': 'success', 'message': 'notification user successfully received'}), 200
    else:
        notifications_data = request.get_json()
        print(notifications_data)
        if "email" in notifications_data:
            email = notifications_data['email']
        else:
            return jsonify({'status': 'failure', 'message': 'unable to located email'}), 500
        if "name" in notifications_data:
            name = notifications_data['name']
        else:
            return jsonify({'status': 'failure', 'message': 'unable to located name'}), 500
        if "uid" in notifications_data:
            uid = notifications_data['surname']
        else:
            return jsonify({'status': 'failure', 'message': 'unable to located uid'}), 500

        return AdminView(config=Config()).add_notifications_user(email=email, name=name, uid=uid)



