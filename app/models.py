from app import db

class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_pregunta = db.Column(db.String(100))
    respuesta = db.Column(db.String(300))
