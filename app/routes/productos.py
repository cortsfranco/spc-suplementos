from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.models.producto import Producto
from app import db

bp = Blueprint('productos', __name__)

@bp.route('/productos')
def index():
    productos = Producto.query.filter_by(activo=True).all()
    return render_template('productos/index.html', productos=productos)

@bp.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        producto = Producto(
            codigo=request.form['codigo'],
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            precio_costo=float(request.form['precio_costo']),
            precio_venta=float(request.form['precio_venta']),
            stock=int(request.form['stock']),
            stock_minimo=int(request.form['stock_minimo'])
        )
        db.session.add(producto)
        try:
            db.session.commit()
            flash('Producto agregado exitosamente', 'success')
            return redirect(url_for('productos.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar el producto', 'danger')
    
    return render_template('productos/nuevo.html')

@bp.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.codigo = request.form['codigo']
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio_costo = float(request.form['precio_costo'])
        producto.precio_venta = float(request.form['precio_venta'])
        producto.stock = int(request.form['stock'])
        producto.stock_minimo = int(request.form['stock_minimo'])
        
        try:
            db.session.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('productos.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el producto', 'danger')
    
    return render_template('productos/editar.html', producto=producto)

@bp.route('/productos/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    producto = Producto.query.get_or_404(id)
    producto.activo = False
    try:
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el producto', 'danger')
    return redirect(url_for('productos.index'))