import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from library.config import Config
from store.store import admin_view

config = Config()
if config.IS_DEBUG:
    config.set_debug_cors_header()
# Import API's
from api.sales import sales
from api.rental import rental
from api.area import area
from api.evaluate import evaluate

sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    integrations=[FlaskIntegration(), RedisIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.5
)
app = Flask(__name__)
# Press the green button in the gutter to run the script.
cors = CORS(app, resources={r"/api/*": {"origins": config.AUTHORIZED_ADDRESSES,
                                        "headers": ['Content-Type'],
                                        "methods": ['POST'],
                                        "max-age": "43200",
                                        "automatic_options": True}})

# Registering API's

app.register_blueprint(sales)
app.register_blueprint(rental)
app.register_blueprint(area)
app.register_blueprint(evaluate)


@app.route('/', methods=['GET', 'POST'])
# @cached(cache=TTLCache(maxsize=1024, ttl=600))
def main():
    """
        will display API Options, Save Default Values, for
        example
        property_types could be limited to certain types only
        finish_quality could be limited to high_quality and etc
        see Notes for different Options Available
    :return:
    """
    if request.method == "GET":
        return render_template('admin.html')


@app.route('/admin', methods=['GET', 'POST'])
# @cached(cache=TTLCache(maxsize=1024, ttl=600))
def admin():
    """
        will display API Options, Save Default Values, for
        example
        property_types could be limited to certain types only
        finish_quality could be limited to high_quality and etc
        see Notes for different Options Available
    :return:
    """
    return render_template('admin.html')


@app.route('/admin/<path:path>', methods=['GET', 'POST'])
def admin_defaults(path):
    if request.method == "GET":
        if path == "property-types":
            return admin_view.fetch_property_types()
        if path == "admin-api-defaults":
            return admin_view.fetch_all_admin_defaults()
        if path == "fetch-api-settings":
            return admin_view.get_settings()
        if path == "construction-dates":
            return admin_view.get_construction_dates()
        if path == "finish-quality":
            return admin_view.fetch_finishing_quality()

    if request.method == "POST":
        if path == "property-types":
            request_data = request.get_json()
            return admin_view.update_property_types(property_selections=request_data)
        if path == "construction-dates":
            request_data = request.get_json()
            return admin_view.update_dates_selected(dates_selected=request_data)

        if path == "finish-quality":
            request_data = request.get_json()
            return admin_view.update_finish_quality(finish_quality=request_data)

        if path == "shutdown-api":
            return admin_view.set_shutdown_status(status=True)

        if path == "restart-api":
            return admin_view.set_shutdown_status(status=False)


# handling warp requests
@app.route('/_ah/warmup')
def warmup():
    # Handle your warmup logic here, e.g. set up a database connection pool
    return '', 200, {}


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


if __name__ == '__main__':
    app.run(debug=config.IS_DEBUG, use_reloader=config.IS_DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


