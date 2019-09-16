from flask import Blueprint, jsonify, render_template, request

from models.line import Line


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
            social_type=data.get('social_type'),
            social_id=data.get('social_id'),
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
        )


@web_blueprint.route('/view_lines', methods=['GET'])
def view_lines():
    lines = Line.get_all()
    return render_template('view_lines.html', lines=lines)



@web_blueprint.route('/admin/moderate', methods=['GET'])
def moderate():
    lines = Line.get_unapproved()
    return render_template('moderate.html', lines=lines)
