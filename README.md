# Wildlinge – Moos-Edition

Ein Sammel- und Kampfspiel im Stil der alten Handheld-Klassiker, komplett im Browser.

**Spielen:** https://schnitzeljagd16-cmyk.github.io/Wildlinge/

Die Startseite wählt automatisch die PC- oder Handy-Version. Andere Version wählen: `…/Wildlinge/#wahl`.

## Als App installieren
- **Android (Chrome):** Seite öffnen → Menü ⋮ → „App installieren“ / „Zum Startbildschirm hinzufügen“.
- **iPhone (Safari):** Teilen-Symbol → „Zum Home-Bildschirm“.
- **PC (Chrome/Edge):** Installieren-Symbol in der Adressleiste.

Nach dem ersten Start läuft das Spiel auch offline. Spielstände bleiben im Gerät gespeichert und gelten für beide Versionen.

## Aufbau
- `src/wildlinge.html` – Quellcode des Spiels
- `tools/make_variants.py` – erzeugt PC- und Handy-Version
- `tools/build_app.py` – baut die komplette App nach `app/`
- `.github/workflows/pages.yml` – veröffentlicht bei jedem Push auf `main` automatisch über GitHub Pages
