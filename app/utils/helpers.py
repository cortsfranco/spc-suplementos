from datetime import datetime, timedelta
from calendar import monthrange
import locale

# Configurar locale para formato de moneda
locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')

def formato_moneda(valor):
    """Formatea un número como moneda argentina"""
    return locale.currency(valor, grouping=True, symbol=True)

def get_rango_fechas(tipo='mes'):
    """Obtiene un rango de fechas según el tipo especificado"""
    hoy = datetime.now()
    
    if tipo == 'hoy':
        inicio = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = hoy.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    elif tipo == 'semana':
        inicio = hoy - timedelta(days=hoy.weekday())
        fin = inicio + timedelta(days=6)
        inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        fin = fin.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    elif tipo == 'mes':
        inicio = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        ultimo_dia = monthrange(hoy.year, hoy.month)[1]
        fin = hoy.replace(day=ultimo_dia, hour=23, minute=59, second=59, microsecond=999999)
    
    else:  # año
        inicio = hoy.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        fin = hoy.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    
    return inicio, fin

def generar_numero_venta():
    """Genera un número de venta único"""
    from app.models import Venta
    fecha = datetime.now().strftime('%Y%m%d')
    ultimo_numero = Venta.query.filter(
        Venta.numero_venta.like(f'{fecha}%')
    ).count()
    return f'{fecha}{str(ultimo_numero + 1).zfill(4)}'

def calcular_estadisticas_ventas(ventas):
    """Calcula estadísticas básicas de un conjunto de ventas"""
    total_ventas = sum(v.total for v in ventas)
    cantidad_ventas = len(ventas)
    ticket_promedio = total_ventas / cantidad_ventas if cantidad_ventas > 0 else 0
    
    productos_vendidos = {}
    for venta in ventas:
        for detalle in venta.items:
            if detalle.producto_id in productos_vendidos:
                productos_vendidos[detalle.producto_id]['cantidad'] += detalle.cantidad
                productos_vendidos[detalle.producto_id]['total'] += detalle.subtotal
            else:
                productos_vendidos[detalle.producto_id] = {
                    'cantidad': detalle.cantidad,
                    'total': detalle.subtotal,
                    'nombre': detalle.producto.nombre
                }
    
    return {
        'total_ventas': total_ventas,
        'cantidad_ventas': cantidad_ventas,
        'ticket_promedio': ticket_promedio,
        'productos_vendidos': productos_vendidos
    } 