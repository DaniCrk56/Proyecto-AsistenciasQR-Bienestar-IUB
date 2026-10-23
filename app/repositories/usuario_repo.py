from app.core.database import Database
from app.models.usuario import Usuario

class UsuarioRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombres, apellidos, id_tipo_documento, numero_documento, correo_institucional, password_hash, id_programa, id_rol, estado, creado, actualizado FROM usuario WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, usuario_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombres, apellidos, id_tipo_documento, numero_documento, correo_institucional, password_hash, id_programa, id_rol, estado, creado, actualizado FROM usuario WHERE id = %s AND estado = TRUE;", (usuario_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, nombres, apellidos, id_tipo_documento, numero_documento, correo_institucional, password_hash, id_programa, id_rol):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombres, apellidos, id_tipo_documento, numero_documento, correo_institucional, password_hash, id_programa, id_rol, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE) RETURNING id;",
            (nombres, apellidos, id_tipo_documento, numero_documento, correo_institucional, password_hash, id_programa, id_rol)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, usuario_id, nombres, apellidos, correo_institucional):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET nombres = %s, apellidos = %s, correo_institucional = %s WHERE id = %s;",
            (nombres, apellidos, correo_institucional, usuario_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, usuario_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET estado = FALSE WHERE id = %s;", (usuario_id,))
        conn.commit()
        conn.close()
        return True
