const express = require('express');
const router = express.Router();
const RecursoRepository = require('../repositories/recurso_repo');
const RecursoModel = require('../models/recurso');

const repo = new RecursoRepository();

// GET: Listar todos
router.get('/', async (req, res) => {
    try {
        const recursos = await repo.obtenerTodos();
        res.json(recursos);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// GET: Obtener por ID
router.get('/:id', async (req, res) => {
    try {
        const recurso = await repo.obtenerPorId(req.params.id);
        if (!recurso) return res.status(404).json({ mensaje: "Recurso no encontrado" });
        res.json(recurso);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// POST: Crear un nuevo recurso
router.post('/', async (req, res) => {
    try {
        const modelo = new RecursoModel(req.body);
        modelo.validar();

        const nuevoId = await repo.crear(req.body);
        res.status(201).json({ mensaje: "Recurso registrado exitosamente", id: nuevoId });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// PUT: Actualizar un recurso
router.put('/:id', async (req, res) => {
    try {
        const exito = await repo.actualizar(req.params.id, req.body);
        if (!exito) return res.status(404).json({ mensaje: "Recurso no encontrado o sin cambios" });
        res.json({ mensaje: "Recurso actualizado correctamente" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// DELETE: Eliminación lógica (estado = 0)
router.delete('/:id', async (req, res) => {
    try {
        const exito = await repo.eliminar(req.params.id);
        if (!exito) return res.status(404).json({ mensaje: "Recurso no encontrado" });
        res.json({ mensaje: "Recurso eliminado (lógicamente) correctamente" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;