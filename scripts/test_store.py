import urllib.request
import json

def test():
    # 1. Probar local server
    try:
        req = urllib.request.urlopen("http://localhost:3000/index.html")
        html = req.read().decode('utf-8')
        print("Local server index.html: OK", len(html), "bytes")
    except Exception as e:
        print("Local server index.html: ERR", e)

    # 2. Probar api/sync en local
    try:
        req = urllib.request.urlopen("http://localhost:3000/api/sync")
        data = json.loads(req.read().decode('utf-8'))
        print("Local server /api/sync: OK, products count:", len(data.get('products', [])))
        print("Banner 1 imageUrl:", data.get('banners', [])[0].get('imageUrl')[:40] if data.get('banners') else "N/A")
    except Exception as e:
        print("Local server /api/sync: ERR", e)

    # 3. Validar sintaxis basica de index.html
    with open("index.html", "r", encoding="utf-8") as f:
        c = f.read()
    assert "<!DOCTYPE html>" in c
    assert "ReactDOM.createRoot" in c
    print("HTML assertions passed.")

if __name__ == "__main__":
    test()
