from app.core.database import Database

class InscripcionRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, id_usuario, id_actividad, codigo_qr, estado, creado, actualizado FROM inscripcion WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, inscripcion_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, id_usuario, id_actividad, codigo_qr, estado, creado, actualizado FROM inscripcion WHERE id = %s AND estado = TRUE;", (inscripcion_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, id_usuario, id_actividad):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inscripcion (id_usuario, id_actividad, estado) VALUES (%s, %s, TRUE) RETURNING id;",
            (id_usuario, id_actividad)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def eliminar(self, inscripcion_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE inscripcion SET estado = FALSE WHERE id = %s;", (inscripcion_id,))
        conn.commit()
        conn.close()
        return True