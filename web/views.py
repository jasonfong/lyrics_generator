from flask import (
    Blueprint, current_app, jsonify, render_template, redirect, request, url_for)

import requests

from models.line import Line
from generator.generator import LyricsGenerator


web_blueprint = Blueprint('web', __name__,
                          template_folder='templates')


@web_blueprint.route('/')
def index():
    return redirect(url_for('web.landing'))


@web_blueprint.route('/submit_line', methods=['GET', 'POST'])
def submit_line():
    if request.method == 'POST':
        data = request.form

        recaptcha_token = data.get('captcha')
        resp = requests.post(
            url='https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': current_app.config['RECAPTCHA_KEY'],
                'response': recaptcha_token,
            }
        )
        if not resp.json()['success']:
            return redirect(url_for('web.landing'))

        social_id = data.get('social_id')
        if social_id:
            social_type = data.get('social_type')
        else:
            social_type = 'anonymous'

        line_ref = Line(
            text=data.get('text'),
            line_type=data.get('line_type'),
            social_type=social_type,
            social_id=social_id,
        )
        line_ref.save()
        return render_template('confirmation.html')

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


@web_blueprint.route('/generate', methods=['GET'])
def generate():
    if not current_app.config['GENERATE_ENABLED']:
        return redirect(url_for('web.landing'))

    generated = LyricsGenerator().generate()

    return render_template(
        'generate.html',
        pre_chorus=generated['pre-chorus'],
        chorus=generated['chorus'],
        verse=generated['verse'],
        bridge=generated['bridge'],
    )


@web_blueprint.route('/landing', methods=['GET'])
def landing():
    return render_template('landing.html')
