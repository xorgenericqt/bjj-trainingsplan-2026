# Übergabe an die lokale Claude-Code-Session

## Mission
Slow Movie Player fertig einrichten — ein Geburtstagsgeschenk (Deadline: **18. Juli**).
Ein Raspberry Pi zeigt Filme auf einem E-Ink-Display in Zeitlupe (1 Bildwechsel/Tag).
Die Hardware ist fertig zusammengebaut und gebootet; es fehlt die komplette Software-Einrichtung.

## Ist-Zustand
- **Hardware:** Raspberry Pi 3 B+ mit aufgestecktem Waveshare 7,5" e-Paper HAT V2
  (800×480, S/W, SKU 13504). Panel über Adapter-Board + weißes FFC-Kabel verbunden.
  Schalter auf dem HAT: Display Config = **B**, Interface Config = **0** (geprüft).
- **OS:** Raspberry Pi OS Lite (64-bit) frisch geflasht. Hostname `slowmovie`,
  Benutzer `pi`, SSH aktiviert, WLAN konfiguriert. Pi ist gebootet und im Heimnetz.
- **Noch nichts installiert** — apt-Update, SlowMovie und unsere Dateien fehlen.

## Zugang
```
ssh pi@slowmovie.local        # Passwort: <VOM USER EINSETZEN>
```
Falls der Hostname nicht auflöst: IP im Router nachschlagen (Gerät „slowmovie").

## Projekt-Dateien
In diesem Ordner (`slow-movie-player/` in diesem Repo, Branch
`claude/slow-movie-player-gift-bntwng`):
- `README.md` — komplette Schritt-für-Schritt-Anleitung (maßgeblich!)
- `slowmovie.conf` — fertige Konfiguration (Treiber `waveshare_epd.epd7in5_V2`, 1 Bild/Tag)
- `webui.py` + `slowmovie-web.service` — Handy-Weboberfläche (Port 8080, LAN-only)
- `switch_movie.sh` — Filmwechsel per SSH
- `birthday_message.py` — Geburtstags-Widmung fürs Display (Text in `LINES` anpassen!)

## Aufgaben (in dieser Reihenfolge)
1. Per SSH auf den Pi. `sudo apt update && sudo apt full-upgrade -y`
2. SlowMovie installieren (offizieller Installer, Autostart-Service: Ja):
   `curl -sSL https://raw.githubusercontent.com/TomWhitwell/SlowMovie/master/Install/install.sh | bash`
   Danach `sudo reboot`, neu verbinden.
3. Unsere 5 Dateien per scp nach `~/SlowMovie/` kopieren (überschreibt die Standard-conf).
4. `chmod +x ~/SlowMovie/switch_movie.sh`; Web-UI-Service installieren:
   `sudo cp ~/SlowMovie/slowmovie-web.service /etc/systemd/system/ && sudo systemctl enable --now slowmovie-web`
5. Testfilm: Den User fragen, wo seine Film-MP4s liegen. Einen Film lokal konvertieren
   (ffmpeg nötig, ggf. installieren) und hochladen:
   `ffmpeg -i FILM.mp4 -vf "scale=800:480:force_original_aspect_ratio=decrease" -an -c:v libx264 -crf 23 OUT.mp4`
   `scp OUT.mp4 pi@slowmovie.local:~/SlowMovie/Videos/`
6. Testmodus: in `~/SlowMovie/slowmovie.conf` vorübergehend `delay = 30`, `increment = 4`
   setzen, `sudo systemctl restart slowmovie`. **Erfolgskriterium: Nach ≤ 2 Minuten
   erscheint ein Filmbild auf dem E-Ink-Display** (Bildaufbau flackert ~10 s, das ist normal).
7. Alle übrigen Filme konvertieren + hochladen (gleicher ffmpeg-Aufruf pro Datei).
8. Endzustand: `delay = 86400`, `increment = 1440` (= 1 Bildwechsel/Tag, 1 Filmminute/Tag),
   Service neu starten. Web-UI prüfen: `http://slowmovie.local:8080` zeigt die Filmliste.

## Debugging-Spickzettel
- Log live: `journalctl -u slowmovie -f`
- Display bleibt weiß → meist FFC-Kabel/Klemme oder Schalter (B/0); SPI prüfen:
  `ls /dev/spidev*` (muss existieren), sonst `sudo raspi-config` → Interface → SPI.
- Web-UI-Status: `sudo systemctl status slowmovie-web`
- SlowMovie-venv: `~/SlowMovie/.venv/bin/python`

## Regeln
- Vor allem, was Daten löscht oder das System neu flasht: erst den User fragen.
- Keine Portfreigaben/Cloud-Dienste einrichten — Web-UI bleibt LAN-only.
- Am 18.7. morgens: `birthday_message.py` (Text vorher mit dem User abstimmen) —
  Ablauf steht im README, Abschnitt „Geburtstags-Feature".
