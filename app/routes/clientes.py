from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.cliente import Cliente
from app import db

bp = Blueprint('clientes', __name__)

@bp.route('/clientes')
def index():
    clientes = Cliente.query.filter_by(activo=True).all()
    return render_template('clientes/index.html', clientes=clientes)

@bp.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.form['nombre'],
            email=request.form['email'],
            telefono=request.form['telefono'],
            direccion=request.form['direccion']
        )
        try:
            db.session.add(cliente)
            db.session.commit()
            flash('Cliente agregado exitosamente', 'success')
            return redirect(url_for('clientes.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar el cliente', 'danger')
    
    return render_template('clientes/nuevo.html')

@bp.route('/clientes/<int:id>/historial')
def historial(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('clientes/historial.html', cliente=cliente)