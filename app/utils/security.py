from functools import wraps
from flask import abort, request, current_app
import hashlib
import hmac
import ipaddress
from datetime import datetime, timedelta
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)

def check_rate_limit(ip, limit=100, period=3600):
    """
    Implementa rate limiting por IP
    """
    key = f'rate_limit:{ip}'
    current = redis_client.get(key)
    
    if current is None:
        redis_client.setex(key, period, 1)
        return True
    
    if int(current) >= limit:
        return False
        
    redis_client.incr(key)
    return True

def verify_webhook_signature(secret):
    """
    Verifica la firma de webhooks
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            signature = request.headers.get('X-Hub-Signature')
            if not signature:
                abort(403)
            
            payload = request.get_data()
            expected_signature = hmac.new(
                secret.encode('utf-8'),
                payload,
                hashlib.sha1
            ).hexdigest()
            
            if not hmac.compare_digest(f'sha1={expected_signature}', signature):
                abort(403)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_ip_whitelist(whitelist):
    """
    Valida IPs contra una whitelist
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            allowed = False
            
            for allowed_ip in whitelist:
                if ipaddress.ip_address(ip) in ipaddress.ip_network(allowed_ip):
                    allowed = True
                    break
                    
            if not allowed:
                abort(403)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_2fa(f):
    """
    Requiere autenticación de dos factores
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
            
        if not current_user.has_2fa_enabled:
            return redirect(url_for('auth.setup_2fa'))
            
        if not session.get('2fa_validated'):
            return redirect(url_for('auth.validate_2fa'))
            
        return f(*args, **kwargs)
    return decorated_function 