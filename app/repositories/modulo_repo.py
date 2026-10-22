from app.core.database import Database

class ModuloRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, estado, creado, actualizado FROM modulo WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, modulo_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, estado, creado, actualizado FROM modulo WHERE id = %s AND estado = TRUE;", (modulo_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, nombre, descripcion):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO modulo (nombre, descripcion, estado) VALUES (%s, %s, TRUE) RETURNING id;",
            (nombre, descripcion)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, modulo_id, nombre, descripcion):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE modulo SET nombre = %s, descripcion = %s WHERE id = %s;",
            (nombre, descripcion, modulo_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, modulo_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE modulo SET estado = FALSE WHERE id = %s;", (modulo_id,))
        conn.commit()
        conn.close()
        return True