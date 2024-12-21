import re
from wtforms.validators import ValidationError

def validar_telefono(form, field):
    """Valida que el teléfono tenga un formato válido"""
    if field.data:
        patron = re.compile(r'^\+?[\d\s-]{10,}$')
        if not patron.match(field.data):
            raise ValidationError('Formato de teléfono inválido')

def validar_codigo_producto(form, field):
    """Valida que el código del producto sea único y tenga el formato correcto"""
    from app.models import Producto
    
    if not re.match(r'^[A-Z0-9]{3,10}$', field.data):
        raise ValidationError('El código debe tener entre 3 y 10 caracteres alfanuméricos')
    
    producto = Producto.query.filter_by(codigo=field.data).first()
    if producto and producto.id != getattr(form, 'id', None):
        raise ValidationError('Este código ya está en uso')

def validar_stock_minimo(form, field):
    """Valida que el stock mínimo sea menor que el stock actual"""
    if field.data > form.stock.data:
        raise ValidationError('El stock mínimo no puede ser mayor que el stock actual') 