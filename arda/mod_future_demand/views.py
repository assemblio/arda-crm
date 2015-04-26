from flask import Blueprint, render_template
from flask.ext.security import login_required


mod_future_demand = Blueprint('future-demand', __name__, url_prefix='/future/demand/requests')


@mod_future_demand.route('', methods=['GET'])
@login_required
def future_demand():
    return render_template('mod_future_demand/future_request.html')
