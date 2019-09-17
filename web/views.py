from flask import Blueprint, jsonify, render_template, request

from models.line import Line

from generator.generator import LyricsGenerator


web_blueprint = Blueprint('web', __name__,
                          template_folder='templates')

@web_blueprint.route('/hello')
def hello():
    return 'hello from the blueprint'


@web_blueprint.route('/submit_line', methods=['GET', 'POST'])
def submit_line():
    if request.method == 'POST':
        data = request.form
        line_ref = Line(
            text=data.get('text'),
            line_type=data.get('line_type'),
            social_type=data.get('social_type'),
            social_id=data.get('social_id'),
            chorus_lines=data.get('chorus'),
            pre_chorus_lines=data.get('pre_chorus'),
            verse_lines=data.get('verse'),
            bridge_lines=data.get('bridge'),
        )
        line_ref.save()
        return render_template(
            'accepted_line.html',
            text=line_ref.text,
            social_type=line_ref.social_type,
            social_id=line_ref.social_id,
        )

    else:
        return render_template(
            'submit_line.html',
            social_types=Line.social_type_choices,
            line_types=Line.line_type_choices,
            chorus_lines=Line.chorus,
            pre_chorus_lines=Line.pre_chorus,
            verse_lines=Line.verse,
            bridge_lines=Line.bridge,
        )


@web_blueprint.route('/view_lines', methods=['GET'])
def view_lines():
    lines = Line.get_all()
    return render_template('view_lines.html', lines=lines)


@web_blueprint.route('/admin/moderate', methods=['GET'])
def moderate():
    lines = Line.get_unapproved()
    return render_template('moderate.html', lines=lines)


@web_blueprint.route('/admin/moderate_action', methods=['POST'])
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


@web_blueprint.route('/generate', methods=['GET'])
def generate():
    generated = LyricsGenerator().generate()

    return render_template(
        'generate.html',
        pre_chorus=generated['pre-chorus'].text,
        chorus=generated['chorus'].text,
        verse=generated['verse'].text,
        bridge=generated['bridge'].text,
    )


@web_blueprint.route('/landing', methods=['GET'])
def landing():
    return render_template('landing.html')
