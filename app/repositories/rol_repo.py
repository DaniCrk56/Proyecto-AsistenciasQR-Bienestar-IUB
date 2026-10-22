from app.core.database import Database

class RolRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, estado, creado, actualizado FROM rol WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, rol_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, estado, creado, actualizado FROM rol WHERE id = %s AND estado = TRUE;", (rol_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, nombre, descripcion):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rol (nombre, descripcion, estado) VALUES (%s, %s, TRUE) RETURNING id;",
            (nombre, descripcion)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, rol_id, nombre, descripcion):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rol SET nombre = %s, descripcion = %s WHERE id = %s;",
            (nombre, descripcion, rol_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, rol_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE rol SET estado = FALSE WHERE id = %s;", (rol_id,))
        conn.commit()
        conn.close()
        return True