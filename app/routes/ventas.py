from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.venta import Venta, DetalleVenta
from app.models.producto import Producto
from app.models.cliente import Cliente
from app import db
from datetime import datetime

bp = Blueprint('ventas', __name__)

@bp.route('/ventas')
def index():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template('ventas/index.html', ventas=ventas)

@bp.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        try:
            venta = Venta(
                cliente_id=request.form['cliente_id'],
                fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d'),
                estado_pago=request.form['estado_pago'],
                estado_entrega=request.form['estado_entrega'],
                notas=request.form['notas']
            )
            venta.numero_venta = venta.generar_numero_venta()
            
            # Procesar items de la venta
            productos = request.form.getlist('producto_id[]')
            cantidades = request.form.getlist('cantidad[]')
            
            total = 0
            for prod_id, cant in zip(productos, cantidades):
                producto = Producto.query.get(prod_id)
                cantidad = int(cant)
                
                if producto.stock < cantidad:
                    flash(f'Stock insuficiente para {producto.nombre}', 'danger')
                    return redirect(url_for('ventas.nueva'))
                
                detalle = DetalleVenta(
                    producto_id=prod_id,
                    cantidad=cantidad,
                    precio_unitario=producto.precio_venta,
                    subtotal=producto.precio_venta * cantidad
                )
                
                producto.stock -= cantidad
                total += detalle.subtotal
                venta.items.append(detalle)
            
            venta.total = total
            db.session.add(venta)
            db.session.commit()
            
            flash('Venta registrada exitosamente', 'success')
            return redirect(url_for('ventas.index'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar la venta', 'danger')
    
    clientes = Cliente.query.filter_by(activo=True).all()
    productos = Producto.query.filter_by(activo=True).all()
    return render_template('ventas/nueva.html', clientes=clientes, productos=productos)