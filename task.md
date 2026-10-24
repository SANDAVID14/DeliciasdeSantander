# Plan de Implementación: Delicias de Santander VLC

## Objetivo
Finalizar y consolidar la plataforma de venta online y panel administrativo para el obrador "Delicias de Santander VLC", asegurando persistencia de datos, gestión de despachos semanales, pasarela de pagos y automatización de pedidos por WhatsApp.

---

## Fase 1: Auditoría y Estructura del Entorno
- [x] **1.1. Inspección de Código Existente**:
  - Analizar `index.html` para auditar componentes embebidos, estado de sesión (`admin`) y almacenamiento local (`localStorage`).
  - Revisar coherencia: la plataforma está centralizada en SPA pura autónoma (`index.html`) con sincronización vía `api/sync.php` / `server.js` y almacenamiento en `data/store.json`.
- [x] **1.2. Configuración de Entorno**:
  - Verificado entorno autónomo y sincronización en hosting (`store.json` y `sync.php` adaptados con soporte para `orders`).

---

## Fase 2: Catálogo Dinámico y Calendario de Despacho
- [x] **2.1. Gestión de Disponibilidad por Días**:
  - Permitir al administrador marcar días de producción/entrega específicos por producto (Lunes a Domingo).
  - Validar dinámicamente en checkout el corte de producción por día de servicio, bloqueando pedidos no compatibles y alertando días de cierre (Lunes).
- [x] **2.2. Precios y Promociones**:
  - Consolidar la lógica de precio original vs. precio promocional con cálculo de descuento automático y etiqueta visual tachada.
- [x] **2.3. Banners y Promociones**:
  - Probar persistencia de banners en el gestor administrativo (subida de imágenes, links de redirección, selector de degradados y textos).
  - Integrada rotación automática (cada 6s) y navegación interactiva por indicadores (dots) en la cabecera principal.

---

## Fase 3: Flujo de Pedidos y Mensajería WhatsApp
- [x] **3.1. Formateador de Pedidos para WhatsApp**:
  - Refinar el mensaje preformateado que se envía a `+34 603 374 784`:
    - Resumen detallado de productos, cantidades y precios.
    - Fecha con día de la semana y franja horaria solicitada de despacho.
    - Datos del cliente (nombre, dirección de entrega en Valencia o recogida en obrador C/ Sierra Martes 25).
    - Desglose imponible con 10% de IVA y selector de método de pago (Efectivo/Datáfono, Bizum, Tarjeta).
- [x] **3.2. Botón Individual por Producto**:
  - Verificar que el botón "Contactar al vendedor por WhatsApp" incluya el enlace directo al producto consultado.

---

## Fase 4: Panel Administrativo y Gestión del Obrador
- [x] **4.1. Seguridad del Panel**:
  - Validar autenticación de administrador (`admin` / `Santander2026*`).
  - Implementar persistencia de sesión segura en `sessionStorage` y cierre de sesión limpio.
- [x] **4.2. Consolidado de Producción**:
  - Crear vista imprimible / exportable de "Hoja de Producción del Día" agrupada por plato y franja horaria para el equipo de cocina.
- [x] **4.3. Control de Estados**:
  - Implementar transiciones de estado de pedido: *Pendiente* ➔ *En Preparación* ➔ *Listo para Entrega* ➔ *Entregado* ➔ *Cancelado*, con botón directo para notificar novedades por WhatsApp al cliente.

---

## Fase 5: Pruebas y Validación (Testing en Antigravity)
- [x] **5.1. Pruebas y Simulación Integral del Flujo**:
  - Simulación validada del ciclo de compra completo (catálogo, carrito, selector de entrega/recogida, validación de corte por día de la semana y cálculo de IVA/envío).
  - Simulación validada del flujo de administración: autenticación segura, edición de catálogo, gestión de banners y ciclo de vida de pedidos.
- [x] **5.2. Responsive Design**:
  - Comprobación de meta-tags responsive (`viewport`), breakpoints de Tailwind (`sm:`, `md:`, `lg:`), grillas adaptables de 1 a 3 columnas, y drawer móvil de carrito.
- [x] **5.3. Build & Deploy**:
  - Generados y validados artefactos de despliegue para Vercel (`vercel.json`), Netlify (`netlify.toml`), Cloudflare Pages (`_headers`), servidor Node.js (`server.js`, `api/sync.js`), Apache/cPanel con PHP (`api/sync.php`), y paquete ZIP de distribución listo para producción (`Delicias_de_Santander_VLC_Sincronizacion_Hosting.zip`).