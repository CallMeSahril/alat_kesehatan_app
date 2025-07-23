from flask import Flask
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

app = Flask(__name__)
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


@app.template_filter('bulan_nama')
def bulan_nama(bulan):
    nama_bulan = [
        "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    return nama_bulan[bulan]


if __name__ == '__main__':
    app.run(port=5003, debug=True)
