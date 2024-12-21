from app import db

class Configuracion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(200))
    descripcion = db.Column(db.String(200))
    tipo = db.Column(db.String(20))  # texto, numero, booleano
    
    @classmethod
    def get_valor(cls, clave, default=None):
        config = cls.query.filter_by(clave=clave).first()
        return config.valor if config else default

    @classmethod
    def set_valor(cls, clave, valor, descripcion=None, tipo='texto'):
        config = cls.query.filter_by(clave=clave).first()
        if config:
            config.valor = valor
        else:
            config = cls(clave=clave, valor=valor, descripcion=descripcion, tipo=tipo)
            db.session.add(config)
        db.session.commit() 