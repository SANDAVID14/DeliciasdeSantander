import http.server
import socketserver
import os
import json
import urllib.parse
import subprocess
from datetime import datetime, timezone

PORT = 3000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'store.json')

def push_to_github(commit_msg):
    """Ejecuta git add, git commit y git push origin master en el repositorio local."""
    try:
        subprocess.run(["git", "add", "data/store.json"], cwd=BASE_DIR, capture_output=True, text=True, check=True)
        res_commit = subprocess.run(["git", "commit", "-m", commit_msg], cwd=BASE_DIR, capture_output=True, text=True)
        res_push = subprocess.run(["git", "push", "origin", "master"], cwd=BASE_DIR, capture_output=True, text=True, timeout=30)
        if res_push.returncode == 0:
            return True, "Sincronizado y publicado en GitHub exitosamente"
        else:
            return False, f"Git push error: {res_push.stderr.strip()}"
    except Exception as e:
        return False, f"Excepcion Git: {str(e)}"

class StoreHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ['/api/sync.php', '/api/sync']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"products": [], "banners": [], "orders": []}).encode('utf-8'))
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ['/api/sync.php', '/api/sync', '/api/git-push']:
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length)
            try:
                data = json.loads(post_body.decode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "JSON invalido"}).encode('utf-8'))
                return

            if data.get('token') != 'Santander2026*':
                self.send_response(403)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Token invalido"}).encode('utf-8'))
                return

            # Si es solo /api/git-push
            if path == '/api/git-push':
                ok, msg = push_to_github(f"feat(admin): sincronizacion manual con GitHub ({datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')})")
                self.send_response(200 if ok else 500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"success": ok, "message": msg}).encode('utf-8'))
                return

            now_iso = datetime.now(timezone.utc).isoformat()
            payload = {
                "updatedAt": now_iso,
                "products": data.get("products", []),
                "banners": data.get("banners", []),
                "orders": data.get("orders", [])
            }

            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)

            # Auto-commit y push automático a GitHub
            commit_title = f"feat(admin): actualizacion desde panel movil/web ({datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')})"
            gh_ok, gh_msg = push_to_github(commit_title)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Datos guardados y actualizados en GitHub" if gh_ok else f"Datos guardados localmente ({gh_msg})",
                "githubSynced": gh_ok,
                "githubDetails": gh_msg,
                "updatedAt": payload["updatedAt"]
            }).encode('utf-8'))
            return

        self.send_response(405)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Method Not Allowed"}).encode('utf-8'))

if __name__ == '__main__':
    os.chdir(BASE_DIR)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), StoreHandler) as httpd:
        print(f"Servidor Delicias de Santander activo en http://0.0.0.0:{PORT}")
        print("Sincronizacion bidireccional con GitHub activada.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
