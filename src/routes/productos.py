from flask import Blueprint, jsonify, request
from extensions import mysql

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

# =====================================
# GET - Listar todos los productos
# =====================================
@productos_bp.route('/', methods=['GET'])
def listar_productos():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, precio_compra, 
                   precio_venta, precio_mayor, stock, categoria_id
            FROM productos
        """)
        datos = cursor.fetchall()

        productos = []
        for fila in datos:
            productos.append({
                "id": fila[0],
                "nombre": fila[1],
                "descripcion": fila[2],
                "precio_compra": float(fila[3]),
                "precio_venta": float(fila[4]),
                "precio_mayor": float(fila[5]) if fila[5] else None,
                "stock": fila[6],
                "categoria_id": fila[7]
            })

        return jsonify(productos), 200

    except Exception as e:
        return jsonify({"mensaje": "Error al obtener productos"}), 500


# =====================================
# GET - Obtener producto por ID
# =====================================
@productos_bp.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, precio_compra, 
                   precio_venta, precio_mayor, stock, categoria_id
            FROM productos
            WHERE id = %s
        """, (id,))
        dato = cursor.fetchone()

        if not dato:
            return jsonify({"mensaje": "Producto no encontrado"}), 404

        producto = {
            "id": dato[0],
            "nombre": dato[1],
            "descripcion": dato[2],
            "precio_compra": float(dato[3]),
            "precio_venta": float(dato[4]),
            "precio_mayor": float(dato[5]) if dato[5] else None,
            "stock": dato[6],
            "categoria_id": dato[7]
        }

        return jsonify(producto), 200

    except Exception:
        return jsonify({"mensaje": "Error al obtener producto"}), 500


# =====================================
# POST - Crear producto (CON VALIDACIÓN)
# =====================================
@productos_bp.route('/', methods=['POST'])
def crear_producto():
    try:
        data = request.json

        # Validar campos obligatorios
        campos_obligatorios = ['nombre', 'precio_compra', 'precio_venta', 'stock', 'categoria_id']
        for campo in campos_obligatorios:
            if campo not in data:
                return jsonify({"mensaje": f"Falta el campo obligatorio: {campo}"}), 400

        cursor = mysql.connection.cursor()

        # Validar que la categoría exista
        cursor.execute("SELECT id FROM categorias WHERE id = %s", (data['categoria_id'],))
        categoria = cursor.fetchone()

        if not categoria:
            return jsonify({"mensaje": "La categoría no existe"}), 400

        cursor.execute("""
            INSERT INTO productos
            (nombre, descripcion, precio_compra, precio_venta,
             precio_mayor, stock, categoria_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['nombre'],
            data.get('descripcion', ''),
            data['precio_compra'],
            data['precio_venta'],
            data.get('precio_mayor'),
            data['stock'],
            data['categoria_id']
        ))

        mysql.connection.commit()

        return jsonify({"mensaje": "Producto creado correctamente"}), 201

    except Exception as e:
        return jsonify({"mensaje": "Error al crear producto"}), 500


# =====================================
# PUT - Actualizar producto (CON VALIDACIÓN)
# =====================================
@productos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        data = request.json
        cursor = mysql.connection.cursor()

        # Verificar que el producto exista
        cursor.execute("SELECT id FROM productos WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({"mensaje": "Producto no encontrado"}), 404

        # Validar categoría si se envía
        if 'categoria_id' in data:
            cursor.execute("SELECT id FROM categorias WHERE id = %s", (data['categoria_id'],))
            if not cursor.fetchone():
                return jsonify({"mensaje": "La categoría no existe"}), 400

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                descripcion = %s,
                precio_compra = %s,
                precio_venta = %s,
                precio_mayor = %s,
                stock = %s,
                categoria_id = %s
            WHERE id = %s
        """, (
            data['nombre'],
            data.get('descripcion', ''),
            data['precio_compra'],
            data['precio_venta'],
            data.get('precio_mayor'),
            data['stock'],
            data['categoria_id'],
            id
        ))

        mysql.connection.commit()

        return jsonify({"mensaje": "Producto actualizado correctamente"}), 200

    except Exception:
        return jsonify({"mensaje": "Error al actualizar producto"}), 500


# =====================================
# DELETE - Eliminar producto
# =====================================
@productos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensaje": "Producto no encontrado"}), 404

        return jsonify({"mensaje": "Producto eliminado correctamente"}), 200

    except Exception:
        return jsonify({"mensaje": "Error al eliminar producto"}), 500