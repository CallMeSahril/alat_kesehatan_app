from flask import Blueprint, render_template, request, redirect
from models.kriteria_model import KriteriaModel

kriteria_bp = Blueprint('kriteria_bp', __name__, url_prefix='/kriteria')


@kriteria_bp.route('/')
def index():
    data_kriteria = KriteriaModel.get_all()
    return render_template('kriteria/index.html', data_kriteria=data_kriteria)


@kriteria_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        KriteriaModel.insert(request.form['nama_kriteria'])
        return redirect('/kriteria')
    return render_template('kriteria/form.html', kriteria=None)


@kriteria_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    kriteria = KriteriaModel.get_by_id(id)
    if request.method == 'POST':
        KriteriaModel.update(id, request.form['nama_kriteria'])
        return redirect('/kriteria')
    return render_template('kriteria/form.html', kriteria=kriteria)


@kriteria_bp.route('/hapus/<int:id>')
def hapus(id):
    KriteriaModel.delete(id)
    return redirect('/kriteria')
