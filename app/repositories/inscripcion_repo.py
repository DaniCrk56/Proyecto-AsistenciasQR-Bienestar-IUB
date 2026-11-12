
from app.core.database import Database
from app.models.inscripcion import Inscripcion

class InscripcionRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()

        if not conn:
            return []

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, id_usuario, id_actividad, codigo_qr,
                   estado, creado, actualizado
            FROM inscripcion
            WHERE estado = TRUE;
        """)

        filas = cursor.fetchall()
        conn.close()

        return filas

    def obtener_por_id(self, inscripcion_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, id_usuario, id_actividad, codigo_qr,
                   estado, creado, actualizado
            FROM inscripcion
            WHERE id = %s AND estado = TRUE;
        """, (inscripcion_id,))

        fila = cursor.fetchone()
        conn.close()

        return fila

    def crear(self, inscripcion):
        conn = self.db.get_connection()

        if not conn:
            return None

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM inscripcion
            WHERE id_usuario = %s
            AND id_actividad = %s
            AND estado = TRUE;
        """, (
            inscripcion.usuario_id,
            inscripcion.actividad_id
        ))

        existente = cursor.fetchone()

        if existente:
            conn.close()
            return "duplicada"

        cursor.execute("""
            INSERT INTO inscripcion (id_usuario, id_actividad)
            VALUES (%s, %s)
            RETURNING id, codigo_qr;
        """, (
            inscripcion.usuario_id,
            inscripcion.actividad_id
        ))

        resultado = cursor.fetchone()

        conn.commit()
        conn.close()

        return resultado

    def eliminar(self, inscripcion_id):
        conn = self.db.get_connection()

        if not conn:
            return False

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE inscripcion
            SET estado = FALSE,
                actualizado = NOW()
            WHERE id = %s;
        """, (inscripcion_id,))

        exito = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return exito

    def actualizar(self, inscripcion_id, inscripcion):
        conn = self.db.get_connection()

        if not conn:
            return False

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE inscripcion
            SET id_usuario = %s,
                id_actividad = %s,
                actualizado = NOW()
            WHERE id = %s AND estado = TRUE;
        """, (
            inscripcion.usuario_id,
            inscripcion.actividad_id,
            inscripcion_id
        ))

        exito = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return exito
