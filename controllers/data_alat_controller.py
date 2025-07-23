from flask import Blueprint, render_template, request, redirect
from models.data_alat_model import DataAlatModel
from models.customer_model import CustomerModel
from models.alat_model import AlatModel
from models.kondisi_model import KondisiModel
from datetime import datetime
from dateutil.relativedelta import relativedelta

data_alat_bp = Blueprint('data_alat_bp', __name__, url_prefix='/data-alat')


@data_alat_bp.route('/')
def index():
    data = DataAlatModel.get_all()
    print(data)
    return render_template('data_alat/index.html', data_alat=data)


@data_alat_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    customers = CustomerModel.get_all()
    alats = AlatModel.get_all()
    kondisi = KondisiModel.get_all()

    data = None

    if request.method == 'POST':
        id_alat = request.form['id_alat']
        # Tidak pakai id_tahun lagi
        garansi = int(request.form['garansi_tahun'])
        tgl_instalasi = datetime.strptime(
            request.form['tgl_instalasi'], '%Y-%m-%d')
        jumlah_maintenance = garansi * 2

        m = []
        for i in range(1, 11):
            if i <= jumlah_maintenance:
                m.append(
                    (tgl_instalasi + relativedelta(months=6 * i)).strftime('%Y-%m'))
            else:
                m.append('')

        data = {
            'id_customer': request.form['id_customer'],
            'id_alat': id_alat,
            'garansi_tahun': garansi,
            'tgl_instalasi': tgl_instalasi.strftime('%Y-%m-%d'),
            'jumlah_maintenance': jumlah_maintenance,
            'm1': m[0], 'm2': m[1], 'm3': m[2], 'm4': m[3], 'm5': m[4],
            'm6': m[5], 'm7': m[6], 'm8': m[7], 'm9': m[8], 'm10': m[9],
            'id_kondisi': request.form['id_kondisi']
        }

        DataAlatModel.insert(data)
        return redirect('/data-alat')

    return render_template(
        'data_alat/form.html',
        data_alat=data,
        customers=customers,
        alats=alats,
        kondisi=kondisi
    )


@data_alat_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    data = DataAlatModel.get_by_id(id)
    if not data:
        return "Data tidak ditemukan", 404

    customers = CustomerModel.get_all()
    alats = AlatModel.get_all()
    kondisi = KondisiModel.get_all()

    if request.method == 'POST':
        id_alat = request.form['id_alat']
        # Tidak pakai id_tahun lagi
        garansi = int(request.form['garansi_tahun'])
        tgl_instalasi = datetime.strptime(
            request.form['tgl_instalasi'], '%Y-%m-%d')
        jumlah_maintenance = garansi * 2

        m = []
        for i in range(1, 11):
            if i <= jumlah_maintenance:
                m.append(
                    (tgl_instalasi + relativedelta(months=6 * i)).strftime('%Y-%m'))
            else:
                m.append('')

        data_update = {
            'id_customer': request.form['id_customer'],
            'id_alat': id_alat,
            'garansi_tahun': garansi,
            'tgl_instalasi': tgl_instalasi.strftime('%Y-%m-%d'),
            'jumlah_maintenance': jumlah_maintenance,
            'm1': m[0], 'm2': m[1], 'm3': m[2], 'm4': m[3], 'm5': m[4],
            'm6': m[5], 'm7': m[6], 'm8': m[7], 'm9': m[8], 'm10': m[9],
            'id_kondisi': request.form['id_kondisi']
        }

        DataAlatModel.update(id, data_update)
        return redirect('/data-alat')

    return render_template(
        'data_alat/form.html',
        data_alat=data,
        customers=customers,
        alats=alats,
        kondisi=kondisi
    )


@data_alat_bp.route('/hapus/<int:id>')
def hapus(id):
    if not DataAlatModel.get_by_id(id):
        return "Data tidak ditemukan", 404

    DataAlatModel.delete(id)
    return redirect('/data-alat')
