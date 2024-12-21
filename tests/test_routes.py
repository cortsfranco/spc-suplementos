from flask import url_for
from app.models import Usuario, Producto

def test_login(client):
    response = client.post(url_for('auth.login'), data={
        'username': 'test',
        'password': 'test123'
    })
    assert response.status_code == 302

def test_productos_lista(client, init_database):
    # Primero hacer login
    client.post(url_for('auth.login'), data={
        'username': 'test',
        'password': 'test123'
    })
    
    response = client.get(url_for('productos.index'))
    assert response.status_code == 200
    assert b'Producto 1' in response.data

def test_nuevo_producto(client, init_database):
    # Primero hacer login
    client.post(url_for('auth.login'), data={
        'username': 'test',
        'password': 'test123'
    })
    
    response = client.post(url_for('productos.nuevo'), data={
        'codigo': 'P003',
        'nombre': 'Producto 3',
        'precio_costo': 100,
        'precio_venta': 150,
        'stock': 10
    })
    assert response.status_code == 302
    assert Producto.query.filter_by(codigo='P003').first() is not None 