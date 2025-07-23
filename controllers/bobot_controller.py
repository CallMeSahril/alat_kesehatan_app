from flask import Blueprint, render_template, request, redirect
from models.kriteria_model import KriteriaModel
from models.matriks_kriteria_model import MatriksKriteriaModel

bobot_bp = Blueprint('bobot_bp', __name__, url_prefix='/bobot')


@bobot_bp.route('/', methods=['GET', 'POST'])
def index():
    kriteria_list = KriteriaModel.get_all()

    if request.method == 'POST':
        MatriksKriteriaModel.delete_all()

        for i in range(len(kriteria_list)):
            for j in range(len(kriteria_list)):
                if i <= j:
                    nilai = float(request.form.get(f'nilai_{i}_{j}', 1))
                    MatriksKriteriaModel.insert(
                        kriteria_list[i]['id_kriteria'],
                        kriteria_list[j]['id_kriteria'],
                        nilai
                    )
                    if i != j:
                        MatriksKriteriaModel.insert(
                            kriteria_list[j]['id_kriteria'],
                            kriteria_list[i]['id_kriteria'],
                            round(1 / nilai, 5)
                        )

        return redirect('/bobot')

    matriks = MatriksKriteriaModel.get_all()
    return render_template('bobot/index.html', kriteria_list=kriteria_list, matriks=matriks)
