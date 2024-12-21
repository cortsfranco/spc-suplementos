from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f'Error enviando email: {str(e)}')

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # Enviar email de forma asíncrona
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_stock_alert(producto):
    """Envía alerta por email cuando un producto tiene stock bajo"""
    send_email(
        subject='Alerta de Stock Bajo',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[current_app.config['ADMIN_EMAIL']],
        text_body=render_template('email/stock_alert.txt',
                                producto=producto),
        html_body=render_template('email/stock_alert.html',
                                producto=producto)
    )

def send_daily_report(ventas_dia, productos_bajos):
    """Envía reporte diario de ventas y stock"""
    send_email(
        subject='Reporte Diario - SPC Suplementos',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[current_app.config['ADMIN_EMAIL']],
        text_body=render_template('email/daily_report.txt',
                                ventas=ventas_dia,
                                productos=productos_bajos),
        html_body=render_template('email/daily_report.html',
                                ventas=ventas_dia,
                                productos=productos_bajos)
    ) 