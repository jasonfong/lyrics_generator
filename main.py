import json

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_basicauth import BasicAuth

from models.line import Line
from web.views import web_blueprint


app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(web_blueprint, url_prefix='/web')

basic_auth = BasicAuth(app)


@app.route('/')
def index():
    return redirect(url_for('web.landing'))

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')


@app.route('/info')
def info():
    return jsonify(
        routes=[repr(item) for item in app.url_map.iter_rules()],
    )

@app.route('/admin/moderate', methods=['GET'])
@basic_auth.required
def moderate():
    lines = Line.get_unapproved()
    return render_template('moderate.html', lines=lines)


@app.route('/admin/moderate_action', methods=['POST'])
@basic_auth.required
def moderate_action():
    data = request.get_json()

    status = data['status']
    line_id = data['line_id']

    line = Line.get(line_id)
    found = False

    if line:
        line.status = status
        line.save()
        found = True

    return jsonify(
        id=line_id,
        status=status,
        found=found,
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
