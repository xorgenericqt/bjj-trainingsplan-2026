# Slow Movie Player — Geburtstagsgeschenk zum 18.7. 🎁

Ein E-Ink-Bilderrahmen, der einen Film in Zeitlupe abspielt: **jeden Tag ein neues Bild**,
das aussieht wie ein gedruckter Foto-Kunstdruck. Basiert auf dem Open-Source-Projekt
[SlowMovie von Tom Whitwell](https://github.com/TomWhitwell/SlowMovie).

**Entscheidung: Schwarz/Weiß-Display (Waveshare 7,5" V2).**

---

## 1. Einkaufsliste (sofort bestellen!)

| # | Teil | Bezugsquelle | Preis ca. |
|---|------|--------------|-----------|
| 1 | **Waveshare 7,5" ePaper Display HAT V2** (800×480, S/W, SPI) | [BerryBase](https://www.berrybase.de/7.5-800-480-epaper-display-hat-for-raspberry-pi-v2) oder Amazon.de | 60–70 € |
| 2 | **Raspberry Pi Zero 2 WH** (WH = mit gelöteter Stiftleiste!) | [BerryBase](https://www.berrybase.de/raspberry-pi-zero-2-wh) | 20–25 € |
| 3 | microSD-Karte 16–32 GB (Class 10 / A1) | BerryBase / Amazon | ~8 € |
| 4 | USB-Netzteil 5 V (min. 2 A) + Micro-USB-Kabel | vorhandenes Handynetzteil oder BerryBase | 0–10 € |
| 5 | Bilderrahmen mit Tiefe, z. B. **IKEA RIBBA 18×24 cm** | IKEA | 8–15 € |
| 6 | Passepartout, Ausschnitt ca. **163×98 mm** (sichtbare Displayfläche) | Bastelladen / Online-Zuschnitt | 5–10 € |

**Gesamt: ca. 100–130 €** · BerryBase liefert ab Lager in 2–3 Werktagen (4,95 € Versand).

> ⚠️ Unbedingt die **„WH"-Variante** des Pi Zero 2 nehmen (Header vorbestückt) —
> dann muss nichts gelötet werden. Das Display-HAT wird einfach aufgesteckt.

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

## 6. Wie es funktioniert (Kurzfassung)

- SlowMovie (Python) zieht per **ffmpeg** einzelne Frames aus dem Video und
  rendert sie über **Pillow** + **omni-epd** auf das E-Ink-Display.
- E-Ink hält das Bild **ohne Strom** — der Pi braucht nur beim Bildwechsel Energie
  (Verbrauch insgesamt ~0,5 W, unter 2 € Stromkosten pro Jahr).
- Der Fortschritt wird gespeichert: Nach Stromausfall läuft der Film an derselben
  Stelle weiter.
- Alles über `slowmovie.conf` einstellbar: Geschwindigkeit, Zufallsmodus,
  Untertitel, Kontrast, mehrere Filme im Wechsel.
