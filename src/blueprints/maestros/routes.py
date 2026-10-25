from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))

# GET: Listar todos los maestros
@maestros_bp.route('/', methods=['GET'])
def listar_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM maestros")
        datos = cursor.fetchall()
        maestros = [fila_a_diccionario(cursor, fila) for fila in datos]
        return jsonify({
            'maestros': maestros,
            'exito': True
        }), 200
    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar los maestros: {}'.format(ex),
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

# GET: Buscar un maestro por ID
@maestros_bp.route("/<string:id>", methods=['GET'])
def leer_maestro(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM maestros WHERE id = %s", (id,))
        fila = cursor.fetchone()
        if fila is None:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404
        maestro = fila_a_diccionario(cursor, fila)
        return jsonify({
            'maestro': maestro,
            'exito': True
        }), 200
    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar el maestro: {}'.format(ex),
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

# POST: Registrar un maestro
@maestros_bp.route('/', methods=['POST'])
def registrar_maestro():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'Se requiere un objeto JSON',
            'exito': False
        }), 400

    campos = ['id', 'nombre', 'apaterno', 'amaterno', 'correo']

    if any(
        campo not in datos
        or not str(datos[campo]).strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'Faltan campos obligatorios o son inválidos',
            'exito': False
        }), 400

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id FROM maestros WHERE id = %s",
            (str(datos['id']).strip(),)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                'mensaje': 'El ID del maestro ya existe',
                'exito': False
            }), 409

        cursor.execute("""
            INSERT INTO maestros
                (id, nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """, tuple(str(datos[campo]).strip() for campo in campos))

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro registrado correctamente',
            'exito': True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            'mensaje': 'Error al registrar el maestro: {}'.format(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

# PUT: Modificar un maestro
@maestros_bp.route("/<string:id>", methods=['PUT'])
def modificar_maestro(id):
    datos = request.get_json()
    if not datos:
        return jsonify({
            "mensaje": "No se recibieron datos para modificar"
        }), 400

    nombre = datos.get('nombre')
    apaterno = datos.get('apaterno')
    amaterno = datos.get('amaterno', '')
    correo = datos.get('correo')

    if not nombre or not apaterno or not correo:
        return jsonify({
            "mensaje": "Nombre, apellido paterno y correo son obligatorios"
        }), 400

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM maestros WHERE id = %s", (id,))
        maestro = cursor.fetchone()
        if not maestro:
            return jsonify({
                "mensaje": "No existe un maestro con ese ID"
            }), 404

        sql = """
            UPDATE maestros
            SET nombre = %s,
                apaterno = %s,
                amaterno = %s,
                correo = %s
            WHERE id = %s
        """
        cursor.execute(sql, (nombre, apaterno, amaterno, correo, id))
        mysql.connection.commit()
        return jsonify({
            "mensaje": "Maestro modificado correctamente",
            "id": id
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            "mensaje": "Error al modificar el maestro",
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

# DELETE: Eliminar un maestro
@maestros_bp.route("/<string:id>", methods=['DELETE'])
def eliminar_maestro(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM maestros WHERE id = %s", (id,))
        maestro = cursor.fetchone()
        if not maestro:
            return jsonify({
                "mensaje": "No existe un maestro con ese ID"
            }), 404

        cursor.execute("DELETE FROM maestros WHERE id = %s", (id,))
        mysql.connection.commit()
        return jsonify({
            "mensaje": "Maestro eliminado correctamente",
            "id": id
        }), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({
            "mensaje": "Error al eliminar el maestro",
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()