# Freifach Informatik: Projekte mit KI und Hardware

Willkommen! In den nächsten Wochen baust du dein eigenes Projekt.
Zuerst machen wir **drei Lektionen gemeinsam**, danach arbeitest du allein oder im Team (max. 3 Personen) an deiner Idee.

Du kannst diese Seite auch zum Selbststudium nutzen. Jede Lektion hat lauffähigen Code und „Funktioniert es?“-Checks.

## So arbeitest du mit dem Material
1. **Lesen:** Die Lektionen findest du unten. Du kannst sie hier im Browser lesen.
2. **Auf den Laptop holen:** Für die Vorlagen brauchst du alle Dateien in VS Code.
   Klone das Repo mit VS Code, so kannst du später mit einem Klick Neues nachholen: **[Anleitung: Material mit GitHub und VS Code holen](anleitungen/github-vscode.md)**.
   Die Seiten in `ki/` öffnest du dort mit **Live Server**.
   (Notlösung ohne Git: [alles als ZIP herunterladen](https://github.com/masta-nksa/schere-stein-papier/archive/refs/heads/main.zip).)
3. **micro:bit-Programme:** Öffne die `.py`-Datei, kopiere den Code in den Editor [python.microbit.org](https://python.microbit.org) und lade ihn auf den micro:bit.
4. **Lösungen:** Zu jeder Vorlage gibt es eine Lösung, z. B. `ki/01-erkennen/loesung/runde.js` und `microbit/06_ssp_ki.py`. Schau sie erst an, wenn du es selbst versucht hast: Du lernst am meisten, wenn du zuerst eigene Fehler findest.

Das ganze Material liegt auch auf GitHub: [github.com/masta-nksa/schere-stein-papier](https://github.com/masta-nksa/schere-stein-papier).

## Der gemeinsame Einstieg: Schere-Stein-Papier

| Lektion | Thema | Was du lernst |
|---|---|---|
| [0](lektionen/00-setup.md) | Setup | micro:bit-Editor, Browser, GitHub Student Pack |
| [1](lektionen/01-microbit.md) | micro:bit | Eingabe → Verarbeitung → Ausgabe, Sensoren, Zufall, Funk |
| [2](lektionen/02-ki.md) | KI im Browser | Ein KI-Modell erkennt dein Handzeichen und spielt mit dem micro:bit |
| [3](lektionen/03-projektstart.md) | Projektstart | Idee, Team, Projektplan |

## Danach: drei Richtungen für dein Projekt
- **Spiele mit Gestensteuerung:** ein Spiel, das du mit Kamera und KI steuerst
- **KI bewegt etwas:** eine KI erkennt etwas, und Hardware reagiert (Servo, Licht, Ton)
- **Bauen und Robotik:** ein Gerät mit Sensoren und Aktoren, ohne KI

## Ordner

```
lektionen/     Anleitungen zu den drei Einstiegslektionen
anleitungen/   Material mit GitHub und VS Code holen
microbit/      micro:bit-Programme (MicroPython) zu Lektion 1 und 2
ki/            Browser-Seiten zu Lektion 2 (Handzeichen erkennen, Spiel, micro:bit per USB), mit Tests
vorlagen/      Projektplan und Milestones
beispiele/     Beispielprojekte zum Weiterbauen, z. B. "Fang das Licht"
lehrperson/    Ablauf der Einstiegslektionen
```

## Hardware
Weitere Bauteile (Taster, Drehgeber, Ultraschall, Servo, Neopixel, Displays) mit Masszeichnungen und Beispielen:
[micro:bit-Hardware-Katalog](https://masta-nksa.github.io/microbit-micropython-samples/hardware/)
