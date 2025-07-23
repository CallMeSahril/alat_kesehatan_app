from flask import Blueprint, render_template
from models.alat_model import Alat
from models.customer_model import Customer
from models.data_alat_model import DataAlat
from models.kondisi_model import Kondisi
from models.tahun_model import Tahun

main = Blueprint('main', __name__)


@main.route('/')
def index():
    alat = Alat.get_all()
    customer = Customer.get_all()
    data_alat = DataAlat.get_all()
    kondisi = Kondisi.get_all()
    tahun = Tahun.get_all()
    return render_template('index.html', alat=alat, customer=customer, data_alat=data_alat, kondisi=kondisi, tahun=tahun)
