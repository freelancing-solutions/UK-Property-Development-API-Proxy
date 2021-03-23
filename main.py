import os
from flask import Flask, render_template
from api.sales import sales
from api.rental import rental
from api.area import area
from api.evaluate import evaluate

app = Flask(__name__, template_folder='templates', static_folder='static')
# Press the green button in the gutter to run the script.

app.register_blueprint(sales)
app.register_blueprint(rental)
app.register_blueprint(area)
app.register_blueprint(evaluate)


@app.route('/', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
