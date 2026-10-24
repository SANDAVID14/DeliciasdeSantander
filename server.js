const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'data', 'store.json');

app.use(cors());
app.use(express.json({ limit: '15mb' }));
app.use(express.static(__dirname));

// Endpoint GET: Obtener datos para los clientes (acepta /api/sync.php y /api/sync)
app.get(['/api/sync.php', '/api/sync'], (req, res) => {
  if (fs.existsSync(DATA_FILE)) {
    const data = fs.readFileSync(DATA_FILE, 'utf8');
    return res.json(JSON.parse(data));
  }
  return res.json({ products: [], banners: [], orders: [] });
});

// Endpoint POST: Guardar cambios del administrador en el hosting (acepta /api/sync.php y /api/sync)
app.post(['/api/sync.php', '/api/sync'], (req, res) => {
  const { token, products, banners, orders } = req.body;
  if (token !== 'Santander2026*') {
    return res.status(403).json({ error: 'Token inválido' });
  }

  const payload = {
    updatedAt: new Date().toISOString(),
    products: products || [],
    banners: banners || [],
    orders: orders || []
  };

  fs.writeFileSync(DATA_FILE, JSON.stringify(payload, null, 2), 'utf8');
  return res.json({ success: true, message: 'Datos guardados en el hosting exitosamente' });
});

app.listen(PORT, () => {
  console.log(`Servidor de Delicias de Santander activo en http://localhost:${PORT}`);
});
