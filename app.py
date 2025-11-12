from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de ejemplo: Libros
class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "autor": self.autor}

@app.route('/')
def index():
    with open('static/index.html', 'r') as f:
        return f.read()

@app.route('/api/libros', methods=['GET'])
def get_libros():
    libros = Libro.query.all()
    return jsonify([libro.to_dict() for libro in libros])

@app.route('/api/libros/<int:id>', methods=['GET'])
def get_libro(id):
    libro = Libro.query.get_or_404(id)
    return jsonify(libro.to_dict())

@app.route('/api/libros', methods=['POST'])
def add_libro():
    data = request.get_json()
    libro = Libro(titulo=data['titulo'], autor=data['autor'])
    db.session.add(libro)
    db.session.commit()
    return jsonify(libro.to_dict()), 201

@app.route('/api/libros/<int:id>', methods=['PUT'])
def update_libro(id):
    libro = Libro.query.get_or_404(id)
    data = request.get_json()
    libro.titulo = data['titulo']
    libro.autor = data['autor']
    db.session.commit()
    return jsonify(libro.to_dict())

@app.route('/api/libros/<int:id>', methods=['DELETE'])
def delete_libro(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return '', 204

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
