const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const DATA_FILE = path.join(process.cwd(), 'data', 'store.json');

  if (req.method === 'GET') {
    try {
      if (fs.existsSync(DATA_FILE)) {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return res.status(200).json(JSON.parse(data));
      }
    } catch (e) {
      console.warn("Error leyendo data/store.json:", e);
    }
    return res.status(200).json({ products: [], banners: [], orders: [] });
  }

  if (req.method === 'POST') {
    const { token, products, banners, orders } = req.body || {};
    if (token !== 'Santander2026*') {
      return res.status(403).json({ error: 'Token inválido' });
    }

    const payload = {
      updatedAt: new Date().toISOString(),
      products: products || [],
      banners: banners || [],
      orders: orders || []
    };

    try {
      fs.writeFileSync(DATA_FILE, JSON.stringify(payload, null, 2), 'utf8');
    } catch (e) {
      console.warn("Sistema de archivos de solo lectura en serverless:", e);
    }

    return res.status(200).json({ success: true, message: 'Datos procesados exitosamente', data: payload });
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
};
