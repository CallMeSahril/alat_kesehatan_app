# controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

# ✅ Contoh user dummy (ganti ke cek DB nanti)
USERS = {
    "admin@example.com": {
        "password": "admin123",   # ganti ke hash/DB kalau sudah siap
        "name": "Administrator"
    }
}


def is_logged_in():
    return session.get("user") is not None


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = USERS.get(email)
        if user and user["password"] == password:
            # simpan info minimal di session
            session["user"] = {"email": email, "name": user["name"]}
            flash("Berhasil login.", "success")

            # arahkan ke halaman tujuan (kalau ada ?next=) atau ke beranda
            next_url = request.args.get("next") or url_for("alat_bp.index")
            return redirect(next_url)
        else:
            flash("Email atau password salah.", "danger")

    # GET -> tampilkan form
    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST", "GET"])
def logout():
    if is_logged_in():
        session.pop("user", None)
        flash("Anda telah logout.", "info")
    return redirect(url_for("auth_bp.login"))
