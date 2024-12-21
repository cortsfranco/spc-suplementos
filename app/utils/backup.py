import os
import json
from datetime import datetime
from app import db
from app.models import Producto, Cliente, Venta, DetalleVenta
from config import Config

def crear_backup():
    """Crea un backup de la base de datos en formato JSON"""
    datos = {
        'productos': [],
        'clientes': [],
        'ventas': [],
        'detalles_venta': []
    }
    
    # Respaldar productos
    productos = Producto.query.all()
    for p in productos:
        datos['productos'].append({
            'id': p.id,
            'codigo': p.codigo,
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'precio_costo': float(p.precio_costo),
            'precio_venta': float(p.precio_venta),
            'stock': p.stock,
            'stock_minimo': p.stock_minimo,
            'activo': p.activo
        })
    
    # Respaldar clientes
    clientes = Cliente.query.all()
    for c in clientes:
        datos['clientes'].append({
            'id': c.id,
            'nombre': c.nombre,
            'email': c.email,
            'telefono': c.telefono,
            'direccion': c.direccion,
            'activo': c.activo
        })
    
    # Respaldar ventas y sus detalles
    ventas = Venta.query.all()
    for v in ventas:
        datos['ventas'].append({
            'id': v.id,
            'numero_venta': v.numero_venta,
            'fecha': v.fecha.isoformat(),
            'cliente_id': v.cliente_id,
            'total': float(v.total),
            'estado_pago': v.estado_pago,
            'estado_entrega': v.estado_entrega,
            'notas': v.notas
        })
        
        for d in v.items:
            datos['detalles_venta'].append({
                'id': d.id,
                'venta_id': d.venta_id,
                'producto_id': d.producto_id,
                'cantidad': d.cantidad,
                'precio_unitario': float(d.precio_unitario),
                'subtotal': float(d.subtotal)
            })
    
    # Crear directorio de backups si no existe
    if not os.path.exists(Config.BACKUP_FOLDER):
        os.makedirs(Config.BACKUP_FOLDER)
    
    # Guardar archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'backup_{timestamp}.json'
    filepath = os.path.join(Config.BACKUP_FOLDER, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
    
    return filename

def restaurar_backup(filename):
    """Restaura la base de datos desde un archivo de backup"""
    filepath = os.path.join(Config.BACKUP_FOLDER, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError('Archivo de backup no encontrado')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    try:
        # Limpiar tablas existentes
        DetalleVenta.query.delete()
        Venta.query.delete()
        Cliente.query.delete()
        Producto.query.delete()
        
        # Restaurar productos
        for p in datos['productos']:
            producto = Producto(
                id=p['id'],
                codigo=p['codigo'],
                nombre=p['nombre'],
                descripcion=p['descripcion'],
                precio_costo=p['precio_costo'],
                precio_venta=p['precio_venta'],
                stock=p['stock'],
                stock_minimo=p['stock_minimo'],
                activo=p['activo']
            )
            db.session.add(producto)
        
        # Restaurar clientes
        for c in datos['clientes']:
            cliente = Cliente(
                id=c['id'],
                nombre=c['nombre'],
                email=c['email'],
                telefono=c['telefono'],
                direccion=c['direccion'],
                activo=c['activo']
            )
            db.session.add(cliente)
        
        db.session.commit()
        
        # Restaurar ventas y detalles
        for v in datos['ventas']:
            venta = Venta(
                id=v['id'],
                numero_venta=v['numero_venta'],
                fecha=datetime.fromisoformat(v['fecha']),
                cliente_id=v['cliente_id'],
                total=v['total'],
                estado_pago=v['estado_pago'],
                estado_entrega=v['estado_entrega'],
                notas=v['notas']
            )
            db.session.add(venta)
        
        db.session.commit()
        
        for d in datos['detalles_venta']:
            detalle = DetalleVenta(
                id=d['id'],
                venta_id=d['venta_id'],
                producto_id=d['producto_id'],
                cantidad=d['cantidad'],
                precio_unitario=d['precio_unitario'],
                subtotal=d['subtotal']
            )
            db.session.add(detalle)
        
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        raise e 