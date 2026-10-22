const express = require('express');
require('dotenv').config();

const rutasRecursos = require('./api/rutas_recursos');

const app = express();
const PORT = process.env.PORT || 4000;

app.use(express.json());

app.use('/recursos', rutasRecursos);

app.get('/', (req, res) => {
    res.json({ mensaje: "La API auxiliar de Express y MySQL se encuentra en línea y funcional" });
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});