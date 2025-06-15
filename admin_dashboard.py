from flask import Blueprint, render_template, session, redirect, url_for

admin_dashboard_bp = Blueprint("admin_dashboard", __name__)

@admin_dashboard_bp.route("/admin-dashboard")
def admin_dashboard():
    # Restrict access to only logged-in admins
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("login.login"))  # Adjust if your login blueprint is different

    return render_template("admin_dashboard.html")
