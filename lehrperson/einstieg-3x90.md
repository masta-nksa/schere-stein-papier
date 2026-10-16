# Einstieg: 3 × 90 Minuten (Lehrperson)

Der Einstieg besteht aus vier **Etappen**: 0 Setup, 1 micro:bit, 2 KI im Browser, 3 Projektstart. Alle bauen dasselbe
Mini-Projekt (Schere-Stein-Papier), das alle vier Projektrichtungen berührt. Ab Etappe 3 wird projektartig gearbeitet.

Die SuS gehen die Etappen **in ihrem eigenen Tempo**: Wer fertig ist, geht zur nächsten Etappe weiter. Die Zeitpläne
unten sind ein **Richtplan** für drei Doppellektionen. Die kurzen Inputs (z. B. `ergebnis()` an der Tafel, das Protokoll)
bleiben gemeinsam: Wer schon weiter ist, hört kurz zu.
Etappe 3 (Ideenmarkt, Gruppen bilden) findet gemeinsam statt. Schnelle können vorher schon ihre Idee vorbereiten.

> Hinweis: Dieses Dokument enthält bewusst **keine Schülernamen**, damit das Repo öffentlich bleiben kann.

## Warum Schere-Stein-Papier?

| Richtung | Was sie darin wiederfindet |
|---|---|
| Spiele mit Gestensteuerung | Spielregeln, Zufall, Punkte, Multiplayer per Funk |
| KI bewegt etwas | Kamera erkennt ein Handzeichen, Hardware reagiert |
| Bauen und Robotik | Etappe 1 ist reine Hardware: Sensoren, Ausgaben, Funk |
| Spieleprogrammierung | Spiellogik selbst programmieren (`ergebnis()`, `runde.js`), Zustände einer Runde (Countdown, Ergebnis) |

Drei klar unterscheidbare Handzeichen sind zudem ideal für Teachable Machine.

## Doppellektion 1: Etappe 1 micro:bit (Eingabe → Verarbeitung → Ausgabe)

| Min. | Inhalt |
|---|---|
| 0–10 | Überblick über die Phase, Teaser: „Nächste Woche spielt ihr mit Handzeichen gegen den micro:bit.“ „Fang das Licht“ kurz zeigen. |
| 10–20 | Input: Eingabe → Verarbeitung → Ausgabe. Editor und Laden auf den micro:bit gemeinsam vorzeigen |
| 20–35 | Schritt 1 (Hallo) und Schritt 2 (Würfel) |
| 35–65 | Schritt 3: Schere-Stein-Papier. Die Funktion `ergebnis()` gemeinsam an der Tafel durchgehen (`% 3`) |
| 65–85 | Schritt 4 (Punkte, Ton), ★ für Schnelle: Funk zu zweit, Reaktionsspiel, ★★ Turnier zu dritt |
| 85–90 | Rückblick, Student Pack anstossen |

**Nur eingebaute Bauteile** (Display, Tasten, Beschleunigungssensor, Lautsprecher, Funk). Es braucht keine Verdrahtung.

## Doppellektion 2: Etappe 2 KI im Browser

| Min. | Inhalt |
|---|---|
| 0–10 | Rückblick, Input: Was ist ein KI-Modell, was sind Trainingsdaten? Datenschutz: Gesicht nicht im Bild |
| 10–28 | Schritt 1: Teachable Machine, Klassen `schere`, `stein`, `papier`, `nichts` trainieren, testen, Link kopieren |
| 28–48 | Schritt 2: Seite `ki/01-erkennen/` mit Live Server. Erkennung ansehen, dann **selbst die Spiellogik** in `runde.js` schreiben (5 TODOs). Gemeinsam klären: Was zählt bei 0? (letzte ca. 500 ms, Schwelle, häufigstes Zeichen) |
| 48–73 | Schritt 3: **`06_ssp_ki_vorlage.py` ausfüllen** (6 TODOs: Countdown mit Ton, Abbruch, Zufall, Ergebnis, Anzeige und Melodie, Schütteln), Seite `ki/02-microbit/` mit Web Serial. Das Protokoll gemeinsam an der Tafel lesen, dann im Log nachverfolgen. ★ Neopixel-Ampel |
| 73–85 | Schritt 4 (Finale): Duell per Funk in Paaren, Rücken an Rücken, `07_ssp_duell.py` (fertig, wird gelesen und verändert). Wer früh fertig ist, macht Aufgaben und ★ weiter |
| 85–90 | Rückblick, Vorschau auf den Projektstart |

