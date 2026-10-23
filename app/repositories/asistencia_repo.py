from app.core.database import Database
from app.models.asistencia import Asistencia

class AsistenciaRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, id_inscripcion, fecha_asistencia, metodo, id_validador, estado, creado, actualizado FROM asistencia WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, asistencia_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, id_inscripcion, fecha_asistencia, metodo, id_validador, estado, creado, actualizado FROM asistencia WHERE id = %s AND estado = TRUE;", (asistencia_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, id_inscripcion, metodo, id_validador):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO asistencia (id_inscripcion, metodo, id_validador, estado) VALUES (%s, %s, %s, TRUE) RETURNING id;",
            (id_inscripcion, metodo, id_validador)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def eliminar(self, asistencia_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE asistencia SET estado = FALSE WHERE id = %s;", (asistencia_id,))
        conn.commit()
        conn.close()
        return True
