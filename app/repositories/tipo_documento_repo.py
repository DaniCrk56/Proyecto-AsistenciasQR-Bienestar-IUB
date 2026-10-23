from app.core.database import Database
from app.models.tipo_documento import TipoDocumento

class TipoDocumentoRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT id, codigo, nombre, estado, creado, actualizado FROM tipo_documento WHERE estado = TRUE;")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, tipo_id):
        conn = self.db.get_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT id, codigo, nombre, estado, creado, actualizado FROM tipo_documento WHERE id = %s AND estado = TRUE;", (tipo_id,))
        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, codigo, nombre):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tipo_documento (codigo, nombre, estado) VALUES (%s, %s, TRUE) RETURNING id;",
            (codigo, nombre)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return nuevo_id

    def actualizar(self, tipo_id, codigo, nombre):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tipo_documento SET codigo = %s, nombre = %s WHERE id = %s;",
            (codigo, nombre, tipo_id)
        )
        conn.commit()
        conn.close()
        return True

    def eliminar(self, tipo_id):
        conn = self.db.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("UPDATE tipo_documento SET estado = FALSE WHERE id = %s;", (tipo_id,))
        conn.commit()
        conn.close()
        return True