Die Zeit ist knapp. **Schritt 4** gilt für alle Paare, die Schritt 3 fertig haben. Wer nur bis Schritt 3 kommt, hat die Kernaufgabe geschafft. Wer es nicht schafft, nimmt die **Lösungsdateien** (`ki/01-erkennen/loesung/runde.js`, `microbit/06_ssp_ki.py`), damit er trotzdem ein laufendes Spiel hat. Das Duell kann sonst als Demo mit zwei Freiwilligen gezeigt werden.

**Hardware in Etappe 2:** Display, Tasten, Lautsprecher (V2) und Schütteln (Beschleunigungssensor) gehören zu den Grundaufgaben, dazu USB und Funk. Zusatz ★: Neopixel-Ampel an Pin 1 (Streifen mit höchstens 8 Pixeln, am 3V-Anschluss des micro:bit, keine Batterie nötig). Ein Servo ist bewusst nicht eingeplant: Er braucht 5 V und ein Batteriepack und kommt erst in der Projektphase dazu.

★ für Schnelle: ml5 handPose statt Teachable Machine (nur Idee, kein eigener Code: Anleitung im Beispielprojekt „Fang das Licht“).

**Häufige Stolpersteine (zum Vorbereiten der Hilfe):**
- Der Python-Editor (WebUSB) muss vom micro:bit getrennt sein, sonst ist der USB-Port für die Seite besetzt.
- Nach jedem neuen Hochladen die Seite **Trennen** und danach neu verbinden.
- Der Tab mit der Seite muss im Vordergrund bleiben, sonst pausiert die Erkennung.
- Beim Duell braucht jedes Paar eine eigene `GRUPPE`.

## Doppellektion 3: Etappe 3 Projektstart (gemeinsam)

| Min. | Inhalt |
|---|---|
| 0–20 | Input: vier Richtungen, drei Stufen, Projektplan und Milestones |
| 20–40 | Ideenmarkt: 2-Minuten-Pitch pro Idee |
| 40–50 | Gruppen bilden (max. 3 oder allein) |
| 50–90 | Projektplan ausfüllen, Milestone 0 und 1 definieren, erste Arbeitsschritte |

## Differenzierung: eigenes Tempo
- **Eigenes Tempo:** Wer eine Etappe fertig hat, geht zur nächsten weiter. Vor Etappe 2 braucht es Git, VS Code und den geklonten Arbeitsordner ([Anleitung](../anleitungen/github-vscode.md)).
- **Grundaufgaben** mit „Funktioniert es?“-Checks: Wer wenig Vorkenntnisse hat, kommt Schritt für Schritt durch.
- **Zusatzaufgaben ★** für die Schnellen, z. B. Funk zu zweit, Reaktionsspiel, Turnier zu dritt, Schummel-micro:bit, ml5 handPose.
- Wer Hilfe braucht, bekommt sie von der Lehrperson. Die Schnellen arbeiten an den ★-Aufgaben weiter.

## Vorbereitung vor der ersten Doppellektion
- Ein micro:bit pro Person, USB-Kabel **mit Datenleitung**
- Alle sieben Programme (`01` bis `05`, ★ `08_reaktion.py`, ★★ `09_ssp_turnier.py`) einmal auf einem micro:bit testen (Schritt 4 braucht einen V2 für den Ton)
- Funk: Gruppennummern für die Paare vorbereiten, für das Turnier zusätzlich Dreiergruppen mit den `SPIELER`-Nummern 1, 2, 3
- Den SuS vorab sagen: Laptop mit Chrome oder Edge mitbringen

