from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from app import db, bcrypt, login_manager

from app.models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# ============================================
# USER LOADER
# ============================================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# ============================================
# REGISTER
# ============================================

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name"
        ).strip()

        email = request.form.get(
            "email"
        ).strip().lower()

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )


        # Validation

        if not name or not email or not password:

            flash(
                "All fields are required.",
                "error"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )


        # Check existing email

        existing_user = User.query.filter_by(

            email=email

        ).first()


        if existing_user:

            flash(
                "Email is already registered.",
                "error"
            )

            return redirect(
                url_for(
                    "auth.register"
                )
            )


        # Hash password

        password_hash = bcrypt.generate_password_hash(

            password

        ).decode(

            "utf-8"

        )


        # Create user

        user = User(

            name=name,

            email=email,

            password_hash=password_hash,

            role="patient"

        )


        db.session.add(user)

        db.session.commit()


        flash(

            "Registration successful. Please login.",

            "success"

        )


        return redirect(

            url_for(

                "auth.login"

            )

        )


    return render_template(

        "register.html"

    )


# ============================================
# LOGIN
# ============================================

@auth_bp.route(

    "/login",

    methods=["GET", "POST"]

)

def login():


    if request.method == "POST":


        email = request.form.get(

            "email"

        ).strip().lower()


        password = request.form.get(

            "password"

        )


        user = User.query.filter_by(

            email=email

        ).first()


        if user and bcrypt.check_password_hash(

            user.password_hash,

            password

        ):


            login_user(user)


            if user.role == "doctor":

                return redirect(

                    url_for(

                        "doctor.doctor_dashboard"

                    )

                )


            return redirect(

                url_for(

                    "dashboard.dashboard"

                )

            )


        flash(

            "Invalid email or password.",

            "error"

        )


    return render_template(

        "login.html"

    )


# ============================================
# LOGOUT
# ============================================

@auth_bp.route(

    "/logout"

)

@login_required

def logout():


    logout_user()


    flash(

        "You have been logged out.",

        "success"

    )


    return redirect(

        url_for(

            "auth.login"

        )

    )