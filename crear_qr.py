"""Convierte un juego HTML en un código QR con el juego dentro.

Uso: .venv/bin/python crear_qr.py tractores.html   -> crea tractores_qr.png

El QR contiene un enlace https normal (las cámaras lo abren solas):
    https://aav188.github.io/qrgame/#<juego comprimido>
La página index.html (el "lanzador") descomprime lo que va después del "#"
y lo ejecuta. El juego viaja dentro del QR, no está guardado en el servidor.
"""
import sys
import zlib

import qrcode

LANZADOR = "https://aav188.github.io/qrgame/#"

# Los QR tienen un modo "alfanumérico" que guarda estos 45 símbolos con solo
# 5.5 bits cada uno (en vez de 8). Usamos 43 de ellos (sin espacio ni %, que
# romperían el enlace) para escribir el juego comprimido: 2 bytes -> 3 símbolos.
ALFABETO = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$*+-./:"


def base43(datos: bytes) -> str:
    out = ""
    for i in range(0, len(datos), 2):
        if i + 1 < len(datos):
            n = datos[i] * 256 + datos[i + 1]
            out += ALFABETO[n % 43] + ALFABETO[n // 43 % 43] + ALFABETO[n // 1849]
        else:
            out += ALFABETO[datos[i] % 43] + ALFABETO[datos[i] // 43]
    return out


entrada = sys.argv[1] if len(sys.argv) > 1 else "juego.html"
nombre = entrada.rsplit(".", 1)[0]

html = open(entrada, encoding="utf-8").read().strip()

comp = zlib.compressobj(9, zlib.DEFLATED, -15)
datos = comp.compress(html.encode("utf-8")) + comp.flush()
url = LANZADOR + base43(datos)

# optimize: el inicio del enlace va en modo normal y el juego en modo alfanumérico.
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=6, border=4)
qr.add_data(url, optimize=20)
qr.make(fit=True)
qr.make_image().save(f"{nombre}_qr.png")
open(f"{nombre}_url.txt", "w", encoding="utf-8").write(url)

print(f"Juego: {len(html.encode())} bytes -> enlace de {len(url)} caracteres")
print(f"Versión de QR: {qr.version} ({qr.modules_count} módulos de lado)")
