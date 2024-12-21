import pytest
from app import create_app, db
from app.models import Usuario, Producto, Cliente
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database():
    # Crear usuario de prueba
    usuario = Usuario(username='test', email='test@example.com')
    usuario.set_password('test123')
    db.session.add(usuario)
    
    # Crear algunos productos de prueba
    productos = [
        Producto(codigo='P001', nombre='Producto 1', precio_venta=100, stock=10),
        Producto(codigo='P002', nombre='Producto 2', precio_venta=200, stock=20)
    ]
    db.session.add_all(productos)
    
    # Crear algunos clientes de prueba
    clientes = [
        Cliente(nombre='Cliente 1', email='cliente1@example.com'),
        Cliente(nombre='Cliente 2', email='cliente2@example.com')
    ]
    db.session.add_all(clientes)
    
    db.session.commit() 