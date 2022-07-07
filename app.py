from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:amaro2211@127.0.0.1:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Persona(db.Model):
    __tablename__ = 'contactos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db. Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Persona %r>" % self.nombre

@cross_origin()
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hola Mundo"})


@cross_origin()
@app.route('/persona', methods=['POST'])
def crear_persona():
    persona_data = request.json
    nombre = persona_data['nombre']
    apellido = persona_data['apellido']
    persona = Persona(nombre=nombre, apellido=apellido)
    db.session.add(persona)
    db.session.commit()
    return jsonify({"success": True, "response": "Persona agregada"})


@cross_origin()
@app.route('/listar', methods=['GET'])
def getpersonas():
    lista_personas = []
    personas = Persona.query.all()
    for persona in personas:
        resultado = {
            "id": persona.id,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
        }
        lista_personas.append(resultado)

    return jsonify(
        {
            "success": True,
            "personas": lista_personas,
            "total personas": len(lista_personas),
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
