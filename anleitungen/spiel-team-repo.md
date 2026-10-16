# Euer Team-Repo für ein Spiel mit Python

Für die Richtung **Spieleprogrammierung** bekommt dein Team ein eigenes Repo auf GitHub, zum Beispiel `spiel-team-1`.
Darin liegt ein kleines, fertiges Spiel («Sternenfänger») als Startpunkt. Ihr programmiert in Python mit pygame-ce.
Bei jedem **Push** stellt GitHub euer Spiel automatisch online, und alle können es im Browser spielen, auch auf dem Handy.

> **Wörter:** **Push** heisst: deine Zwischenstände (Commits) zu GitHub hochladen. **Pull** heisst: die Zwischenstände der anderen holen.
> Ein **Collaborator** ist eine Person, die in ein Repo hochladen darf.

Git und VS Code hast du schon eingerichtet ([Anleitung](github-vscode.md)). Hier kommt nur dazu, was beim Team-Repo neu ist.

---

## Einmal: Einladung annehmen

Die Lehrperson sagt euch, welches Repo euer Team hat, und lädt alle aus dem Team ein. Dazu braucht sie deinen **GitHub-Namen**.

1. Du bekommst eine E-Mail von GitHub. Klicke auf **View invitation**.
   Oder öffne direkt `https://github.com/masta-nksa/spiel-team-1/invitations` (mit eurer Nummer).
2. Klicke auf **Accept invitation**.

**Funktioniert es?**

- [ ] GitHub zeigt die Meldung, dass du jetzt hochladen darfst (*You now have push access*).

**Wer darf hochladen?** Nur die Personen, die zum Repo eingeladen sind, also euer Team und die Lehrperson. Alle anderen können euer Spiel und den Code **anschauen**, weil das Repo öffentlich ist, aber nichts verändern. Darum: keine Passwörter, Adressen oder Fotos von Personen ins Repo legen.

---

## Einmal: Das Repo klonen

Wie beim Arbeitsordner, nur mit der Adresse eures Team-Repos:

1. In VS Code: **Datei → Ordner schliessen**, dann links **Quellcodeverwaltung** → **Repository klonen**.
2. Adresse einfügen (mit eurer Nummer) und Enter drücken:
   ```
   https://github.com/masta-nksa/spiel-team-1.git
   ```
3. Einen Ordner wählen, wieder **keinen OneDrive- oder iCloud-Ordner**, dann **Öffnen**.

Danach einmal im Terminal von VS Code (**Terminal → Neues Terminal**) die Pakete installieren:

```bash
python -m pip install -r requirements.txt
```

Und das Spiel starten:

```bash
python spiel/main.py
```

**Funktioniert es?**

- [ ] Im Terminal steht beim Start `pygame-ce` und eine Versionsnummer (nicht nur `pygame`).
- [ ] Ein Fenster mit «Sternenfänger» geht auf. Mit Leertaste oder Klick startet das Spiel.
- [ ] Links im Explorer siehst du den Ordner `spiel` und die Datei `README.md`.

Im `README.md` steht, wie das Spiel aufgebaut ist und was ihr zuerst ausbauen könnt.
Wie man so ein Spiel Schritt für Schritt aufbaut, zeigt das [Tutorial: Ein Spiel mit Python entwickeln](../beispiele/sternenfaenger/README.md).

---

## Arbeiten im Team

Jedes Mal, wenn du zu arbeiten beginnst und wenn du aufhörst:

1. **Zuerst Neues holen (Pull):** In der Quellcodeverwaltung auf **…** → **Pull**. So hast du, was die anderen hochgeladen haben.
2. **Arbeiten**, speichern, das Spiel testen.
3. **Commit:** oben eine kurze Nachricht eintippen, was du gemacht hast, z. B. `Gegner springt`, dann **Commit**.
4. **Hochladen (Push):** auf **Änderungen synchronisieren** (*Sync Changes*) klicken. Das macht Pull und Push zusammen.

Beim **ersten Push** fragt VS Code (oder ein Fenster *Connect to GitHub*) nach der Anmeldung: **Zulassen** bzw. **Sign in with your browser**, im Browser bei GitHub anmelden und bestätigen, zurück zu VS Code.

**Tipps fürs Team**

- Oft und in kleinen Schritten committen und pushen, nicht erst am Ende der Lektion.
- Teilt die Arbeit nach **Dateien** auf: Wer an `figuren.py` arbeitet, ändert nicht gleichzeitig dasselbe wie jemand anderes.
- Nur pushen, was läuft. Sonst ist das Spiel auch für die anderen kaputt.

---

## Euer Spiel online

Nach jedem Push baut GitHub das Spiel für den Browser (etwa 1 Minute). Ihr seht das im Repo auf GitHub unter **Actions**:
Ein **grüner Haken** heisst, die neue Version ist online. Ein **rotes Kreuz** heisst, etwas ist schiefgegangen: Klickt darauf und lest die Fehlermeldung.

Euer Spiel läuft unter (mit eurer Nummer):

```
https://masta-nksa.github.io/spiel-team-1/
```

Im Browser dauert der erste Start einige Sekunden. Das ist normal.

**Funktioniert es?**

- [ ] Nach eurem ersten Push zeigt **Actions** einen grünen Haken, und die Seite zeigt eure Änderung.

---

## Wenn etwas nicht klappt

| Problem | Lösung |
|---|---|
| Push: „Permission denied“ oder „403“ | Einladung noch nicht angenommen, oder VS Code ist mit einem anderen GitHub-Konto angemeldet. Links unten auf das Personensymbol klicken und das Konto prüfen. |
| Push: „rejected“ oder „fetch first“ | Jemand hat vorher hochgeladen. Zuerst **Pull**, dann nochmals pushen. |
| Pull: Meldung zu **Konflikt** (*Merge Conflict*) | Zwei Personen haben dieselbe Stelle geändert. VS Code zeigt beide Versionen. Gemeinsam entscheiden, was bleibt, speichern, Commit. Bei Unsicherheit die Lehrperson fragen. |
| Push: „GH007“ oder „private email“ | In GitHub unter **Settings → Emails** die Option *Block command line pushes that expose my email* ausschalten, oder die Lehrperson fragen. |
| `No module named pygame` | Die Pakete fehlen: `python -m pip install -r requirements.txt` |
| „Hier ist das alte pygame installiert“ oder beim Start `pygame 2.6…` statt `pygame-ce` | Das alte pygame stört. Zuerst `python -m pip uninstall -y pygame pygame-ce`, dann `python -m pip install -r requirements.txt` |
| Lokal läuft es, online nicht | Die Regeln für den Browser im `README.md` lesen (z. B. Töne nur als `.ogg`). In **Actions** die Fehlermeldung ansehen. |
| Online nach dem Push noch die alte Version, obwohl **Actions** grün ist | Der Browser merkt sich die Seite bis zu 10 Minuten. Mit `Ctrl+Shift+R` (Mac: `Cmd+Shift+R`) neu laden, die Seite in einem privaten Fenster öffnen oder kurz warten. |

[Zurück zu Etappe 3](../etappen/03-projektstart.md) · [Zurück zur Übersicht](../README.md)
