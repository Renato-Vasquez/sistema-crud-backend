from flask import Blueprint, jsonify, request
from extensions import mysql
from werkzeug.security import generate_password_hash

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# ===============================
# GET - Listar todos
# ===============================
@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, email, activo FROM usuarios")
    datos = cursor.fetchall()

    usuarios = []
    for fila in datos:
        usuarios.append({
            "id": fila[0],
            "nombre": fila[1],
            "email": fila[2],
            "activo": fila[3]
        })

    return jsonify(usuarios)


# ===============================
# GET - Obtener uno por ID
# ===============================
@usuarios_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, email, activo FROM usuarios WHERE id = %s", (id,))
    dato = cursor.fetchone()

    if dato:
        usuario = {
            "id": dato[0],
            "nombre": dato[1],
            "email": dato[2],
            "activo": dato[3]
        }
        return jsonify(usuario)
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404


# ===============================
# POST - Crear usuario
# ===============================
@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.json
    cursor = mysql.connection.cursor()
    hashed_password = generate_password_hash(data['password'])

    cursor.execute("""
    INSERT INTO usuarios (nombre, email, password)
    VALUES (%s, %s, %s)
""", (
    data['nombre'],
    data['email'],
    hashed_password
))
    mysql.connection.commit()

    return jsonify({"mensaje": "Usuario creado correctamente"}), 201


# ===============================
# PUT - Actualizar usuario
# ===============================
@usuarios_bp.route('/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.json
    cursor = mysql.connection.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nombre = %s,
            email = %s,
            activo = %s
        WHERE id = %s
    """, (data['nombre'], data['email'], data['activo'], id))

    mysql.connection.commit()

    if cursor.rowcount == 0:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario actualizado correctamente"})


# ===============================
# DELETE - Eliminar usuario
# ===============================
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    mysql.connection.commit()

    if cursor.rowcount == 0:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario eliminado correctamente"})