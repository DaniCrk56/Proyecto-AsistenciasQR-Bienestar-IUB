from app.core.database import Database

class ProgramaRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, estado, creado, actualizado FROM programa WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, programa_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, estado, creado, actualizado FROM programa WHERE id = %s AND estado = TRUE;", (programa_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, nombre):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO programa (nombre, estado) VALUES (%s, TRUE) RETURNING id;",
            (nombre,)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, programa_id, nombre):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE programa SET nombre = %s WHERE id = %s;",
            (nombre, programa_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, programa_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE programa SET estado = FALSE WHERE id = %s;", (programa_id,))
        conn.commit()
        conn.close()
        return True