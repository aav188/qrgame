"""Convierte un juego HTML en un código QR con el juego dentro.

Uso: .venv/bin/python crear_qr.py tractores.html   -> crea tractores_qr.png

El QR contiene un enlace https normal (las cámaras lo abren solas):
    https://aav188.github.io/qrgame/#<juego comprimido>
La página index.html (el "lanzador") descomprime lo que va después del "#"
y lo ejecuta. El juego viaja dentro del QR, no está guardado en el servidor.
"""
import base64
import sys
import zlib

import segno

LANZADOR = "https://aav188.github.io/qrgame/"

entrada = sys.argv[1] if len(sys.argv) > 1 else "juego.html"
nombre = entrada.rsplit(".", 1)[0]

html = open(entrada, encoding="utf-8").read().strip()

# Comprimimos (deflate) y pasamos a base64 "url-safe": así el enlace es más
# corto y solo usa letras, números, "-" y "_", que ningún lector de QR estropea.
comp = zlib.compressobj(9, zlib.DEFLATED, -15)
datos = comp.compress(html.encode("utf-8")) + comp.flush()
url = LANZADOR + "#" + base64.urlsafe_b64encode(datos).decode().rstrip("=")

qr = segno.make(url, error="l", micro=False)
qr.save(f"{nombre}_qr.png", scale=6, border=4)
open(f"{nombre}_url.txt", "w", encoding="utf-8").write(url)

print(f"Juego: {len(html.encode())} bytes -> enlace de {len(url)} caracteres")
print(f"Versión de QR: {qr.version} ({qr.symbol_size()[0]} módulos de lado)")
