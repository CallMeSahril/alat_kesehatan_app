from flask import Blueprint, render_template, request
from models.data_alat_model import DataAlatModel
from datetime import datetime

jadwal_bp = Blueprint('jadwal_bp', __name__, url_prefix='/jadwal')


@jadwal_bp.route('/')
def index():
    tahun = request.args.get('tahun', default=None, type=int)
    current_year = datetime.now().year
    tahun = tahun if tahun else current_year
    years = list(range(current_year - 10, current_year + 11))

    data_alat = DataAlatModel.get_all()
    skor_dict = DataAlatModel.get_skor_akhir()
    kolom_maintenance = [f'm{i}' for i in range(1, 11)]

    data_per_bulan = {i: [] for i in range(1, 13)}
    rekap_tahun = {}
    rekap_bulan = {i: 0 for i in range(1, 13)}
    tahun_dari_m_1_10 = set()
    jadwal_tercatat = set()

    for alat in data_alat:
        alat['skor_akhir'] = skor_dict.get(alat['id_data'], 0)

        for kolom in kolom_maintenance:
            tgl_str = alat.get(kolom)
            if not tgl_str:
                continue
            try:
                tgl = datetime.strptime(tgl_str, '%Y-%m')
            except:
                continue

            tahun_dari_m_1_10.add(tgl.year)
            rekap_tahun[tgl.year] = rekap_tahun.get(tgl.year, 0) + 1

            if tgl.year == tahun:
                key = (alat['id_data'], kolom.upper(), tgl.year, tgl.month)

                # 💥 Tambahkan debug untuk lihat data ganda
                for existing in data_per_bulan[tgl.month]:
                    if (
                        existing['id_data'] == alat['id_data'] and
                        existing.get('jadwal_ke') == kolom.upper() and
                        existing.get('jadwal_date') == tgl
                    ):
                        print(f"🛑 DUPLIKAT TERDETEKSI:")
                        print(f"Alat ID      : {alat['id_data']}")
                        print(f"Nama Alat    : {alat['nama_alat']}")
                        print(f"Customer     : {alat['nama_customer']}")
                        print(f"Tanggal      : {tgl_str}")
                        print(f"Kolom        : {kolom}")
                        print(f"Skor Akhir   : {alat['skor_akhir']}")
                        print("-" * 50)

                # Lanjutkan seperti biasa
                if key in jadwal_tercatat:
                    continue
                jadwal_tercatat.add(key)

                rekap_bulan[tgl.month] += 1
                data_alat_baru = alat.copy()
                data_alat_baru['jadwal_ke'] = kolom.upper()
                data_alat_baru['jadwal_date'] = tgl
                data_per_bulan[tgl.month].append(data_alat_baru)

    print(data_per_bulan)

    return render_template(
        'jadwal/index.html',
        data_per_bulan=data_per_bulan,
        tahun=tahun,
        years=years,
        rekap_tahun=rekap_tahun,
        rekap_bulan=rekap_bulan,
        tahun_maintenance=sorted(tahun_dari_m_1_10)
    )

@jadwal_bp.route('/print')
def print_view():
    tahun = request.args.get('tahun', default=None, type=int)
    years = DataAlatModel.get_years()
    if not tahun or tahun not in years:
        tahun = years[0] if years else datetime.now().year

    data_alat = DataAlatModel.get_all_filtered_by_year(tahun)
    skor_dict = DataAlatModel.get_skor_akhir()
    kolom_maintenance = [f'm{i}' for i in range(1, 11)]

    data_per_bulan = {i: [] for i in range(1, 13)}
    rekap_tahun = {}
    rekap_bulan = {i: 0 for i in range(1, 13)}
    tahun_dari_m_1_10 = set()
    jadwal_tercatat = set()

    for alat in data_alat:
        alat['skor_akhir'] = skor_dict.get(alat['id_data'], 0)

        for kolom in kolom_maintenance:
            tgl_str = alat.get(kolom)
            if not tgl_str:
                continue
            try:
                tgl = datetime.strptime(tgl_str, '%Y-%m')
            except:
                continue

            tahun_dari_m_1_10.add(tgl.year)
            rekap_tahun[tgl.year] = rekap_tahun.get(tgl.year, 0) + 1

            if tgl.year == tahun:
                key = (alat['id_data'], tgl.year, tgl.month)
                if key in jadwal_tercatat:
                    continue
                jadwal_tercatat.add(key)

                rekap_bulan[tgl.month] += 1
                data_alat_baru = alat.copy()
                data_alat_baru['jadwal_ke'] = kolom.upper()
                data_alat_baru['jadwal_date'] = tgl
                data_per_bulan[tgl.month].append(data_alat_baru)

    # Tambah nama hari (Indonesia)
    hari_id = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    now = datetime.now()
    current_day = hari_id[now.weekday()]

    return render_template(
        'jadwal/print_jadwal.html',
        data_per_bulan=data_per_bulan,
        tahun=tahun,
        years=years,
        rekap_tahun=rekap_tahun,
        rekap_bulan=rekap_bulan,
        tahun_maintenance=sorted(tahun_dari_m_1_10),
        current_date=now.strftime("%d %B %Y"),
        current_day=current_day
    )

