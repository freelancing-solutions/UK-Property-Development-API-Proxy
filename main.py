import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, render_template
from library.config import Config
from cachetools import cached, LRUCache, TTLCache

config = Config()

# Import API's
from api.sales import sales
from api.rental import rental
from api.area import area
from api.evaluate import evaluate


sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.3
)
app = Flask(__name__)
# Press the green button in the gutter to run the script.


# Registering API's
app.register_blueprint(sales)
app.register_blueprint(rental)
app.register_blueprint(area)
app.register_blueprint(evaluate)


@app.route('/', methods=['GET', 'POST'])
@cached(cache=TTLCache(maxsize=2048, ttl=60))
def main():
    """
        will display API Options, Save Default Values, for
        example
        property_types could be limited to certain types only
        finish_quality could be limited to high_quality and etc
        see Notes for different Options Available
    :return:
    """
    return render_template('admin.html')


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0


if __name__ == '__main__':
    app.run(debug=config.IS_DEV, use_reloader=config.IS_DEV, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
