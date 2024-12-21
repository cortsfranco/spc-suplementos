from app import create_app, db
from app.models import Producto, Venta
from app.utils.email import send_daily_report
from datetime import datetime, timedelta
import schedule
import time

app = create_app()

def check_stock_levels():
    """Verifica niveles de stock y envía alertas si es necesario"""
    with app.app_context():
        productos_bajos = Producto.query.filter(
            Producto.stock <= Producto.stock_minimo
        ).all()
        
        if productos_bajos:
            for producto in productos_bajos:
                send_stock_alert(producto)

def generate_daily_report():
    """Genera y envía el reporte diario"""
    with app.app_context():
        # Obtener ventas del día
        hoy = datetime.now().date()
        ventas_dia = Venta.query.filter(
            db.func.date(Venta.fecha) == hoy
        ).all()
        
        # Obtener productos con stock bajo
        productos_bajos = Producto.query.filter(
            Producto.stock <= Producto.stock_minimo
        ).all()
        
        # Enviar reporte
        send_daily_report(ventas_dia, productos_bajos)

def run_scheduler():
    # Programar tareas
    schedule.every().day.at("09:00").do(check_stock_levels)
    schedule.every().day.at("20:00").do(generate_daily_report)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler() 