import zipfile
import os

zip_name = "Delicias_de_Santander_VLC_Sincronizacion_Hosting.zip"
files_to_zip = [
    "index.html",
    "_headers",
    "server.py",
    "server.js",
    "package.json",
    "data/store.json",
    "api/sync.php",
    "api/sync.js"
]

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for f in files_to_zip:
        if os.path.exists(f):
            zipf.write(f, arcname=f)
            print(f"Added {f} to {zip_name}")

print("Zip creation completed successfully:", os.path.getsize(zip_name), "bytes")
