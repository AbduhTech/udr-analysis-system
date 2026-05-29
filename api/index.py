"""
UDR Analysis System — Flask app for Vercel deployment
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'udr_webapp'))

import base64
import tempfile

from flask import Flask, render_template, request, jsonify

from modules.observation_module   import analyze_observation, analyze_observation_demo
from modules.survey_module        import analyze_survey, analyze_survey_demo
from modules.case_study_module    import analyze_case_study, analyze_case_study_demo
from modules.triangulation_module import triangulate
from modules.report_generator     import generate_text_report
from modules.visualization        import (
    plot_ai_frequency, plot_udr_profile, plot_debugging_gap,
    plot_illusory_competence, plot_institutional_gap,
)

app = Flask(__name__, template_folder='templates')


def _b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/observation', methods=['POST'])
def api_observation():
    d = request.get_json()
    result = analyze_observation(
        int(d['students']), int(d['sessions']), int(d['ai_first']),
        int(d['unable']),   int(d['debug']),    int(d['reason']),
        int(d['passed']),   int(d['drop']),
    )
    return jsonify(result)


@app.route('/api/survey', methods=['POST'])
def api_survey():
    use_demo = request.form.get('use_demo', 'true') == 'true'
    if use_demo or 'csv' not in request.files or request.files['csv'].filename == '':
        return jsonify(analyze_survey_demo())
    f = request.files['csv']
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='wb') as tmp:
        f.save(tmp)
        tmp_path = tmp.name
    try:
        result = analyze_survey(tmp_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
    return jsonify(result)


@app.route('/api/case', methods=['POST'])
def api_case():
    d = request.get_json()
    result = analyze_case_study(
        int(d['claimed']),
        int(d['ta_u']), int(d['ta_d']), int(d['ta_r']),
        int(d['tb_u']), int(d['tb_d']), int(d['tb_r']),
        int(d['dep']),
        bool(d['explain_ai']),
        bool(d['ai_before']),
    )
    return jsonify(result)


@app.route('/api/triangulate', methods=['POST'])
def api_triangulate():
    d = request.get_json()
    obs  = d.get('obs')  or analyze_observation_demo()
    surv = d.get('surv') or analyze_survey_demo()
    case = d.get('case') or analyze_case_study_demo()
    final = triangulate(obs, surv, case)
    report = generate_text_report(obs, surv, case, final)
    return jsonify({**final, '_report': report})


@app.route('/api/figures', methods=['POST'])
def api_figures():
    d = request.get_json()
    surv = d.get('surv') or analyze_survey_demo()
    try:
        paths = [
            plot_ai_frequency(surv),
            plot_udr_profile(surv),
            plot_debugging_gap(surv),
            plot_illusory_competence(surv),
            plot_institutional_gap(surv),
        ]
        return jsonify({'figures': [_b64(p) for p in paths]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
