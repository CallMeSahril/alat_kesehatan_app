from flask import Blueprint, render_template, request, redirect
from models.tahun_model import TahunModel

tahun_bp = Blueprint('tahun_bp', __name__, url_prefix='/tahun')


@tahun_bp.route('/')
def index():
    data_tahun = TahunModel.get_all()
    return render_template('tahun/index.html', data_tahun=data_tahun)


@tahun_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        TahunModel.insert(request.form['tahun'])
        return redirect('/tahun')
    return render_template('tahun/form.html', tahun=None)


@tahun_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    tahun = TahunModel.get_by_id(id)
    if request.method == 'POST':
        TahunModel.update(id, request.form['tahun'])
        return redirect('/tahun')
    return render_template('tahun/form.html', tahun=tahun)


@tahun_bp.route('/hapus/<int:id>')
def hapus(id):
    TahunModel.delete(id)
    return redirect('/tahun')
