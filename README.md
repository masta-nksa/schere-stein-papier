# Freifach Informatik: Projekte mit KI und Hardware

Willkommen! In den nächsten Wochen baust du dein eigenes Projekt.
Zum Einstieg gehst du **vier Etappen** durch, in deinem **eigenen Tempo**: Bist du mit einer Etappe fertig, gehst du einfach zur nächsten weiter. Danach arbeitest du allein oder im Team (max. 3 Personen) an deiner Idee.

Du kannst diese Seite auch zum Selbststudium nutzen. Jede Etappe hat lauffähigen Code und „Funktioniert es?“-Checks.

## So arbeitest du mit dem Material
1. **Lesen:** Die Etappen findest du unten. Du kannst sie hier im Browser lesen.
2. **Auf den Laptop holen:** Für die Vorlagen brauchst du alle Dateien in VS Code.
   Klone dazu deinen **Arbeitsordner** [schere-stein-papier-code](https://github.com/masta-nksa/schere-stein-papier-code) mit VS Code. So kannst du später mit einem Klick Neues nachholen: **[Anleitung: Material mit GitHub und VS Code holen](anleitungen/github-vscode.md)**.
   Die Seiten in `ki/` öffnest du dort mit **Live Server**.
   (Notlösung ohne Git: [Arbeitsordner als ZIP herunterladen](https://github.com/masta-nksa/schere-stein-papier-code/archive/refs/heads/main.zip).)
3. **micro:bit-Programme:** Öffne die `.py`-Datei, kopiere den Code in den Editor [python.microbit.org](https://python.microbit.org) und lade ihn auf den micro:bit.
4. **Lösungen:** Zu jeder Vorlage gibt es eine Lösung, z. B. `ki/01-erkennen/loesung/runde.js` und `microbit/06_ssp_ki.py`. Schau sie erst an, wenn du es selbst versucht hast: Du lernst am meisten, wenn du zuerst eigene Fehler findest.

Auf GitHub: [Arbeitsordner zum Klonen](https://github.com/masta-nksa/schere-stein-papier-code) · [ganzes Material mit Website](https://github.com/masta-nksa/schere-stein-papier)

## Der Einstieg: Schere-Stein-Papier in vier Etappen

| Etappe | Thema | Was du lernst |
|---|---|---|
| [0](etappen/00-setup.md) | Setup | micro:bit-Editor, Browser, GitHub Student Pack |
| [1](etappen/01-microbit.md) | micro:bit | Eingabe → Verarbeitung → Ausgabe, Sensoren, Zufall, Funk |
| [2](etappen/02-ki.md) | KI im Browser | Ein KI-Modell erkennt dein Handzeichen und spielt mit dem micro:bit |
| [3](etappen/03-projektstart.md) | Projektstart | Idee, Team, Projektplan |

## Danach: vier Richtungen für dein Projekt
- **Spiele mit Gestensteuerung:** ein Spiel, das du mit Kamera und KI steuerst
- **KI bewegt etwas:** eine KI erkennt etwas, und Hardware reagiert (Servo, Licht, Ton)
- **Bauen und Robotik:** ein Gerät mit Sensoren und Aktoren, ohne KI
- **Spieleprogrammierung:** ein Spiel in Python (pygame-ce), ohne Hardware und ohne KI, das online im Browser läuft ([Tutorial](beispiele/sternenfaenger/README.md) · [Team-Repo klonen](anleitungen/spiel-team-repo.md))

## Ordner

```
etappen/       Anleitungen zu den vier Etappen des Einstiegs
anleitungen/   Material mit GitHub und VS Code holen, Team-Repo für Spiele klonen
arbeits-repo/  README und Abgleich für den Arbeitsordner schere-stein-papier-code
microbit/      micro:bit-Programme (MicroPython) zu Etappe 1 und 2
ki/            Browser-Seiten zu Etappe 2 (Handzeichen erkennen, Spiel, micro:bit per USB), mit Tests
vorlagen/      Projektplan und Milestones
beispiele/     Beispielprojekte zum Weiterbauen: "Fang das Licht", Tutorial "Sternenfänger" (Spiel mit Python)
spiel-vorlage/ Vorlage für Spiele mit Python (pygame-ce) im Browser, Kopie des Repos spiel-vorlage
lehrperson/    Richtplan und Vorbereitung für die Lehrperson
```

## Hardware
Weitere Bauteile (Taster, Drehgeber, Ultraschall, Servo, Neopixel, Displays) mit Masszeichnungen und Beispielen:
[micro:bit-Hardware-Katalog](https://masta-nksa.github.io/microbit-micropython-samples/hardware/)
