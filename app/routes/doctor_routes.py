from flask import (

    Blueprint,

    render_template,

    redirect,

    url_for,

    abort

)

from flask_login import (

    login_required,

    current_user

)


doctor_bp = Blueprint(

    "doctor",

    __name__,

    url_prefix="/doctor"

)


@doctor_bp.route(

    "/dashboard"

)

@login_required

def doctor_dashboard():


    if current_user.role != "doctor":

        abort(

            403

        )


    return render_template(

        "doctor_dashboard.html"

    )