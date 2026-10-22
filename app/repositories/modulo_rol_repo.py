from app.core.database import Database

class ModuloRolRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, id_rol, id_modulo, estado, creado, actualizado FROM modulo_rol WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, modulo_rol_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, id_rol, id_modulo, estado, creado, actualizado FROM modulo_rol WHERE id = %s AND estado = TRUE;", (modulo_rol_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, id_rol, id_modulo):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO modulo_rol (id_rol, id_modulo, estado) VALUES (%s, %s, TRUE) RETURNING id;",
            (id_rol, id_modulo)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, modulo_rol_id, id_rol, id_modulo):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE modulo_rol SET id_rol = %s, id_modulo = %s WHERE id = %s;",
            (id_rol, id_modulo, modulo_rol_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, modulo_rol_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE modulo_rol SET estado = FALSE WHERE id = %s;", (modulo_rol_id,))
        conn.commit()
        conn.close()
        return True