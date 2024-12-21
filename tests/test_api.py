import json
import pytest
from base64 import b64encode
from app import create_app, db
from app.models import Usuario, Producto

def get_auth_headers(client, username, password):
    """Helper para obtener headers de autenticación"""
    credentials = b64encode(f"{username}:{password}".encode()).decode('utf-8')
    response = client.post('/api/token', headers={
        'Authorization': f'Basic {credentials}'
    })
    token = json.loads(response.data)['token']
    return {'Authorization': f'Bearer {token}'}

class TestAPI:
    def setup_method(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Crear usuario de prueba
        user = Usuario(username='test', email='test@example.com')
        user.set_password('test123')
        db.session.add(user)
        db.session.commit()
        
        self.auth_headers = get_auth_headers(self.client, 'test', 'test123')

    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_productos(self):
        # Crear producto de prueba
        producto = Producto(
            codigo='TEST1',
            nombre='Producto Test',
            precio_venta=100
        )
        db.session.add(producto)
        db.session.commit()

        response = self.client.get('/api/productos', 
                                 headers=self.auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['codigo'] == 'TEST1'

    def test_crear_producto(self):
        producto_data = {
            'codigo': 'TEST2',
            'nombre': 'Nuevo Producto',
            'precio_venta': 200
        }
        
        response = self.client.post('/api/productos',
                                  headers=self.auth_headers,
                                  json=producto_data)
        assert response.status_code == 201
        
        producto = Producto.query.filter_by(codigo='TEST2').first()
        assert producto is not None
        assert producto.nombre == 'Nuevo Producto'

    def test_actualizar_producto(self):
        # Crear producto
        producto = Producto(
            codigo='TEST3',
            nombre='Producto Original',
            precio_venta=300
        )
        db.session.add(producto)
        db.session.commit()

        # Actualizar producto
        update_data = {'nombre': 'Producto Actualizado'}
        response = self.client.put(f'/api/productos/{producto.id}',
                                 headers=self.auth_headers,
                                 json=update_data)
        assert response.status_code == 200
        
        producto = Producto.query.get(producto.id)
        assert producto.nombre == 'Producto Actualizado' 