# Das Material mit GitHub und VS Code holen

Deine Arbeitsdateien (Vorlagen, Programme, Lösungen, Beispiele) liegen in einem eigenen Repo auf GitHub. Du holst es einmal auf deinen Laptop und arbeitest dann direkt in **VS Code**. Die Anleitungen zu den Etappen liest du auf der [Website](https://masta-nksa.github.io/schere-stein-papier/).
Wenn es neue Aufgaben oder Korrekturen gibt, holst du sie mit einem Klick nach.

Das Repo zum Klonen: [github.com/masta-nksa/schere-stein-papier-code](https://github.com/masta-nksa/schere-stein-papier-code)

> **Wörter:** Ein **Repository** (kurz Repo) ist ein Projektordner mit Verlauf. **Klonen** heisst: das Repo auf deinen Laptop kopieren. Ein **Commit** ist ein gespeicherter Zwischenstand. **Pull** heisst: Neues von GitHub holen.

---

## Einmal: Git installieren

VS Code braucht das Programm **Git**, um mit GitHub zu arbeiten.

- **Windows:** Auf [git-scm.com](https://git-scm.com) Git herunterladen und installieren. Bei allen Fragen die vorgeschlagene Einstellung lassen und auf **Next** klicken.
- **Mac:** Das Programm **Terminal** öffnen und `git --version` eintippen. Fehlt Git, bietet der Mac an, die Entwicklerwerkzeuge zu installieren: auf **Installieren** klicken.

Danach **VS Code neu starten**.

**Funktioniert es?**

- [ ] In VS Code im Menü **Terminal → Neues Terminal** öffnen und `git --version` eintippen. Es erscheint eine Versionsnummer, z. B. `git version 2.47.0`.

---

## Einmal: Git einrichten

Git schreibt zu jedem Zwischenstand, wer ihn gemacht hat. Tippe im Terminal von VS Code diese Zeilen ein, eine nach der anderen (mit deinem Vornamen und deiner Schul-Mail):

```bash
git config --global user.name "Vorname"
```

```bash
git config --global user.email "vorname.nachname@schule.ch"
```

Die dritte Zeile sagt Git, dass es beim Holen von Neuem deine Arbeit und die neuen Dateien **zusammenführen** soll. Ohne sie bricht das Holen ab, sobald du eigene Zwischenstände gespeichert hast:

```bash
git config --global pull.rebase false
```

Das bleibt nur auf deinem Laptop. Du lädst nichts zu GitHub hoch.

---

## Einmal: Das Repo klonen

1. Öffne VS Code. Falls ein Ordner offen ist: **Datei → Ordner schliessen**.
2. Klicke links auf das Symbol **Quellcodeverwaltung** (englisch *Source Control*, Tastenkürzel `Ctrl+Shift+G`, auf dem Mac `Cmd+Shift+G`).
3. Klicke auf **Repository klonen** (*Clone Repository*).
4. Füge diese Adresse ein und drücke Enter:
   ```
   https://github.com/masta-nksa/schere-stein-papier-code.git
   ```
5. Wähle einen Ordner auf deinem Laptop, z. B. einen neuen Ordner `Freifach` in deinem Benutzerordner. Nimm möglichst **keinen OneDrive- oder iCloud-Ordner**: Das Synchronisieren kann Git stören.
6. VS Code fragt, ob du das Repo öffnen willst: **Öffnen** (*Open*).
7. Fragt VS Code, ob du den Autoren vertraust: **Ja, ich vertraue den Autoren**.

**Funktioniert es?**

- [ ] Links im **Explorer** siehst du die Ordner `beispiele`, `ki`, `microbit`, `vorlagen` und die Datei `README.md`.
- [ ] Unten links steht `main`.

---

## Arbeiten

- **Etappen lesen:** auf der [Website](https://masta-nksa.github.io/schere-stein-papier/). Dort steht bei jedem Schritt, welche Datei du brauchst.
- **Browser-Seiten (Etappe 2):** Du brauchst die Erweiterung **Live Server**. VS Code schlägt sie beim ersten Öffnen unten rechts vor: **Installieren**. Sonst links auf **Erweiterungen**, nach „Live Server“ suchen und installieren. Dann Rechtsklick auf `index.html` → **Open with Live Server**.
- **Vorlagen bearbeiten:** Du arbeitest direkt in den Dateien, z. B. `ki/01-erkennen/runde.js`. Speichern mit `Ctrl+S`.
- **micro:bit-Programme:** Die `.py`-Datei in VS Code öffnen, alles kopieren und in [python.microbit.org](https://python.microbit.org) einfügen. Dort auf den micro:bit laden.
- **Lösungen:** Liegen gleich daneben, z. B. `ki/01-erkennen/loesung/runde.js` und `microbit/06_ssp_ki.py`. Erst nach einem eigenen Versuch anschauen.

---

## Neues holen (wenn die Lehrperson etwas ergänzt hat)

Bevor du Neues holst, sicherst du deine Arbeit. Sonst weiss Git nicht, was mit deinen Änderungen passieren soll.

1. **Deine Arbeit sichern (Commit):** In der **Quellcodeverwaltung** oben eine Nachricht eintippen, z. B. `meine Arbeit`, und auf **Commit** klicken. Fragt VS Code, ob alle Änderungen übernommen werden sollen: **Ja**.
2. **Neues holen (Pull):** In der Quellcodeverwaltung oben auf **…** (*Weitere Aktionen*) → **Pull** klicken.

**Funktioniert es?**

- [ ] Die neuen Dateien oder Änderungen sind da, und deine eigene Arbeit ist noch da.

**Wichtig:** Drücke **nicht** auf **Änderungen synchronisieren** (*Sync Changes*). Dieser Knopf will deine Arbeit auch zu GitHub hochladen. Das darfst du in diesem Repo nicht, und es kommt eine Fehlermeldung. Deine Arbeit ist trotzdem sicher auf deinem Laptop gespeichert.

---

## Wenn etwas nicht klappt

| Problem | Lösung |
|---|---|
| `git` wird nicht gefunden | Git installiert? Danach VS Code **ganz** schliessen und neu starten. |
| Kein Knopf **Repository klonen** | Ist noch ein Ordner offen? **Datei → Ordner schliessen**. Oder `F1` drücken und `Git: Clone` eintippen. |
| Beim Commit: „Please tell me who you are“ | Name und Mail fehlen. Die Zeilen aus „Git einrichten“ eintippen. |
| Beim Pull: „divergent branches“ oder „Need to specify how to reconcile“ | Die dritte Zeile aus „Git einrichten“ fehlt (`pull.rebase false`). Eintippen und nochmals **Pull**. |
| Beim Pull: Meldung zu **Konflikt** (*Merge Conflict*) | Du und die Lehrperson habt dieselbe Stelle geändert. Melde dich bei der Lehrperson. |
| Fehlermeldung „Permission denied“ oder „403“ | Du hast **Sync Changes** oder **Push** gedrückt. Das ist nicht nötig. Deine Arbeit ist lokal gespeichert. |
| Live Server öffnet eine leere Seite oder Fehler | Hast du den **ganzen Ordner** `schere-stein-papier-code` geöffnet und nicht nur eine Datei? |
| Es geht gar nicht | Notlösung: [Arbeitsordner als ZIP herunterladen](https://github.com/masta-nksa/schere-stein-papier-code/archive/refs/heads/main.zip), entpacken, Ordner in VS Code öffnen. Neues holst du dann aber von Hand. |

## Später in der Projektphase
Für dein eigenes Projekt legst du ein **eigenes Repo** auf GitHub an. Dann kannst du auch hochladen (**Push**) und im Team zusammenarbeiten. Das zeigen wir in der Projektphase.

[Zurück zur Übersicht](../README.md)
