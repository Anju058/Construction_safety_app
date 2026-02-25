import importlib
import importlib.metadata as _md
import werkzeug

# Ensure werkzeug.__version__ exists for Flask testing compatibility (Werkzeug 3.x removed __version__)
try:
    if not hasattr(werkzeug, '__version__'):
        try:
            werkzeug.__version__ = _md.version('werkzeug')
        except Exception:
            werkzeug.__version__ = '3.0.0'
except Exception:
    pass

from flask import Flask, render_template, request, session
from ahp import calculate_ahp, build_matrix_from_comparisons, HAZARD_NAMES, SHORT_NAMES
from cos import calculate_budget_allocation
from ahp_equipment import (
    build_equipment_matrix,
    calculate_equipment_ahp,
    EQUIPMENT_NAMES as EQUIP_NAMES,
)

app = Flask(__name__)
app.secret_key = 'construction_safety_app_key'

# Register custom zip filter for Jinja2
@app.template_filter('zip')
def zip_filter(a, b):
    """Custom zip filter for Jinja2 templates"""
    return zip(a, b)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ahp', methods=['GET', 'POST'])
def ahp():
    if request.method == 'POST':
        # Get all form inputs and build pairwise comparison matrix
        comparisons = {}
        for i in range(9):
            for j in range(i + 1, 9):
                key = f'h{i}_h{j}'
                if key in request.form:
                    try:
                        comparisons[key] = float(request.form[key])
                    except ValueError:
                        comparisons[key] = 1.0  # Default to 1 if invalid
        
        # Build matrix from user inputs
        matrix = build_matrix_from_comparisons(comparisons, n=9)
        
        # Calculate AHP
        hazard_names, weights, lambda_max, CI, CR, consistency_status = calculate_ahp(matrix)
        
        # Store weights in session for COS calculation
        session['hazard_weights'] = weights.tolist()
        session['hazard_names'] = hazard_names

        return render_template(
            'dashboard.html',
            criteria=hazard_names,
            weights=[round(w, 4) for w in weights],
            lambda_max=round(lambda_max, 4),
            CI=round(CI, 4),
            CR=round(CR, 4),
            consistency_status=consistency_status,
            show_risk_chart=True
        )

    return render_template('ahp_main.html', hazards=HAZARD_NAMES, short_names=SHORT_NAMES)



@app.route('/cos', methods=['GET', 'POST'])
def cos_route():
    if request.method == 'POST':
        total_budget = float(request.form['budget'])

        # Get weights from session or calculate defaults
        if 'hazard_weights' in session:
            risk_weights = session['hazard_weights']
            hazard_names = session['hazard_names']
        else:
            # Fallback: use identity matrix (all equal weights)
            import numpy as np
            weights = np.ones(9) / 9
            hazard_names = HAZARD_NAMES
            risk_weights = weights.tolist()

        allocation = calculate_budget_allocation(total_budget, risk_weights)

        return render_template(
            'dashboard.html',
            criteria=hazard_names,
            allocation=[round(a, 2) for a in allocation],
            total_budget=total_budget,
            show_budget_chart=True
        )

    return render_template('cos.html', hazards=HAZARD_NAMES, short_names=SHORT_NAMES)


@app.route('/equipment-ahp', methods=['GET', 'POST'])
def equipment_ahp():
    if request.method == 'POST':
        # read six comparisons from form
        keys = ['A_B', 'A_C', 'A_D', 'B_C', 'B_D', 'C_D']
        comps = {}
        for k in keys:
            val = request.form.get(k, '1')
            try:
                comps[k] = float(val)
            except Exception:
                comps[k] = 1.0

        matrix = build_equipment_matrix(comps)
        equipment_names, weights, lambda_max, CI, CR, consistency_status = calculate_equipment_ahp(matrix)

        # store in session for COS allocation
        session['equipment_weights'] = weights.tolist()
        session['equipment_names'] = equipment_names

        # Render a dedicated results page
        return render_template(
            'equipment_results.html',
            equipment=equipment_names,
            weights=[round(float(w), 4) for w in weights],
            lambda_max=round(lambda_max, 4),
            CI=round(CI, 4),
            CR=round(CR, 4),
            consistency_status=consistency_status,
            total_budget=None
        )

    return render_template('equipment_ahp.html', equipment=EQUIP_NAMES)


@app.route('/equipment-cos', methods=['GET', 'POST'])
def equipment_cos():
    if request.method == 'POST':
        total_budget = float(request.form.get('budget', 0))

        if 'equipment_weights' in session:
            weights = session['equipment_weights']
            names = session.get('equipment_names', EQUIP_NAMES)
        else:
            import numpy as np
            weights = (np.ones(4) / 4).tolist()
            names = EQUIP_NAMES

        allocation = calculate_budget_allocation(total_budget, weights)

        return render_template(
            'equipment_cos.html',
            equipment=names,
            weights=[float(w) for w in weights],
            allocation=[round(a, 2) for a in allocation],
            total_budget=round(total_budget, 2)
        )

    return render_template('equipment_cos.html', equipment=EQUIP_NAMES, weights=None, allocation=None, total_budget=None)



if __name__ == '__main__':
    app.run(debug=True)
