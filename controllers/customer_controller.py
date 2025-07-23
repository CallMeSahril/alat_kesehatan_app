from flask import Blueprint, render_template, request, redirect
from models.customer_model import CustomerModel

customer_bp = Blueprint('customer_bp', __name__, url_prefix='/customer')

@customer_bp.route('/')
def index():
    data_customer = CustomerModel.get_all()
    return render_template('customer/index.html', data_customer=data_customer)

@customer_bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        CustomerModel.insert(request.form['nama_customer'], request.form['alamat'])
        return redirect('/customer')
    return render_template('customer/form.html', customer=None)

@customer_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    customer = CustomerModel.get_by_id(id)
    if request.method == 'POST':
        CustomerModel.update(id, request.form['nama_customer'], request.form['alamat'])
        return redirect('/customer')
    return render_template('customer/form.html', customer=customer)

@customer_bp.route('/hapus/<int:id>')
def hapus(id):
    CustomerModel.delete(id)
    return redirect('/customer')