## Vorbereitung vor der zweiten Doppellektion
- Material für Etappe 2 liegt bereit: [Etappe 2](../etappen/02-ki.md), Seiten in `ki/`, micro:bit-Programme `microbit/06_ssp_ki_vorlage.py` (für die SuS), `microbit/06_ssp_ki.py` (Lösung) und `microbit/07_ssp_duell.py`. Lösung der Seite: `ki/01-erkennen/loesung/runde.js`. Die Lösungsdateien erst nach einem eigenen Versuch herausgeben.
- **Neopixel-Streifen** für das Zusatz ★ bereitlegen: höchstens 8 Pixel, schon gelötet. Anschluss vorab selbst testen (Daten an Pin 1, 3V, GND) und die SuS den Anschluss einmal abnehmen lassen.
- **Von Hand testen** (Kamera, USB und Funk konnten nur simuliert werden):
  - Schritt 2: Modell trainieren, Seite `ki/01-erkennen/` mit Live Server starten, alle Handzeichen und „nichts“ prüfen
  - Schritt 2: die Vorlage `runde.js` ausfüllen (oder die Lösung einsetzen) und eine Runde spielen
  - Schritt 3: `06_ssp_ki.py` (Lösung) laden, Editor trennen, Seite verbinden, mehrere Runden spielen, auch Schütteln und Ton
  - ★ Neopixel: `N_PIXEL` auf die Pixelzahl setzen und Countdown und Ergebnisfarben prüfen
  - Schritt 4: `07_ssp_duell.py` auf **zwei** micro:bits (zwei Laptops), mehrere Runden, auch mit absichtlich unklarem Handzeichen
  - Je einmal mit V1 und V2 probieren, falls beides im Einsatz ist
- Ein eigenes **Reserve-Modell** trainieren und den Link bereithalten (für SuS, deren Training nicht klappt)
- Kamera im Schul-WLAN prüfen, ebenso Zugriff auf `cdn.jsdelivr.net` (p5.js, TensorFlow.js, Teachable Machine) und auf den Modell-Link von Teachable Machine
- Prüfen, ob Chrome oder Edge an der Schule **Web Serial** zulässt (kann per Richtlinie gesperrt sein)
- Gruppennummern für die Paare vorbereiten (eine eigene Zahl pro Paar) und Plätze Rücken an Rücken einplanen
- VS Code + Live Server + Git bei den SuS, Repo klonen: als Hausaufgabe nach der ersten Doppellektion ([Anleitung](../anleitungen/github-vscode.md)). Wer schon in der ersten Doppellektion zu Etappe 2 kommt, macht das zuerst. Zu Beginn der zweiten Doppellektion kurz prüfen, wer es geschafft hat. Notlösung: ZIP-Download.
- Nach Änderungen an `ki/` oder `microbit/06–07` die Tests laufen lassen: `python ki/test/simuliere_microbit.py` und danach `node ki/test/test-logik.js`

