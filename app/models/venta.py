from app import db
from datetime import datetime

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_venta = db.Column(db.String(20), unique=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    total = db.Column(db.Float, default=0.0)
    estado_pago = db.Column(db.String(20), default='pendiente')
    estado_entrega = db.Column(db.String(20), default='pendiente')
    notas = db.Column(db.Text)
    items = db.relationship('DetalleVenta', backref='venta', lazy=True)

    def generar_numero_venta(self):
        fecha = datetime.now().strftime('%Y%m%d')
        ultimo_numero = Venta.query.filter(
            Venta.numero_venta.like(f'{fecha}%')
        ).count()
        return f'{fecha}{str(ultimo_numero + 1).zfill(4)}'

class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cantidad = db.Column(db.Integer)
    precio_unitario = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    producto = db.relationship('Producto')