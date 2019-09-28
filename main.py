import json

from flask import Flask, jsonify, redirect, url_for
from web.views import web_blueprint


app = Flask(__name__)
app.register_blueprint(web_blueprint, url_prefix='/web')


@app.route('/')
def index():
    return redirect(url_for('web.landing'))


@app.route('/info')
def hello():
    return jsonify(
        routes=[repr(item) for item in app.url_map.iter_rules()],
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