## Veröffentlichung
- Website: [masta-nksa.github.io/schere-stein-papier](https://masta-nksa.github.io/schere-stein-papier/) (GitHub Pages, öffentlich)
- **Material-Repo** (hier wird alles geändert): [github.com/masta-nksa/schere-stein-papier](https://github.com/masta-nksa/schere-stein-papier), Branch `main`
- **Arbeits-Repo** für die SuS (zum Klonen): [github.com/masta-nksa/schere-stein-papier-code](https://github.com/masta-nksa/schere-stein-papier-code). Es enthält nur `ki/` (ohne Tests), `microbit/`, `beispiele/`, `vorlagen/`, ein eigenes README (`arbeits-repo/README.md`) und die Empfehlung für Live Server.
- **Abgleich:** Die GitHub-Action `.github/workflows/arbeits-repo.yml` überträgt diese Ordner bei jedem Push mit einem normalen Commit ins Arbeits-Repo. Sie schreibt mit einem Deploy-Key (Secret `ARBEITS_REPO_KEY`), der nur auf das Arbeits-Repo Zugriff hat. Status: im Material-Repo unter *Actions*. Von Hand starten: *Actions → Arbeits-Repo abgleichen → Run workflow*. **Nie direkt im Arbeits-Repo ändern**, sonst wird es beim nächsten Abgleich überschrieben.
- Die SuS klonen das Repo mit VS Code ([Anleitung](../anleitungen/github-vscode.md)) und arbeiten lokal mit Live Server. Neues holen sie mit Commit und Pull. Wenn du später eine Vorlage änderst, an der die SuS schon arbeiten, kann es beim Pull Konflikte geben. Ändere Vorlagen deshalb möglichst früh, bevor die ersten SuS daran arbeiten, oder lege neue Dateien an. Die Seite `ki/02-microbit/` geht auch direkt online, weil Pages `https` nutzt (Kamera und Web Serial funktionieren).
- Lösungen sind bewusst sichtbar (`loesung/`, `microbit/06_ssp_ki.py`).
- Für die Spieleprogrammierung gibt es ein drittes Repo, die Vorlage `spiel-vorlage`, und daraus die Team-Repos (siehe unten).
- Änderungen veröffentlichen: committen und `git push`. Nach ein bis zwei Minuten ist die Website aktuell. In Markdown keine doppelten geschweiften Klammern und keine geschweifte Klammer mit Prozentzeichen verwenden (Liquid-Syntax von Jekyll), sonst bricht der Pages-Build.

## Für die Projektphase
- **Neopixel:** Streifen in kurze Stücke schneiden und Anschlüsse anlöten. Das Löten kann auch eine Aufgabe in der Richtung „Bauen und Robotik“ sein.
- **Zwischenstand-Runde** etwa nach der Hälfte der Projektphase (zugleich Entscheidungspunkt Basis/Erweiterung), dazu eine Schlusspräsentation.
- **Lasercutter-Einführung** nach etwa vier Wochen Projektphase.

## Team-Repos für die Spieleprogrammierung
- **Vorlage:** Template-Repo [masta-nksa/spiel-vorlage](https://github.com/masta-nksa/spiel-vorlage), online unter [masta-nksa.github.io/spiel-vorlage](https://masta-nksa.github.io/spiel-vorlage/). Python mit pygame-ce, die GitHub-Action baut bei jedem Push mit pygbag und stellt das Spiel auf GitHub Pages. Eine Kopie liegt hier unter `spiel-vorlage/`. Es gibt keinen automatischen Abgleich: Änderungen an beiden Orten machen.
- **Auf Lager:** `spiel-team-1` bis `spiel-team-5` (öffentlich, Pages eingeschaltet, Spiel schon online). Ein Ruleset «main schützen» verhindert Force-Push und das Löschen von `main`. Als Owner bist du davon ausgenommen.
- **Vergeben:** Im Repo unter *Settings → Collaborators → Add people* die GitHub-Namen des Teams eintragen. Die SuS nehmen die Einladung an und folgen der [Anleitung für die SuS](../anleitungen/spiel-team-repo.md). Welches Team welches Repo hat, nicht hier notieren (öffentlich).
- **Wer darf pushen:** nur die Eingeladenen und du. Alle anderen können das Repo nur lesen. Collaborators haben Schreibrechte auf das ganze Repo (auch auf den Workflow), aber nur du kannst einladen, die Sichtbarkeit ändern, das Repo löschen oder archivieren.
- **Zurückgeben:** Collaborators entfernen. Zum Wiederverwenden besser ein neues Repo anlegen als ein altes zurücksetzen.
- **Ein weiteres Repo anlegen:** *Use this template* in `spiel-vorlage`, Owner `masta-nksa`, Public. Danach *Settings → Pages → Source: GitHub Actions* und, falls der erste Lauf rot ist, *Actions → Spiel online stellen → Run workflow*. Mit der GitHub CLI geht das auch per Befehl (`gh repo create masta-nksa/spiel-team-6 --public --template masta-nksa/spiel-vorlage`, dann `gh api -X POST repos/masta-nksa/spiel-team-6/pages -f build_type=workflow`).
- Änderungen an der Vorlage kommen **nicht** in schon angelegte Team-Repos.
- **Tutorial** zum Selbststudium: [beispiele/sternenfaenger/](../beispiele/sternenfaenger/README.md), sechs Schritte vom Fenster bis zur Vorlage, Schritte 1–4 als lauffähige Einzeldateien (geht auch ins Arbeits-Repo). Kopien davon liegen als `tutorial/` in der Vorlage und in den Team-Repos (Kopfzeile mit Startbefehl angepasst). Kein automatischer Abgleich: Änderungen an den Schritten an allen Orten nachführen.
- **Vorher testen:** Im Schul-WLAN prüfen, ob `masta-nksa.github.io` und `pygame-web.github.io` erreichbar sind (von dort lädt der Browser Python und pygame-ce).

## Rahmen
- Das Freifach ist freiwillig und wird nicht benotet. Milestones und Projektplan sind Orientierungshilfen ohne Abgabepflicht.
- Bei Interesse lassen sich bis zu 15 Doppellektionen anhängen.
