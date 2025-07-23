from flask import Blueprint, render_template, request, redirect
from models.kondisi_model import KondisiModel

kondisi_bp = Blueprint('kondisi_bp', __name__, url_prefix='/kondisi')


@kondisi_bp.route('/')
def index():
    data_kondisi = KondisiModel.get_all()
    return render_template('kondisi/index.html', data_kondisi=data_kondisi)


@kondisi_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        KondisiModel.insert(request.form['nama_kondisi'])
        return redirect('/kondisi')
    return render_template('kondisi/form.html', kondisi=None)


@kondisi_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    kondisi = KondisiModel.get_by_id(id)
    if request.method == 'POST':
        KondisiModel.update(id, request.form['nama_kondisi'])
        return redirect('/kondisi')
    return render_template('kondisi/form.html', kondisi=kondisi)


@kondisi_bp.route('/hapus/<int:id>')
def hapus(id):
    KondisiModel.delete(id)
    return redirect('/kondisi')
