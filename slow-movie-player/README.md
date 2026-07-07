# Slow Movie Player — Geburtstagsgeschenk zum 18.7. 🎁

Ein E-Ink-Bilderrahmen, der einen Film in Zeitlupe abspielt: **jeden Tag ein neues Bild**,
das aussieht wie ein gedruckter Foto-Kunstdruck. Basiert auf dem Open-Source-Projekt
[SlowMovie von Tom Whitwell](https://github.com/TomWhitwell/SlowMovie).

**Entscheidung: Schwarz/Weiß-Display (Waveshare 7,5" V2).**

---

## 1. Einkaufsliste (Verfügbarkeit geprüft: 07.07.2026)

**Hauptbestellung — alles bei Welectron auf Lager:**

| # | Teil | Link | Preis |
|---|------|------|-------|
| 1 | **Waveshare 7,5" ePaper Display HAT V2** (800×480, S/W, SKU 13504) | [Welectron](https://www.welectron.com/Waveshare-13504-75inch-e-Paper-HAT) | 64,90 € |
| 2 | **Raspberry Pi 3 Modell B+** (Header verlötet, kein Zubehör nötig) | [Welectron](https://www.welectron.com/Raspberry-Pi-3-Modell-B_1) | 40,90 € |
| 2b | *Alternative, falls im Shop bestellbar:* Raspberry Pi Zero 2 W (ohne Header, braucht Hammer Header #3) | [Welectron](https://www.welectron.com/Raspberry-Pi-Zero-2-W_1) | 19,90 € |
| 4 | Offizielle Raspberry Pi microSD-Karte, **32 GB** wählen | [Welectron](https://www.welectron.com/Offizielle-Raspberry-Pi-microSD-Speicherkarte) | 9,90 € |
| 5 | Offizielles Raspberry Pi Micro-USB-Netzteil 5,1 V / 2,5 A | [Welectron](https://www.welectron.com/Official-Raspberry-Pi-Power-Supply-microUSB-51V-25A-EU-UK-US-AU) | 9,90 € |

**Nur nötig, falls Variante 2b (Zero 2 W) bestellt wird:**

| # | Teil | Link | Preis |
|---|------|------|-------|
| 3 | **GPIO Hammer Header** (lötfrei, Variante „Male Header") | [buyzero.de](https://buyzero.de/products/gpio-hammer-header-kein-loten-benotigt) | 2,69 € |

**Lokal besorgen:**

| # | Teil | Wo | Preis |
|---|------|----|-------|
| 6 | Bilderrahmen mit Tiefe, z. B. **IKEA RIBBA 18×24 cm** | IKEA | 8–15 € |
| 7 | Passepartout, Ausschnitt ca. **163×98 mm** (sichtbare Displayfläche) | Bastelladen / Online-Zuschnitt | 5–10 € |

**Gesamt: ca. 125–140 €** inkl. Versand.

> ⚠️ **Lieferengpass beim Pi Zero 2 (Stand 07/2026):** Die WH-Variante (mit
> vorbestücktem Header) war bei BerryBase, Rasppishop, Welectron und Botland
> ausverkauft; ebenso der Zero 2 W bei BerryBase/Rasppishop/buyzero/Reichelt.
> Nur **Welectron hatte den Zero 2 W (ohne Header) lagernd**. Der Hammer Header
> von buyzero wird ohne Löten mit ein paar Hammerschlägen montiert (Anleitung
> liegt bei). Alternativ: 2×20-Stiftleiste anlöten oder auf Amazon.de nach
> „Pi Zero 2 WH" (Prime) schauen — dort teurer, aber oft verfügbar.

## 2. Zeitplan bis zum 18.7.

| Datum | Schritt |
|-------|---------|
| 5.–6.7. | Bestellen (BerryBase + IKEA) |
| 9.–10.7. | Lieferung · SD-Karte flashen · Software installieren (Abend 1) |
| 11.–12.7. | Film vorbereiten · Konfiguration testen (Abend 2) |
| 13.–15.7. | Einbau in den Rahmen · 2–3 Tage Probelauf |
| 16.–17.7. | Puffer für Feintuning (Kontrast, Bildausschnitt) |
| **18.7.** | **Schenken** 🎉 (morgens `birthday_message.py` laufen lassen) |

## 3. Software-Installation (Abend 1, ca. 1 Stunde)

### 3.1 SD-Karte flashen

1. [Raspberry Pi Imager](https://www.raspberrypi.com/software/) herunterladen.
2. OS: **Raspberry Pi OS Lite (64-bit)**.
3. Im Imager unter „Einstellungen" (Zahnrad) direkt konfigurieren:
   - Hostname: `slowmovie`
   - SSH aktivieren
   - WLAN-Zugangsdaten eintragen
   - Benutzer/Passwort setzen

### 3.2 SlowMovie installieren

Pi mit aufgestecktem Display-HAT booten, dann per SSH verbinden (`ssh pi@slowmovie.local`):

```bash
# Offizielles Installationsskript (installiert ffmpeg, Python-Umgebung, systemd-Service)
curl -sSL https://raw.githubusercontent.com/TomWhitwell/SlowMovie/master/Install/install.sh | bash
```

Das Skript aktiviert SPI, installiert alle Abhängigkeiten und richtet den
Autostart-Service ein.

### 3.3 Unsere Konfiguration einspielen

Die Datei [`slowmovie.conf`](slowmovie.conf) aus diesem Ordner auf den Pi kopieren:

```bash
scp slowmovie.conf pi@slowmovie.local:~/SlowMovie/slowmovie.conf
```

Eingestellt ist darin:
- Displaytreiber für das Waveshare 7,5" V2 (S/W)
- **1 Bildwechsel pro Tag**, dabei springt der Film **1 Filmminute** weiter
  → ein 2-Stunden-Film läuft ca. 4 Monate
- Timecode-Anzeige aus, Vollbild an

Zum Testen kann man `delay` vorübergehend auf `30` stellen — dann wechselt das
Bild alle 30 Sekunden und man sieht sofort, ob alles funktioniert.

### 3.4 Film vorbereiten und hochladen

Beliebige `.mp4`-Datei (H.264). Tipp: vorher auf Display-Auflösung herunterrechnen,
das spart dem Pi Zero viel Arbeit:

```bash
# Auf dem eigenen Rechner (ffmpeg erforderlich):
ffmpeg -i film.mp4 -vf "scale=800:480:force_original_aspect_ratio=decrease" -an film_800.mp4
scp film_800.mp4 pi@slowmovie.local:~/SlowMovie/Videos/
```

Danach den Service neu starten:

```bash
ssh pi@slowmovie.local "sudo systemctl restart slowmovie"
```

## 4. Einbau in den Rahmen (13.–15.7.)

1. Glas des RIBBA-Rahmens **drin lassen** (schützt das Display, E-Ink ist matt genug).
   Wer es puristischer mag, lässt das Glas weg.
2. Passepartout mit 163×98-mm-Ausschnitt auf das Display legen, mit dünnem
   Klebeband hinten fixieren.
3. Display + Passepartout in den Rahmen, dahinter den Pi mit HAT
   (das Flachbandkabel des Displays vorsichtig falten, nicht knicken!).
4. Rückwand: kleine Aussparung für das USB-Kabel unten hineinschneiden.
5. Kabel an der Wand entlang nach unten führen — oder hinter einem Sideboard
   verschwinden lassen.

## 5. Geburtstags-Feature 🎂

[`birthday_message.py`](birthday_message.py) zeigt eine persönliche Widmung auf dem
Display an (Text in der Datei anpassen!). Am Morgen des 18.7. ausführen:

```bash
scp birthday_message.py pi@slowmovie.local:~/SlowMovie/
ssh pi@slowmovie.local "sudo systemctl stop slowmovie && cd ~/SlowMovie && .venv/bin/python birthday_message.py"
```

Die Botschaft bleibt stehen (E-Ink!), bis man den Film wieder startet:

```bash
ssh pi@slowmovie.local "sudo systemctl start slowmovie"
```

## 6. Mehrere Filme (Tarantino-Komplettpaket 🎬)

SlowMovie spielt **automatisch alle Videos im Ordner `Videos/`** nacheinander ab —
einfach alle Filme dort ablegen. Der Fortschritt wird **pro Film** gespeichert,
man kann also wechseln und später an derselben Stelle weiterschauen.

- Alle Filme vorher auf 800×480 herunterrechnen (siehe 3.4) — dann braucht jeder
  Film nur ~400–800 MB, alle 10 Tarantino-Filme passen locker auf eine 32-GB-Karte.
- Zufällige Reihenfolge statt alphabetisch: `random-file = True` in der Conf.
- **Gezielt umschalten**: [`switch_movie.sh`](switch_movie.sh) auf den Pi kopieren, dann z. B.:

```bash
ssh pi@slowmovie.local "~/SlowMovie/switch_movie.sh 'Pulp Fiction'"
```

Das Skript sucht den Film im Videos-Ordner, trägt ihn in die Conf ein und
startet den Service neu — das neue Bild erscheint nach wenigen Sekunden.

> Rechenbeispiel: Bei 1 Filmminute pro Tag läuft jeder Film ~4 Monate.
> Alle 10 Filme hintereinander = ein Geschenk, das **über 3 Jahre** läuft.

## 7. Wie es funktioniert (Kurzfassung)

- SlowMovie (Python) zieht per **ffmpeg** einzelne Frames aus dem Video und
  rendert sie über **Pillow** + **omni-epd** auf das E-Ink-Display.
- E-Ink hält das Bild **ohne Strom** — der Pi braucht nur beim Bildwechsel Energie
  (Verbrauch insgesamt ~0,5 W, unter 2 € Stromkosten pro Jahr).
- Der Fortschritt wird gespeichert: Nach Stromausfall läuft der Film an derselben
  Stelle weiter.
- Alles über `slowmovie.conf` einstellbar: Geschwindigkeit, Zufallsmodus,
  Untertitel, Kontrast, mehrere Filme im Wechsel.
