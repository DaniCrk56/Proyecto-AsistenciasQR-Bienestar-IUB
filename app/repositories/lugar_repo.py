from app.core.database import Database

class LugarRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, capacidad, estado, creado, actualizado FROM lugar WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, lugar_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, capacidad, estado, creado, actualizado FROM lugar WHERE id = %s AND estado = TRUE;", (lugar_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, nombre, capacidad):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lugar (nombre, capacidad, estado) VALUES (%s, %s, TRUE) RETURNING id;",
            (nombre, capacidad)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, lugar_id, nombre, capacidad):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE lugar SET nombre = %s, capacidad = %s WHERE id = %s;",
            (nombre, capacidad, lugar_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, lugar_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE lugar SET estado = FALSE WHERE id = %s;", (lugar_id,))
        conn.commit()
        conn.close()
        return True