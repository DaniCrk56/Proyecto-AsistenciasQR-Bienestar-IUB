from app.core.database import Database
from app.models.categoria_actividad import CategoriaActividad

class CategoriaActividadRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, estado, creado, actualizado FROM categoria_actividad WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, categoria_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, estado, creado, actualizado FROM categoria_actividad WHERE id = %s AND estado = TRUE;", (categoria_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, nombre, descripcion):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categoria_actividad (nombre, descripcion, estado) VALUES (%s, %s, TRUE) RETURNING id;",
            (nombre, descripcion)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, categoria_id, nombre, descripcion):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE categoria_actividad SET nombre = %s, descripcion = %s WHERE id = %s;",
            (nombre, descripcion, categoria_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, categoria_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE categoria_actividad SET estado = FALSE WHERE id = %s;", (categoria_id,))
        conn.commit()
        conn.close()
        return True
