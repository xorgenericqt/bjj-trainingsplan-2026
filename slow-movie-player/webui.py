#!/usr/bin/env python3
"""SlowMovie Remote - Mini-Weboberflaeche zum Filmwechseln per Handy.

Laeuft ohne Zusatzpakete (nur Python-Standardbibliothek).
Im Browser oeffnen: http://slowmovie.local:8080

Installation auf dem Pi:
    scp webui.py slowmovie-web.service pi@slowmovie.local:~/SlowMovie/
    ssh pi@slowmovie.local
    sudo cp ~/SlowMovie/slowmovie-web.service /etc/systemd/system/
    sudo systemctl enable --now slowmovie-web
"""

import os
import re
import subprocess
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE, "Videos")
CONF = os.path.join(BASE, "slowmovie.conf")
PORT = 8080

SPEEDS = [
    ("1 Bild pro Tag (1 Filmminute/Tag)", 86400, 1440),
    ("1 Bild pro Stunde", 3600, 60),
    ("1 Bild pro Minute", 60, 1),
    ("Test: alle 30 Sekunden", 30, 4),
]

PAGE = """<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Slow Movie Remote</title>
<style>
 body {{ font-family: -apple-system, sans-serif; background: #14100c; color: #f0e6d2;
        max-width: 480px; margin: 0 auto; padding: 16px; }}
 h1 {{ font-size: 22px; letter-spacing: 2px; }}
 h2 {{ font-size: 14px; text-transform: uppercase; letter-spacing: 2px; color: #b3946a; margin-top: 28px; }}
 .film, .speed {{ display: block; width: 100%; text-align: left; margin: 8px 0; padding: 14px;
        background: #2a211a; color: #f0e6d2; border: 1px solid #4a3a28; border-radius: 10px;
        font-size: 16px; }}
 .active {{ border-color: #e6b800; background: #3a2e1a; }}
 .active::after {{ content: " \\25B6"; color: #e6b800; }}
 .msg {{ padding: 10px; background: #1e3a1e; border-radius: 8px; margin: 10px 0; }}
</style></head><body>
<h1>&#127902; SLOW MOVIE REMOTE</h1>
{msg}
<h2>Film w&auml;hlen</h2>
<form method="post" action="/switch">{films}</form>
<h2>Geschwindigkeit</h2>
<form method="post" action="/speed">{speeds}</form>
</body></html>"""


def read_conf():
    try:
        with open(CONF) as f:
            return f.read()
    except OSError:
        return ""


def write_conf_value(text, key, value):
    if re.search(rf"^{key}\s*=", text, re.M):
        return re.sub(rf"^{key}\s*=.*$", f"{key} = {value}", text, flags=re.M)
    return text.rstrip("\n") + f"\n{key} = {value}\n"


def restart_slowmovie():
    subprocess.run(["systemctl", "restart", "slowmovie"], check=False)


class Handler(BaseHTTPRequestHandler):
    def _send(self, html, code=200):
        body = html.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _page(self, msg=""):
        conf = read_conf()
        m = re.search(r"^file\s*=\s*(.+)$", conf, re.M)
        current = os.path.basename(m.group(1).strip()) if m else None
        films = sorted(
            f for f in os.listdir(VIDEO_DIR)
            if f.lower().endswith((".mp4", ".mkv", ".avi", ".mov"))
        ) if os.path.isdir(VIDEO_DIR) else []
        film_html = "".join(
            f'<button class="film{" active" if f == current else ""}" '
            f'name="file" value="{urllib.parse.quote(f)}">{f}</button>'
            for f in films
        ) or "<p>Keine Filme im Videos-Ordner.</p>"
        speed_html = "".join(
            f'<button class="speed" name="preset" value="{d}:{i}">{label}</button>'
            for label, d, i in SPEEDS
        )
        msg_html = f'<div class="msg">{msg}</div>' if msg else ""
        self._send(PAGE.format(msg=msg_html, films=film_html, speeds=speed_html))

    def do_GET(self):
        self._page()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = urllib.parse.parse_qs(self.rfile.read(length).decode())
        conf = read_conf()
        if self.path == "/switch" and data.get("file"):
            fname = urllib.parse.unquote(data["file"][0])
            if os.path.isfile(os.path.join(VIDEO_DIR, fname)):
                conf = write_conf_value(conf, "file", f"Videos/{fname}")
                with open(CONF, "w") as f:
                    f.write(conf)
                restart_slowmovie()
                return self._page(f"L&auml;uft jetzt: {fname}")
        if self.path == "/speed" and data.get("preset"):
            delay, inc = data["preset"][0].split(":")
            conf = write_conf_value(conf, "delay", delay)
            conf = write_conf_value(conf, "increment", inc)
            with open(CONF, "w") as f:
                f.write(conf)
            restart_slowmovie()
            return self._page("Geschwindigkeit ge&auml;ndert.")
        self._page("Unbekannte Aktion.")

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"SlowMovie Remote auf Port {PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
