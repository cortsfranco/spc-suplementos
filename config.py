import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('f1e44df99a36d851ffca0eaf85406c33') or 'dev-key-temporal'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://spc_imby_user:NqlUODe7jfa9TeT988cO0CI1tLt90RIz@dpg-ctjgkb52ng1s73bjimtg-a/spc_imby'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de correo
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configuración de la aplicación
    ITEMS_PER_PAGE = 10
    BACKUP_FOLDER = os.path.join(basedir, 'backups')
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit 