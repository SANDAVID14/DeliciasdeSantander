<?php
// Configuración de Cabeceras CORS para permitir peticiones seguras
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

$dataFile = __DIR__ . '/../data/store.json';
$dataDir = __DIR__ . '/../data';

// Crear directorio data si no existe
if (!is_dir($dataDir)) {
    mkdir($dataDir, 0755, true);
}

// 1. GET: Retorna los datos actuales para cualquier visitante de la web
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($dataFile)) {
        echo file_get_contents($dataFile);
    } else {
        echo json_encode(["status" => "empty", "products" => [], "banners" => []]);
    }
    exit;
}

// 2. POST: Guarda los cambios del Administrador directamente en el archivo central del hosting
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $rawInput = file_get_contents('php://input');
    $inputData = json_decode($rawInput, true);

    if (!$inputData) {
        http_response_code(400);
        echo json_encode(["error" => "Datos JSON invalidos"]);
        exit;
    }

    // Verificación de seguridad mediante Token de Administrador
    $expectedToken = "Santander2026*";
    if (!isset($inputData['token']) || $inputData['token'] !== $expectedToken) {
        http_response_code(403);
        echo json_encode(["error" => "No autorizado. Token incorrecto."]);
        exit;
    }

    // Estructurar el contenido que verán todos los usuarios
    $storeContent = [
        "updatedAt" => date('c'),
        "products" => $inputData['products'] ?? [],
        "banners" => $inputData['banners'] ?? [],
        "orders" => $inputData['orders'] ?? []
    ];

    $saved = file_put_contents($dataFile, json_encode($storeContent, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

    if ($saved !== false) {
        http_response_code(200);
        echo json_encode([
            "success" => true,
            "message" => "Datos actualizados correctamente en el servidor del hosting",
            "updatedAt" => $storeContent["updatedAt"]
        ]);
    } else {
        http_response_code(500);
        echo json_encode(["error" => "No se pudo escribir en el archivo store.json. Verifique permisos de escritura (chmod 755 o 777 en carpeta data)."]);
    }
    exit;
}
