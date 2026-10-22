class RecursoModel {
    constructor(data) {
        this.nombre = data.nombre;
        this.codigo_serial = data.codigo_serial;
        this.id_categoria = data.id_categoria;
    }

    validar() {
        if (!this.nombre || !this.codigo_serial || !this.id_categoria) {
            throw new Error("Todos los campos obligatorios deben ser completados.");
        }
        return true;
    }
}

module.exports = RecursoModel;