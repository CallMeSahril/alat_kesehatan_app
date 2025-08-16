from flask import Flask, request, redirect, url_for, session
from controllers.alat_controller import alat_bp
from controllers.tahun_controller import tahun_bp
from controllers.customer_controller import customer_bp
from controllers.data_alat_controller import data_alat_bp
from controllers.kondisi_controller import kondisi_bp
from controllers.kriteria_controller import kriteria_bp
from controllers.bobot_controller import bobot_bp
from controllers.perhitungan_bobot_controller import perhitungan_bobot_bp
from controllers.bobot_alternatif_controller import bobot_alternatif_bp
from controllers.perhitungan_alternatif_controller import perhitungan_alternatif_bp
from controllers.jadwal_controller import jadwal_bp
# <- pastikan file ini ada (route login/logout)
from controllers.auth_controller import auth_bp

app = Flask(__name__)
# diperlukan untuk session/flash
app.config["SECRET_KEY"] = "ganti-ini-dengan-yang-sangat-rahasia"

# ===== Register Blueprints =====
app.register_blueprint(alat_bp)
app.register_blueprint(tahun_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(data_alat_bp)
app.register_blueprint(kondisi_bp)
app.register_blueprint(kriteria_bp)
app.register_blueprint(bobot_bp)
app.register_blueprint(perhitungan_bobot_bp)
app.register_blueprint(bobot_alternatif_bp)
app.register_blueprint(perhitungan_alternatif_bp)
app.register_blueprint(jadwal_bp)
app.register_blueprint(auth_bp)

# ===== Filter/Helper =====


@app.template_filter('bulan_nama')
def bulan_nama(bulan):
    nama_bulan = [
        "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    return nama_bulan[bulan]


def is_logged_in():
    return session.get("user") is not None

# ===== Redirect root ke login/jadwal =====


@app.route("/")
def root():
    if not is_logged_in():
        return redirect(url_for("auth_bp.login", next=request.path))
    # jika sudah login, arahkan ke halaman utama yang kamu inginkan
    return redirect(url_for("jadwal_bp.index"))


# ===== Paksa login untuk semua endpoint kecuali whitelist publik =====
PUBLIC_ENDPOINTS = {
    "auth_bp.login",   # halaman login
    # logout biar bisa keluar meski belum login (aman-aman saja)
    "auth_bp.logout",
    "static",          # file statis
}


@app.before_request
def require_login():
    # izinkan endpoint publik & favicon
    if request.endpoint in PUBLIC_ENDPOINTS or request.path == "/favicon.ico":
        return
    # jika belum login, paksa ke login
    if not is_logged_in():
        return redirect(url_for("auth_bp.login", next=request.path))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5033, debug=True)
