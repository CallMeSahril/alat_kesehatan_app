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
    # Hitung λ_max
    lambda_max = np.sum(np.dot(matriks, bobot) / bobot) / len(kriteria)

    # Hitung CI (Consistency Index)
    n = len(kriteria)
    CI = (lambda_max - n) / (n - 1) if n > 1 else 0

    # Nilai RI (Random Index) berdasarkan jumlah kriteria
    RI_dict = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
        6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
    }
    RI = RI_dict.get(n, 1.49)  # default max RI

    # Hitung CR (Consistency Ratio)
    CR = CI / RI if RI != 0 else 0
    konsisten = CR < 0.1
    # Simpan bobot
    PerhitunganBobotModel.simpan_bobot(kriteria, bobot)

    return render_template('perhitungan_bobot/index.html',
                           kriteria=kriteria,
                           matriks=matriks,
                           normalisasi=normalisasi,
                           bobot=bobot,
                           lambda_max=lambda_max,
                           CI=CI,
                           RI=RI,
                           CR=CR,
                           konsisten=konsisten)

