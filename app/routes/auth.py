from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario
from app import db
from werkzeug.urls import url_parse
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login'))
            
        if not user.activo:
            flash('Esta cuenta está desactivada', 'danger')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=request.form.get('remember', False))
        user.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
        
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        current_user.nombre = request.form['nombre']
        current_user.email = request.form['email']
        
        if request.form.get('password'):
            if not current_user.check_password(request.form['password_actual']):
                flash('Contraseña actual incorrecta', 'danger')
                return redirect(url_for('auth.perfil'))
            current_user.set_password(request.form['password'])
            
        try:
            db.session.commit()
            flash('Perfil actualizado exitosamente', 'success')
        except:
            db.session.rollback()
            flash('Error al actualizar el perfil', 'danger')
            
    return render_template('auth/perfil.html') 