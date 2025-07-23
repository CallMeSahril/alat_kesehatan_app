from flask import Blueprint, render_template, request, redirect
from models.alat_model import AlatModel
from models.tahun_model import TahunModel  # tambahkan ini

alat_bp = Blueprint('alat_bp', __name__, url_prefix='/alat')


@alat_bp.route('/')
def index():
    data_alat = AlatModel.get_all()
    return render_template('alat/index.html', data_alat=data_alat)


@alat_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    tahun_list = TahunModel.get_all()  # ambil data tahun untuk dropdown
    if request.method == 'POST':
        AlatModel.insert(
            request.form['nama_alat'],
            request.form['merk'],
            request.form['tahun_produksi']
        )
        return redirect('/alat')
    return render_template('alat/form.html', alat=None, tahun_list=tahun_list)


@alat_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    alat = AlatModel.get_by_id(id)
    tahun_list = TahunModel.get_all()  # ambil data tahun juga saat edit
    if request.method == 'POST':
        AlatModel.update(
            id,
            request.form['nama_alat'],
            request.form['merk'],
            request.form['tahun_produksi']
        )
        return redirect('/alat')
    return render_template('alat/form.html', alat=alat, tahun_list=tahun_list)


@alat_bp.route('/hapus/<int:id>')
def hapus(id):
    AlatModel.delete(id)
    return redirect('/alat')
