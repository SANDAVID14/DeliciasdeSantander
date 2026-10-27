# Instrucciones para que las Modificaciones del Administrador se vean en Toda la Web

## ¿Por qué no se veían antes los cambios en otros dispositivos?
Anteriormente, el panel guardaba los datos en el `localStorage` del navegador local (solo en el teléfono o computador del administrador). Los clientes que visitaban la web abrían su propia sesión en blanco y no recibían esas ediciones.

## ¿Cómo funciona la nueva sincronización automática con el hosting?
Hemos implementado una **arquitectura en tiempo real cliente-servidor**:
1. **Cuando un cliente entra a la web**: El navegador consulta automáticamente al hosting el archivo `data/store.json`. Siempre recibe los productos, precios, fotos, ofertas y banners más recientes.
2. **Cuando el administrador modifica algo en el panel**: Al pulsar *"Guardar Producto"* o *"Guardar Banner"*, la aplicación hace una llamada segura (`POST /api/sync.php`) hacia el hosting con la clave maestra `Santander2026*`.
3. El hosting reescribe el archivo `data/store.json` central de inmediato.
4. A partir de ese segundo, **cualquier persona en cualquier parte del mundo** que abra la tienda ve los cambios reflejados.

## Instalación en tu Hosting (Hostinger, cPanel, Raiola, Webempresa, etc.)
1. Descomprime este archivo ZIP en la carpeta pública de tu hosting (habitualmente `public_html/` o `www/`).
2. Asegúrate de que la carpeta `/data` tenga permisos de lectura y escritura (`755` o `775`).
3. ¡Listo! Todo funciona automáticamente con PHP sin necesidad de bases de datos complejas.

## Si tu hosting o entorno es Node.js (Vercel, VPS, Render)
- Ejecuta `npm install express cors` y arranca con `node server.js`.

## Si ejecutas localmente con Python (Windows / Mac / Linux)
- Ejecuta `python server.py` y abre `http://localhost:3000`.
