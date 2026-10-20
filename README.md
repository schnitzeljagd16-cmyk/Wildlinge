# Wildlinge – Moos-Edition

Ein Sammel- und Kampfspiel im Stil der alten Handheld-Klassiker, komplett im Browser.

**Spielen:** https://schnitzeljagd16-cmyk.github.io/Wildlinge/

Die Startseite wählt automatisch die PC- oder Handy-Version. Andere Version wählen: `…/Wildlinge/#wahl`.

## Als App installieren
- **Android (Chrome):** Seite öffnen → Menü ⋮ → „App installieren“ / „Zum Startbildschirm hinzufügen“.
- **iPhone (Safari):** Teilen-Symbol → „Zum Home-Bildschirm“.
- **PC (Chrome/Edge):** Installieren-Symbol in der Adressleiste.

Nach dem ersten Start läuft das Spiel auch offline. Spielstände bleiben im Gerät gespeichert und gelten für beide Versionen.

## Android-App (APK)
Bei jedem Update baut GitHub automatisch eine neue APK. Neueste Version:
https://github.com/schnitzeljagd16-cmyk/Wildlinge/releases/latest → **Wildlinge.apk** auf dem Handy herunterladen und öffnen
(beim ersten Mal „Installation aus unbekannten Quellen“ für den Browser erlauben). Updates einfach drüber installieren, Spielstände bleiben.

## Aufbau
- `src/wildlinge.html` – Quellcode des Spiels
- `tools/make_variants.py` – erzeugt PC- und Handy-Version
- `tools/build_app.py` – baut die komplette App nach `app/`
- `.github/workflows/pages.yml` – veröffentlicht bei jedem Push auf `main` automatisch über GitHub Pages
