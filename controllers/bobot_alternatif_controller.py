from flask import Blueprint, render_template, request, redirect
from models.data_alat_model import DataAlatModel
from models.kriteria_model import KriteriaModel
from models.bobot_alternatif_model import BobotAlternatifModel
from datetime import datetime
from collections import defaultdict

bobot_alternatif_bp = Blueprint(
    'bobot_alternatif_bp', __name__, url_prefix='/bobot-alternatif'
)


@bobot_alternatif_bp.route('/')
def index():
    data_alat = DataAlatModel.get_all()
    kriteria = KriteriaModel.get_all()
    all_bobot = BobotAlternatifModel.get_all()

    # Kelompokkan bobot alternatif per id_data_alat dan id_kriteria
    nilai_per_alat = defaultdict(dict)
    for row in all_bobot:
        nilai_per_alat[row['id_data_alat']][row['id_kriteria']] = row['nilai']

    generated_ids = set(nilai_per_alat.keys())

    return render_template(
        'bobot_alternatif/index.html',
        data_alat=data_alat,
        kriteria=kriteria,
        generated_ids=generated_ids,
        nilai_per_alat=nilai_per_alat
    )


@bobot_alternatif_bp.route('/generate/<int:id_data>')
def generate(id_data):
    data = DataAlatModel.get_by_id(id_data)
    kriteria = KriteriaModel.get_all()

    if not data:
        return f"Data dengan ID {id_data} tidak ditemukan", 404

    map_kondisi = {
        'Ex Service': 5,
        'Good': 1
    }

    nilai = []
    kondisi = data['nama_kondisi']
    customer = data['nama_customer']
    print(
        f"Processing ID {id_data} - Kondisi: {kondisi} - Customer: {customer}")
    for k in kriteria:
        nama_kriteria = k['nama_kriteria']

        if nama_kriteria == 'Tingkat Kerusakan':
            nilai.append(map_kondisi.get(kondisi, 1))

        elif nama_kriteria == 'Frekuensi Pemakaian':
            nilai.append(data['jumlah_maintenance'])

        elif nama_kriteria == 'Umur Alat':
            tahun_alat = int(data['tahun_produksi'])
            umur = datetime.now().year - tahun_alat
            nilai.append(max(1, umur))

        elif nama_kriteria == 'Tanggal Instalasi':
            instalasi = data['tgl_instalasi']
            umur = datetime.now().year - instalasi.year
            nilai.append(max(1, 10 - umur))

        elif nama_kriteria == 'Jenis Customer':
            if 'RSUD' in customer or 'RSU' in customer:
                nilai.append(5)
            elif 'RS' in customer:
                nilai.append(4)
            elif 'Klinik' in customer:
                nilai.append(2)
            else:
                nilai.append(1)
        else:
            # Default jika kriteria tidak dikenali
            nilai.append(1)

    print(f"Nilai: {nilai} - Jumlah Kriteria: {len(kriteria)}")

    if len(nilai) == len(kriteria):
        BobotAlternatifModel.delete_by_data_alat(id_data)
        for i, k in enumerate(kriteria):
            BobotAlternatifModel.insert(id_data, k['id_kriteria'], nilai[i])
    else:
        print(
            f"⚠️ SKIP ID {id_data} - Nilai: {len(nilai)} | Kriteria: {len(kriteria)}")

    return redirect('/bobot-alternatif')


@bobot_alternatif_bp.route('/generate-all')
def generate_all():
    data_list = DataAlatModel.get_all()
    kriteria = KriteriaModel.get_all()
    map_kondisi = {
        'Ex Service': 5,
        'Good': 1
    }

    for data in data_list:
        nilai = []
        kondisi = data['nama_kondisi']
        customer = data['nama_customer']

        for k in kriteria:
            nama_kriteria = k['nama_kriteria']

            if nama_kriteria == 'Tingkat Kerusakan':
                nilai.append(map_kondisi.get(kondisi, 1))

            elif nama_kriteria == 'Frekuensi Pemakaian':
                nilai.append(data['jumlah_maintenance'])

            elif nama_kriteria == 'Umur Alat':
                tahun_alat = int(data['tahun_produksi'])
                umur = datetime.now().year - tahun_alat
                nilai.append(max(1, umur))

            elif nama_kriteria == 'Tanggal Instalasi':
                instalasi = data['tgl_instalasi']
                umur = datetime.now().year - instalasi.year
                nilai.append(max(1, 10 - umur))

            elif nama_kriteria == 'Jenis Customer':
                if 'RSUD' in customer or 'RSU' in customer:
                    nilai.append(5)
                elif 'RS' in customer:
                    nilai.append(4)
                elif 'Klinik' in customer:
                    nilai.append(2)
                else:
                    nilai.append(1)
            else:
                # Default nilai jika kriteria tidak dikenali
                nilai.append(1)

        # Print debug setelah loop kriteria selesai
        print(f"nilai {nilai} - kriteria: {kriteria}")

        # Simpan hanya jika jumlah nilai sama dengan jumlah kriteria
        if len(nilai) == len(kriteria):
            BobotAlternatifModel.delete_by_data_alat(data['id_data'])
            for i, k in enumerate(kriteria):
                BobotAlternatifModel.insert(
                    data['id_data'], k['id_kriteria'], nilai[i])
        else:
            print(
                f"⚠️ SKIP ID {data['id_data']} - Nilai: {len(nilai)} | Kriteria: {len(kriteria)}")

    return redirect('/bobot-alternatif')
