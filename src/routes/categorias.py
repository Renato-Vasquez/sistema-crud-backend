from flask import Blueprint, jsonify, request
from extensions import mysql

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('/', methods=['GET'])
def listar_categorias():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion FROM categorias")
    datos = cursor.fetchall()

    categorias = []
    for fila in datos:
        categorias.append({
            "id": fila[0],
            "nombre": fila[1],
            "descripcion": fila[2]
        })

    return jsonify(categorias)


@categorias_bp.route('/', methods=['POST'])
def crear_categoria():
    data = request.json
    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO categorias (nombre, descripcion)
        VALUES (%s, %s)
    """, (data['nombre'], data.get('descripcion', '')))

    mysql.connection.commit()

    return jsonify({"mensaje": "Categoria creada"}), 201