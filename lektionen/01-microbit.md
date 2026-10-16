# Lektion 1: micro:bit – Schere-Stein-Papier

**Ziel:** Am Ende spielst du Schere-Stein-Papier gegen deinen micro:bit.
Nächste Woche erkennt eine KI dein Handzeichen über die Kamera und schickt es an den micro:bit.

## Die wichtigste Idee: Eingabe → Verarbeitung → Ausgabe
Fast jedes Gerät funktioniert so, egal ob Spiel, Roboter oder Waschmaschine:

| Eingabe | Verarbeitung | Ausgabe |
|---|---|---|
| Taste, Sensor, Kamera | dein Programm entscheidet | Display, Ton, Motor, Licht |

Achte heute bei jedem Schritt darauf: Was ist die Eingabe, was die Ausgabe?

## Vorbereitung
1. Öffne [python.microbit.org](https://python.microbit.org) in **Chrome oder Edge**.
2. Schliesse den micro:bit mit dem USB-Kabel an.
3. Code in den Editor kopieren, dann **Send to micro:bit** (das erste Mal verbinden und den micro:bit auswählen).

Kein Chrome/Edge? Dann **Save** drücken und die `.hex`-Datei auf das Laufwerk **MICROBIT** ziehen.

---

## Schritt 1: Hallo micro:bit
**Code:** [`microbit/01_hallo.py`](../microbit/01_hallo.py)

Taste A zeigt ein lachendes Gesicht, Taste B ein trauriges.

**Funktioniert es?**

- [ ] „Hallo“ läuft durch.
- [ ] A und B zeigen verschiedene Gesichter.

**Aufgaben**
1. Ändere den Text, der am Anfang durchläuft.
2. Nimm andere Bilder. Im Editor links unter **Reference** findest du alle, z. B. `Image.HEART`.
3. Was passiert, wenn du die Zeile `sleep(50)` löschst? (Tipp: es passiert wenig. Warum ist sie trotzdem sinnvoll?)

---

## Schritt 2: Würfel (Sensor + Zufall)
**Code:** [`microbit/02_wuerfel.py`](../microbit/02_wuerfel.py)

Schüttle den micro:bit. Der Beschleunigungssensor merkt das, und das Programm würfelt eine Zahl.

**Funktioniert es?**

- [ ] Schütteln zeigt eine Zahl.
- [ ] Die Zahl ändert sich.

**Aufgaben**
1. Mach einen Würfel von 1 bis 12.
2. Statt einer Zahl ein Bild: Bei 1 bis 3 ein `Image.HAPPY`, sonst ein `Image.SAD`.
3. ★ Neige statt schütteln: Ersetze `"shake"` durch `"left"` oder `"right"`. Was ändert sich?

---

## Schritt 3: Schere-Stein-Papier
**Code:** [`microbit/03_ssp.py`](../microbit/03_ssp.py)

- **Taste A:** deine Wahl wechseln (Stein → Papier → Schere)
- **Taste B:** bestätigen. Der micro:bit zeigt seine Wahl, dann das Ergebnis (✓, ✗ oder =).

**Funktioniert es?**

- [ ] A wechselt die drei Bilder.
- [ ] B zeigt die Wahl des micro:bit.
- [ ] Das Ergebnis stimmt.

**Verstehen:** Schau dir die Funktion `ergebnis()` an. Sie rechnet `(ich - gegner) % 3`.
Probiere auf Papier aus, warum `1` „gewonnen“ bedeutet. (Stein = 0, Papier = 1, Schere = 2.)

**Aufgaben**
1. Zeichne eigene Bilder für Stein, Papier und Schere. `9` ist hell, `0` aus, jede Zeile hat 5 Zeichen.
2. Statt mit Taste B soll man mit **Schütteln** bestätigen.

---

## Schritt 4: Punkte und Ton (Best of 3)
**Code:** [`microbit/04_ssp_punkte.py`](../microbit/04_ssp_punkte.py)

Jetzt zählt der micro:bit die Punkte und spielt Töne. Wer zuerst 3 Runden gewinnt, gewinnt das Spiel.

**Funktioniert es?**

- [ ] Der Spielstand läuft durch, z. B. `2:1`.
- [ ] Es gibt Töne.
- [ ] Nach 3 Siegen beginnt ein neues Spiel.

**Aufgaben**
1. Ändere `ZIEL`, damit man 5 Runden gewinnen muss.
2. Andere Töne: unter **Reference** findest du Melodien wie `music.NYAN`.
3. ★ Der micro:bit schummelt: Er gewinnt etwas häufiger als normal. Wie würdest du das einbauen?

---

## Zusatz ★: Zu zweit per Funk
**Code:** [`microbit/05_ssp_funk.py`](../microbit/05_ssp_funk.py)

Zwei micro:bits spielen gegeneinander. Beide laden das Programm und stellen **dieselbe** `GRUPPE` ein.
Jedes Paar braucht eine **eigene** Zahl, sonst funkt ihr euch gegenseitig dazwischen.

**Funktioniert es?**

- [ ] Nach dem Abschicken dreht sich die Uhr.
- [ ] Wenn beide abgeschickt haben, sehen beide das Ergebnis.

**Aufgaben**
1. Zählt Punkte wie in Schritt 4.
2. ★★ Was passiert, wenn ein drittes Gerät in derselben Gruppe mitfunkt? Wie könnte man das verhindern?

---

## Zusatz ★: Reaktionsspiel
**Code:** [`microbit/08_reaktion.py`](../microbit/08_reaktion.py)

Wie schnell bist du? **Taste A** startet, das Display wird dunkel. Nach einer Zufallszeit leuchtet es ganz auf, und du drückst so schnell wie möglich **Taste B**. Der micro:bit misst die Zeit mit `running_time()` und zeigt sie in Millisekunden. Zu früh gedrückt? Dann zählt es nicht.

**Funktioniert es?**

- [ ] Nach dem Start wird das Display dunkel.
- [ ] Es leuchtet nach 2 bis 5 Sekunden auf.
- [ ] Deine Zeit läuft über das Display.
- [ ] Zu früh gedrückt zeigt ein trauriges Gesicht.

**Aufgaben**
1. Vergleicht eure Zeiten: Wer ist am schnellsten? Wirst du mit mehreren Versuchen schneller?
2. Ändere die Wartezeit auf 1 bis 8 Sekunden. Was ändert sich beim Spielen?
3. Spiele fünf Runden hintereinander und zeige am Ende den **Durchschnitt** an. (Tipp: Zeiten in einer Liste sammeln, mit `sum(zeiten) // len(zeiten)` rechnen.)
4. ★★ Statt `running_time()`: Zähle in der Warteschleife selbst, wie oft `sleep(1)` durchlaufen wurde. Warum ist das ungenauer?

---

## Zusatz ★★: Schere-Stein-Papier zu dritt (Turnier)
**Code:** [`microbit/09_ssp_turnier.py`](../microbit/09_ssp_turnier.py)

Drei micro:bits spielen gleichzeitig. Alle haben dieselbe `GRUPPE`, aber jeder eine **andere** `SPIELER`-Nummer (1, 2 oder 3). Taste A wechselt die Wahl, Taste B schickt sie ab. Sobald alle drei abgeschickt haben, zeigt jeder die beiden anderen Zeichen und sein Ergebnis. Für jeden besiegten Gegner gibt es einen Punkt.

Funk kann Nachrichten verlieren. Darum wird jede Wahl mehrmals gefunkt, und jede Nachricht trägt eine **Rundennummer**. Nachrichten einer anderen Runde werden ignoriert, so zählt eine alte Wahl nicht in der neuen Runde.

**Funktioniert es?**

- [ ] Nach dem Abschicken dreht sich die Uhr.
- [ ] Wenn alle abgeschickt haben, sehen alle die Zeichen der anderen.
- [ ] Die Punkte stimmen (prüft nach: Stein gegen Schere = 1 Punkt)

**Aufgaben**
1. Was passiert, wenn nur zwei von drei abschicken? Wie lange wartet der micro:bit? (Tipp: `WARTEN_MS`.)
2. Wozu dient die Rundennummer? Streiche sie gedanklich weg: Was könnte schiefgehen?
3. Ändere die Punkte: Sieg 3 Punkte, Unentschieden 1 Punkt.
4. ★ Wer zuerst 10 Punkte hat, gewinnt: Zeige ein Siegerbild und beginne neu.

---

## Rückblick
Beantworte für dich:
- Was waren heute die **Eingaben**? Was die **Ausgaben**?
- Wo steckt in deinem Spiel die **Verarbeitung**, also die Entscheidung?
- Nächste Woche ersetzen wir die Taste A durch eine Kamera mit KI. Was müsste sich im Programm ändern, was bleibt gleich?

## Wenn etwas nicht klappt

| Problem | Lösung |
|---|---|
| „Send to micro:bit“ findet nichts | Chrome oder Edge? Kabel mit Datenleitung? Anderen USB-Anschluss probieren. |
| Fehlermeldung läuft über das Display | Zeilennummer merken. Häufig: Einrückung oder ein vergessenes `:` |
| Kein Ton | Nur der micro:bit **V2** hat einen eingebauten Lautsprecher (steht hinten drauf). |
| Funk geht nicht | Beide dieselbe `GRUPPE`? Beide das Programm neu geladen? |
| Turnier: alle warten ewig | Hat jeder eine **andere** `SPIELER`-Nummer (1, 2, 3)? Alle dieselbe `GRUPPE`? Alle drei haben Taste B gedrückt? Nach 15 Sekunden gibt der micro:bit auf (trauriges Gesicht). |

[Weiter zu Lektion 2: KI im Browser](02-ki.md)
