from flask import Blueprint, jsonify, request
from extensions import mysql

tareas_bp = Blueprint('tareas', __name__)

# =========================
# GET - Listar tareas
# =========================
@tareas_bp.route('/tareas', methods=['GET'])
def listar_tareas():
    try:
        cursor = mysql.connection.cursor()
        sql = """
        SELECT t.id, t.titulo, t.descripcion, t.estado, u.nombre
        FROM tareas t
        LEFT JOIN usuarios u ON t.usuario_id = u.id
        """
        cursor.execute(sql)
        datos = cursor.fetchall()

        tareas = []
        for fila in datos:
            tarea = {
                'id': fila[0],
                'titulo': fila[1],
                'descripcion': fila[2],
                'estado': fila[3],
                'usuario': fila[4]
            }
            tareas.append(tarea)

        return jsonify({'tareas': tareas})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al listar tareas'}), 500


# =========================
# GET - Una tarea
# =========================
@tareas_bp.route('/tareas/<int:id>', methods=['GET'])
def obtener_tarea(id):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT id, titulo, descripcion, estado, usuario_id FROM tareas WHERE id = %s"
        cursor.execute(sql, (id,))
        dato = cursor.fetchone()

        if dato:
            tarea = {
                'id': dato[0],
                'titulo': dato[1],
                'descripcion': dato[2],
                'estado': dato[3],
                'usuario_id': dato[4]
            }
            return jsonify(tarea)
        else:
            return jsonify({'mensaje': 'Tarea no encontrada'}), 404

    except Exception as ex:
        return jsonify({'mensaje': 'Error'}), 500


# =========================
# POST - Crear tarea
# =========================
@tareas_bp.route('/tareas', methods=['POST'])
def crear_tarea():
    try:
        cursor = mysql.connection.cursor()
        sql = """
        INSERT INTO tareas (titulo, descripcion, estado, usuario_id)
        VALUES (%s, %s, %s, %s)
        """
        data = request.json
        cursor.execute(sql, (
            data['titulo'],
            data.get('descripcion'),
            data.get('estado', 'pendiente'),
            data['usuario_id']
        ))
        mysql.connection.commit()

        return jsonify({'mensaje': 'Tarea creada correctamente'}), 201

    except Exception as ex:
        return jsonify({'mensaje': 'Error al crear tarea'}), 500


# =========================
# PUT - Actualizar tarea
# =========================
@tareas_bp.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    try:
        cursor = mysql.connection.cursor()
        sql = """
        UPDATE tareas
        SET titulo=%s, descripcion=%s, estado=%s, usuario_id=%s
        WHERE id=%s
        """
        data = request.json
        cursor.execute(sql, (
            data['titulo'],
            data.get('descripcion'),
            data['estado'],
            data['usuario_id'],
            id
        ))
        mysql.connection.commit()

        return jsonify({'mensaje': 'Tarea actualizada correctamente'})

    except Exception as ex:
        return jsonify({'mensaje': 'Error al actualizar tarea'}), 500


# =========================
# DELETE - Eliminar tarea
# =========================
@tareas_bp.route('/tareas/<int:id>', methods=['DELETE'])
def eliminar_tarea(id):
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM tareas WHERE id = %s"
        cursor.execute(sql, (id,))
        mysql.connection.commit()

        return jsonify({'mensaje': 'Tarea eliminada correctamente'})

    except Exception as ex:
        return jsonify({'mensaje': 'Error al eliminar tarea'}), 500