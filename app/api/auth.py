from functools import wraps
from flask import request, jsonify
import jwt
from app import app
from app.models import Usuario

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token inválido'}), 401

        if not token:
            return jsonify({'message': 'Token faltante'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Usuario.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorated

@app.route('/api/token', methods=['POST'])
def get_token():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'No se pudo verificar'}), 401

    user = Usuario.query.filter_by(username=auth.username).first()
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 401
        
    if user.check_password(auth.password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        
        return jsonify({'token': token})

    return jsonify({'message': 'No se pudo verificar'}), 401 