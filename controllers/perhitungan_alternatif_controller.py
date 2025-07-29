from flask import Blueprint, render_template
from models.perhitungan_alternatif_model import PerhitunganAlternatifModel

perhitungan_alternatif_bp = Blueprint(
    'perhitungan_alternatif_bp', __name__, url_prefix='/perhitungan-alternatif')


@perhitungan_alternatif_bp.route('/')
def index():
    bobot_kriteria = PerhitunganAlternatifModel.get_bobot_kriteria()
    data = PerhitunganAlternatifModel.get_nilai_alternatif()

    # Struktur: {id_data_alat: {total_skor, nama_customer, nama_alat}}
    hasil = {}
    for row in data:
        id_alt = row['id_data_alat']
        nilai = row['nilai']
        bobot = bobot_kriteria.get(row['id_kriteria'], 0)
        skor = nilai * bobot

        if id_alt not in hasil:
            hasil[id_alt] = {
                'id_data_alat': id_alt,
                'nama_customer': row['nama_customer'],
                'nama_alat': row['nama_alat'],
                'skor_akhir': 0
            }

        hasil[id_alt]['skor_akhir'] += skor

    # Ubah ke list dan urutkan
    ranking = sorted(
        hasil.values(), key=lambda x: x['skor_akhir'], reverse=True)

    # Simpan ke DB
    PerhitunganAlternatifModel.simpan_hasil(ranking)

    return render_template('perhitungan_alternatif/index.html', ranking=ranking)
