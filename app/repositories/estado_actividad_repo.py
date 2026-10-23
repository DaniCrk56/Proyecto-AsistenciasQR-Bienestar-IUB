from app.core.database import Database
from app.models.estado_actividad import EstadoActividad

class EstadoActividadRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, estado, creado, actualizado FROM estado_actividad WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, estado_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, estado, creado, actualizado FROM estado_actividad WHERE id = %s AND estado = TRUE;", (estado_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, nombre):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO estado_actividad (nombre, estado) VALUES (%s, TRUE) RETURNING id;",
            (nombre,)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, estado_id, nombre):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE estado_actividad SET nombre = %s WHERE id = %s;",
            (nombre, estado_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, estado_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE estado_actividad SET estado = FALSE WHERE id = %s;", (estado_id,))
        conn.commit()
        conn.close()
        return True
