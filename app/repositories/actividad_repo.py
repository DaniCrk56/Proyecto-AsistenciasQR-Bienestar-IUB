
from app.core.database import Database
from app.models.actividad import Actividad


class ActividadRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, fecha, hora_inicio,
                   hora_fin, cupo_maximo, id_lugar, id_categoria,
                   id_estado_actividad, id_responsable, estado,
                   creado, actualizado
            FROM actividad
            WHERE estado = TRUE;
        """)

        filas = cursor.fetchall()
        conn.close()
        return filas

    def obtener_por_id(self, actividad_id):
        conn = self.db.get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, fecha, hora_inicio,
                   hora_fin, cupo_maximo, id_lugar, id_categoria,
                   id_estado_actividad, id_responsable, estado,
                   creado, actualizado
            FROM actividad
            WHERE id = %s AND estado = TRUE;
        """, (actividad_id,))

        fila = cursor.fetchone()
        conn.close()
        return fila

    def crear(self, actividad: Actividad):
        conn = self.db.get_connection()
        if not conn:
            return False

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO actividad (
                nombre, descripcion, fecha, hora_inicio, hora_fin,
                cupo_maximo, id_lugar, id_categoria,
                id_estado_actividad, id_responsable, estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
            RETURNING id;
        """, (
            actividad.nombre,
            actividad.descripcion,
            actividad.fecha,
            actividad.hora_inicio,
            actividad.hora_fin,
            actividad.cupo_maximo,
            actividad.id_lugar,
            actividad.id_categoria,
            actividad.id_estado_actividad,
            actividad.id_responsable
        ))

        nuevo_id = cursor.fetchone()["id"]

        conn.commit()
        conn.close()

        return nuevo_id

    def actualizar(self, actividad_id, actividad: Actividad):
        conn = self.db.get_connection()
        if not conn:
            return False

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE actividad
            SET nombre = %s,
                descripcion = %s,
                fecha = %s,
                hora_inicio = %s,
                hora_fin = %s,
                cupo_maximo = %s,
                id_lugar = %s,
                id_categoria = %s,
                id_estado_actividad = %s
            WHERE id = %s AND estado = TRUE;
        """, (
            actividad.nombre,
            actividad.descripcion,
            actividad.fecha,
            actividad.hora_inicio,
            actividad.hora_fin,
            actividad.cupo_maximo,
            actividad.id_lugar,
            actividad.id_categoria,
            actividad.id_estado_actividad,
            actividad_id
        ))

        exito = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return exito

    def eliminar(self, actividad_id):
        conn = self.db.get_connection()
        if not conn:
            return False

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE actividad
            SET estado = FALSE
            WHERE id = %s AND estado = TRUE;
        """, (actividad_id,))

        exito = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return exito
