const db = require('../core/database');

class RecursoRepository {
    async obtenerTodos() {
        const [rows] = await db.query("SELECT * FROM recurso WHERE estado = 1 ORDER BY id ASC;");
        return rows;
    }

    async obtenerPorId(id) {
        const [rows] = await db.query("SELECT * FROM recurso WHERE id = ? AND estado = 1;", [id]);
        return rows[0];
    }

    async crear(recurso) {
        const query = "INSERT INTO recurso (nombre, codigo_serial, id_categoria, estado) VALUES (?, ?, ?, 1);";
        const [result] = await db.query(query, [recurso.nombre, recurso.codigo_serial, recurso.id_categoria]);
        return result.insertId;
    }

    async actualizar(id, recurso) {
        const query = "UPDATE recurso SET nombre = ?, codigo_serial = ?, id_categoria = ? WHERE id = ?;";
        const [result] = await db.query(query, [recurso.nombre, recurso.codigo_serial, recurso.id_categoria, id]);
        return result.affectedRows > 0;
    }

    async eliminar(id) {
        // Borrado lógico: cambia el estado a 0 sin borrar el registro de la tabla (exigencia del parcial)
        const query = "UPDATE recurso SET estado = 0 WHERE id = ?;";
        const [result] = await db.query(query, [id]);
        return result.affectedRows > 0;
    }
}

module.exports = RecursoRepository;