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


    def registrar_por_qr(self, codigo_qr, id_evento, id_validador):

        conn = self.db.get_connection()

        if not conn:
            return {"estado": "error"}

        cursor = conn.cursor()

        try:
            # Buscar la inscripción correspondiente al QR y al evento
            cursor.execute("""
                SELECT id
                FROM inscripcion
                WHERE codigo_qr = %s
                AND id_actividad = %s
                AND estado = TRUE;
            """, (codigo_qr, id_evento))

            inscripcion = cursor.fetchone()

            if not inscripcion:
                return {"estado": "no_encontrada"}

            if isinstance(inscripcion, dict):
                id_inscripcion = inscripcion["id"]
            else:
                id_inscripcion = inscripcion[0]

            # Comprobar si ya tiene asistencia registrada
            cursor.execute("""
                SELECT id
                FROM asistencia
                WHERE id_inscripcion = %s
                AND estado = TRUE;
            """, (id_inscripcion,))

            asistencia = cursor.fetchone()

            if asistencia:
                return {"estado": "duplicada"}

            # Registrar asistencia
            cursor.execute("""
                INSERT INTO asistencia (
                    id_inscripcion,
                    metodo,
                    id_validador,
                    estado
                )
                VALUES (%s, 'QR', %s, TRUE)
                RETURNING id;
            """, (id_inscripcion, id_validador))

            nueva_asistencia = cursor.fetchone()

            if isinstance(nueva_asistencia, dict):
                nuevo_id = nueva_asistencia["id"]
            else:
                nuevo_id = nueva_asistencia[0]

            conn.commit()

            return {
                "estado": "registrada",
                "id": nuevo_id
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()

def obtener_por_evento(self, id_evento):

    conn = self.db.get_connection()

    if not conn:
        return []

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                a.id,
                u.nombres,
                u.apellidos,
                u.numero_documento,
                act.nombre AS evento,
                a.fecha_asistencia,
                a.metodo
            FROM asistencia a
            INNER JOIN inscripcion i
                ON a.id_inscripcion = i.id
            INNER JOIN usuario u
                ON i.id_usuario = u.id
            INNER JOIN actividad act
                ON i.id_actividad = act.id
            WHERE i.id_actividad = %s
            AND a.estado = TRUE
            ORDER BY a.fecha_asistencia DESC;
        """, (id_evento,))

        filas = cursor.fetchall()

        if filas and not isinstance(filas[0], dict):
            columnas = [columna[0] for columna in cursor.description]
            filas = [dict(zip(columnas, fila)) for fila in filas]

        return filas

    finally:
        cursor.close()
        conn.close()
