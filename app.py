from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Producto, Cliente, Venta, DetalleVenta
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    ventas_recientes = Venta.query.order_by(Venta.fecha.desc()).limit(5).all()
    total_ventas_hoy = Venta.query.filter(db.func.date(Venta.fecha) == db.func.date(db.func.now())).count()
    total_productos = Producto.query.count()
    total_clientes = Cliente.query.count()
    ventas_pendientes = Venta.query.filter_by(estado_entrega='pendiente').count()
    
    return render_template('index.html',
                         ventas_recientes=ventas_recientes,
                         total_ventas_hoy=total_ventas_hoy,
                         total_productos=total_productos,
                         total_clientes=total_clientes,
                         ventas_pendientes=ventas_pendientes)

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    if request.method == 'POST':
        nuevo_producto = Producto(
            codigo=request.form['codigo'],
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            precio_costo=float(request.form['precio_costo']),
            precio_venta=float(request.form['precio_venta']),
            stock=int(request.form['stock'])
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('productos'))
    
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    if request.method == 'POST':
        # Lógica para crear nueva venta
        pass
    
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return render_template('ventas.html', 
                         ventas=ventas,
                         clientes=clientes,
                         productos=productos)

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        nuevo_cliente = Cliente(
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            direccion=request.form['direccion']
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return redirect(url_for('clientes'))
    
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

if __name__ == '__main__':
    app.run(debug=True) 