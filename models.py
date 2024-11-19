from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categorias'  # Nombre de la tabla en tu base de datos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    
    supercat = db.Column(db.String(250), nullable=True)  # Campo supercat
    superest = db.Column(db.String(250), nullable=True)  # Campo superest

    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer, nullable=False)
    producto = db.Column(db.Integer, nullable=False)
    detalle = db.Column(db.String(250), nullable=True)
    imagen = db.Column(db.String(250), nullable=True)
    img1 = db.Column(db.String(250), nullable=True)
    img2 = db.Column(db.String(250), nullable=True)
    img3 = db.Column(db.String(250), nullable=True)
    categoria = db.Column(db.Integer, nullable=True)
    stock = db.Column(db.Numeric(10), nullable=True)    
    costo = db.Column(db.Numeric(10), nullable=True)
    por1 = db.Column(db.Numeric(10), nullable=True)
    precio1 = db.Column(db.Numeric(10), nullable=True)
    por2 = db.Column(db.Numeric(10), nullable=True)
    precio2 = db.Column(db.Numeric(10), nullable=True)
    
    # Agrega otros campos según tu estructura
