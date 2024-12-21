import pytest
from app.models import Usuario, Producto, Cliente, Venta
from datetime import datetime

def test_usuario_password_hashing():
    u = Usuario(username='test')
    u.set_password('cat')
    assert not u.check_password('dog')
    assert u.check_password('cat')

def test_producto_precio_venta():
    p = Producto(precio_costo=100)
    p.set_precio_venta(50)  # 50% de ganancia
    assert p.precio_venta == 150
    assert p.ganancia == 50

def test_cliente_total_compras(init_database):
    cliente = Cliente.query.first()
    
    # Crear algunas ventas para el cliente
    venta1 = Venta(cliente=cliente, total=100)
    venta2 = Venta(cliente=cliente, total=200)
    db.session.add_all([venta1, venta2])
    db.session.commit()
    
    assert cliente.total_compras() == 300

def test_venta_calculo_total():
    venta = Venta()
    producto1 = Producto(precio_venta=100)
    producto2 = Producto(precio_venta=200)
    
    venta.agregar_item(producto1, 2)
    venta.agregar_item(producto2, 1)
    
    assert venta.total == 400 