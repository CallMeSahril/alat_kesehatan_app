from flask import Blueprint, render_template
from models.perhitungan_bobot_model import PerhitunganBobotModel
import numpy as np

perhitungan_bobot_bp = Blueprint('perhitungan_bobot_bp', __name__, url_prefix='/perhitungan-bobot')


@perhitungan_bobot_bp.route('/')
def index():
    kriteria, matriks = PerhitunganBobotModel.get_matriks_kriteria()

    # Normalisasi matriks
    kolom_total = matriks.sum(axis=0)
    normalisasi = matriks / kolom_total
    bobot = normalisasi.mean(axis=1)

    # Simpan bobot
    PerhitunganBobotModel.simpan_bobot(kriteria, bobot)

    return render_template('perhitungan_bobot/index.html',
                           kriteria=kriteria,
                           matriks=matriks,
                           normalisasi=normalisasi,
                           bobot=bobot)
