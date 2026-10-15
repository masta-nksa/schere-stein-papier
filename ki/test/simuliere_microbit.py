"""Simulation der micro:bit-Programme 06_ssp_ki.py und 07_ssp_duell.py (ohne Hardware).

Start:  python ki/test/simuliere_microbit.py
Danach: node ki/test/test-logik.js     (prüft mit dem JS-Parser, ob jede Zeile lesbar ist)

Die micro:bit-Module (microbit, radio, random, uart) werden nachgebaut. Die Zeit läuft SCALE-mal
schneller. Pro Gerät läuft das echte Skript in einem eigenen Thread, dazu ein "Browser", der auf "?"
mit einem vorgegebenen Handzeichen antwortet. Zwischen den Geräten gibt es einen Funk-Äther, der
Nachrichten verlieren oder verspätet zustellen kann.

Nicht simuliert: echte Funk-Laufzeiten, MicroPython-Eigenheiten (Speicher, fehlende Funktionen),
das Verhalten der echten USB-Verbindung.
"""
import builtins
import os
import random as zufallsmodul
import sys
import threading
import time
import traceback
import types

HIER = os.path.dirname(os.path.abspath(__file__))
MICROBIT = os.path.normpath(os.path.join(HIER, "..", "..", "microbit"))
AUSGABE = os.path.join(HIER, "ausgabe-microbit.txt")
SCALE = 5.0                   # 1 echte Sekunde = 5 Sekunden im micro:bit

# soll[ich][gegner]: 1 = ich gewinne, 0 = unentschieden, -1 = ich verliere (0 = Stein, 1 = Papier, 2 = Schere)
SOLL = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]

BILDER_NAMEN = {
    "00000:09990:09990:09990:00000": "STEIN",
    "99999:90009:90009:90009:99999": "PAPIER",
    "99009:99090:00900:99090:99009": "SCHERE",
}

fehler = 0
geprueft = 0
alle_zeilen = []


def pruefe(bedingung, text):
    global fehler, geprueft
    geprueft += 1
    if not bedingung:
        fehler += 1
        print("FEHLER: " + text)


class Stopp(BaseException):
    pass


# ---------- Nachbau der micro:bit-Module ----------

class _ImageMeta(type):
    def __getattr__(cls, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return "Image." + name


class Image(metaclass=_ImageMeta):
    def __init__(self, s):
        self.s = s


def bildname(x):
    if isinstance(x, Image):
        return BILDER_NAMEN.get(x.s, x.s)
    return str(x)


class Aether:
    """Funk zwischen den Geräten: gleiche Gruppe empfängt, Queue-Länge 3, optional Verluste."""

    def __init__(self, verlust=0.0, seed=1):
        self.geraete = []
        self.verlust = verlust
        self.rng = zufallsmodul.Random(seed)
        self.verwerfe_an = {}         # Gerätename -> so viele Nachrichten gehen verloren
        self.lock = threading.Lock()

    def senden(self, von, text):
        with self.lock:
            for g in self.geraete:
                if g is von or g.gruppe != von.gruppe:
                    continue
                if self.verwerfe_an.get(g.name, 0) > 0:
                    self.verwerfe_an[g.name] -= 1
                    continue
                if self.rng.random() < self.verlust:
                    continue
                if len(g.funk_queue) >= 3:      # volle Queue: neue Nachricht geht verloren
                    continue
                g.funk_queue.append(text)


class Geraet:
    def __init__(self, name, skript, aether=None, zufall=(), ids=(), ersetze=(), seed=0):
        self.name = name
        self.skript = skript
        self.aether = aether
        self.zufall = list(zufall)        # Werte für random.randint(0, 2)
        self.ids = list(ids)              # Werte für random.randint(1, 99) (Rundennummern)
        self.ersetze = ersetze
        self.rng = zufallsmodul.Random(seed)
        self.lock = threading.Lock()
        self.gedrueckt_a = False
        self.gedrueckt_b = False
        self.geschuettelt = False         # wird von accelerometer.was_gesture("shake") abgefragt
        self.toene = []                   # music.pitch / music.play
        self.pixel_log = []               # jeder neopixel.show() als Liste der Farben
        self.pixel_pin = None
        self.funk_queue = []
        self.gruppe = 0
        self.rx = bytearray()             # Bytes vom Browser zum micro:bit
        self.tx = bytearray()             # Bytes vom micro:bit zum Browser
        self.zeilen = []                  # alle Zeilen, die der micro:bit geschickt hat
        self.anzeigen = []                # alles, was auf dem Display erschien
        self.antworten = []               # was der "Browser" auf "?" antwortet
        self.ende = 0                     # Anzahl beendeter Runden ("P" oder "X")
        self.fehler = None
        self.stop = False
        self.t0 = time.monotonic()
        self.globs = None
        if aether is not None:
            aether.geraete.append(self)

    # --- Module, die das Skript importiert ---
    def _module(self):
        g = self

        class Anzeige:
            def show(self, x, **kw):
                g.anzeigen.append(bildname(x))

            def scroll(self, x, **kw):
                g.anzeigen.append("scroll:" + str(x))

            def clear(self):
                g.anzeigen.append("clear")

        class Taste:
            def __init__(self, attr):
                self.attr = attr

            def was_pressed(self):
                with g.lock:
                    v = getattr(g, self.attr)
                    setattr(g, self.attr, False)
                return v

        class Uart:
            def init(self, baudrate=9600, **kw):
                g.baud = baudrate

            def any(self):
                return len(g.rx) > 0

            def read(self, n=None):
                with g.lock:
                    daten = bytes(g.rx if n is None else g.rx[:n])
                    del g.rx[:len(daten)]
                return daten or None

            def write(self, d):
                if isinstance(d, str):
                    d = d.encode()
                with g.lock:
                    g.tx.extend(d)
                return len(d)

        class Beschleunigung:
            def was_gesture(self, name):
                assert name in ("up", "down", "left", "right", "face up", "face down", "freefall", "3g", "6g", "8g", "shake")
                if name != "shake":
                    return False
                with g.lock:
                    v = g.geschuettelt
                    g.geschuettelt = False
                return v

        def sleep(ms):
            if g.stop:
                raise Stopp()
            time.sleep(ms / 1000.0 / SCALE)

        mb = types.ModuleType("microbit")
        mb.display = Anzeige()
        mb.button_a = Taste("gedrueckt_a")
        mb.button_b = Taste("gedrueckt_b")
        mb.sleep = sleep
        mb.running_time = lambda: int((time.monotonic() - g.t0) * 1000 * SCALE)
        mb.Image = Image
        mb.uart = Uart()
        mb.accelerometer = Beschleunigung()
        mb.pin1 = "pin1"

        class Radio:
            def config(self, **kw):
                if "group" in kw:
                    g.gruppe = kw["group"]

            def on(self):
                pass

            def off(self):
                pass

            def send(self, text):
                assert isinstance(text, str), "radio.send braucht einen String"
                assert len(text) <= 32, "Funknachricht zu lang"
                if g.aether:
                    g.aether.senden(g, text)

            def receive(self):
                with g.lock:
                    return g.funk_queue.pop(0) if g.funk_queue else None

            def receive_bytes(self):
                t = self.receive()
                return None if t is None else t.encode()

        rd = types.ModuleType("radio")
        r = Radio()
        for n in ("config", "on", "off", "send", "receive", "receive_bytes"):
            setattr(rd, n, getattr(r, n))

        zu = types.ModuleType("random")

        def randint(a, b):
            if (a, b) == (0, 2) and g.zufall:
                return g.zufall.pop(0)
            if (a, b) == (1, 99) and g.ids:
                return g.ids.pop(0)
            return g.rng.randint(a, b)
        zu.randint = randint

        mu = types.ModuleType("music")
        mu.__getattr__ = lambda name: "music." + name                  # music.BA_DING usw.
        mu.pitch = lambda freq, duration=-1, pin="pin0", wait=True: g.toene.append(("pitch", freq))
        mu.play = lambda melodie, pin="pin0", wait=True, loop=False: g.toene.append(("play", melodie))

        neo = types.ModuleType("neopixel")

        class NeoPixel:
            def __init__(self, pin, n, bpp=3):
                g.pixel_pin = pin
                self.p = [(0, 0, 0)] * n

            def __setitem__(self, i, farbe):
                assert len(farbe) == 3 and all(0 <= c <= 255 for c in farbe), "Farbe muss (r, g, b) mit 0..255 sein"
                self.p[i] = tuple(farbe)

            def __getitem__(self, i):
                return self.p[i]

            def show(self):
                g.pixel_log.append(list(self.p))
        neo.NeoPixel = NeoPixel

        return {"microbit": mb, "radio": rd, "random": zu, "music": mu, "neopixel": neo}

    def starten(self):
        with open(os.path.join(MICROBIT, self.skript), encoding="utf-8") as f:
            quelle = f.read()
        for alt, neu in self.ersetze:
            assert alt in quelle, "Ersetzung nicht gefunden: " + alt
            quelle = quelle.replace(alt, neu)
        module = self._module()
        eingebaut = dict(builtins.__dict__)
        echt = builtins.__import__

        def imp(name, *a, **k):
            return module[name] if name in module else echt(name, *a, **k)
        eingebaut["__import__"] = imp
        self.globs = {"__builtins__": eingebaut, "__name__": "__main__"}
        code = compile(quelle, self.skript, "exec")

        def lauf():
            try:
                exec(code, self.globs)
            except Stopp:
                pass
            except BaseException as e:      # noqa: B902
                self.fehler = e
                traceback.print_exc()
        self.thread = threading.Thread(target=lauf, daemon=True)
        self.browser_thread = threading.Thread(target=self._browser, daemon=True)
        self.thread.start()
        self.browser_thread.start()

    def beenden(self):
        self.stop = True
        self.thread.join(2)
        self.browser_thread.join(2)

    # --- der "Browser" am anderen Ende des USB-Kabels ---
    def _browser(self):
        rest = b""
        while not self.stop:
            time.sleep(0.002)
            with self.lock:
                daten = bytes(self.tx)
                self.tx.clear()
            rest += daten
            while b"\n" in rest:
                zeile, rest = rest.split(b"\n", 1)
                z = zeile.decode().strip()
                self.zeilen.append(z)
                alle_zeilen.append(z)
                if z == "?":
                    self._antworte()
                elif z.startswith("P ") or z == "X":
                    self.ende += 1

    def _antworte(self):
        a = self.antworten.pop(0) if self.antworten else None
        time.sleep(0.01)                       # Rechenzeit des Browsers
        if a is None:
            return                             # Browser antwortet nicht
        if isinstance(a, tuple):               # ("roh", [Stück, Stück]): Antwort in Teilen
            for stueck in a[1]:
                with self.lock:
                    self.rx.extend(stueck)
                time.sleep(0.01)
            return
        text = "G-\n" if a == "-" else "G%d\n" % a
        with self.lock:
            self.rx.extend(text.encode())

    def ergebnisse(self):
        return [z for z in self.zeilen if z.startswith("R ")]

    def anzahl_countdown(self):
        return len([z for z in self.zeilen if z.startswith("C")])


def warte(bedingung, timeout=15.0):
    ende = time.monotonic() + timeout
    while time.monotonic() < ende:
        if bedingung():
            return True
        time.sleep(0.005)
    return False


def runde(geraete, druecker, nachlauf=0.7):
    """Taste A bei den `druecker` drücken und warten, bis alle `geraete` die Runde beendet haben."""
    vor = [g.ende for g in geraete]
    for d in druecker:
        d.gedrueckt_a = True
    ok = warte(lambda: all(g.ende > v for g, v in zip(geraete, vor)))
    time.sleep(nachlauf)                       # Anzeige und Funk aufräumen lassen
    return ok


def kein_absturz(geraete, wo):
    for g in geraete:
        pruefe(g.fehler is None, wo + ": Gerät " + g.name + " ist abgestürzt: " + repr(g.fehler))


def neues_duell(verlust=0.0, seed=0, ids_a=(), ids_b=()):
    ae = Aether(verlust, seed)
    a = Geraet("A", "07_ssp_duell.py", ae, ids=ids_a, seed=seed * 2 + 1)
    b = Geraet("B", "07_ssp_duell.py", ae, ids=ids_b, seed=seed * 2 + 2)
    a.starten()
    b.starten()
    time.sleep(0.1)
    return ae, a, b


# ---------- Szenarien ----------

def test_ki_alle_kombinationen():
    print("06: alle 9 Kombinationen")
    m = Geraet("M", "06_ssp_ki.py")
    m.starten()
    time.sleep(0.1)
    punkte = [0, 0]
    for g in range(3):
        for c in range(3):
            m.zufall.append(c)
            m.antworten.append(g)
            ok = runde([m], [m])
            pruefe(ok, "06: Runde %d/%d nicht beendet" % (g, c))
            e = SOLL[g][c]
            pruefe(m.ergebnisse() and m.ergebnisse()[-1] == "R %d %d %d" % (g, c, e),
                   "06: Ergebnis falsch für du=%d micro:bit=%d: %s" % (g, c, m.ergebnisse()[-1:]))
            if e == 1:
                punkte[0] += 1
            elif e == -1:
                punkte[1] += 1
            pruefe(m.zeilen[-1] == "P %d %d" % tuple(punkte), "06: Punkte falsch: " + m.zeilen[-1])
    pruefe(m.zeilen[:4] == ["C3", "C2", "C1", "?"], "06: Beginn der Runde: " + str(m.zeilen[:4]))
    kein_absturz([m], "06 Kombinationen")
    m.beenden()


def test_ki_sonderfaelle():
    print("06: unsicher, keine Antwort, alte und kaputte Daten")
    m = Geraet("M", "06_ssp_ki.py")
    m.starten()
    time.sleep(0.1)

    # nicht sicher erkannt -> Runde zählt nicht
    m.antworten.append("-")
    runde([m], [m])
    pruefe(m.zeilen[-1] == "X", "06: 'G-' soll X ergeben: " + m.zeilen[-1])
    pruefe("Image.CONFUSED" in m.anzeigen, "06: bei 'G-' soll Image.CONFUSED erscheinen")
    pruefe(not m.ergebnisse(), "06: bei 'G-' darf es kein R geben")

    # Browser antwortet nicht
    m.antworten.append(None)
    runde([m], [m], nachlauf=0.3)
    pruefe(m.zeilen[-1] == "X", "06: keine Antwort soll X ergeben: " + m.zeilen[-1])
    pruefe("scroll:Browser?" in m.anzeigen, "06: bei keiner Antwort soll 'Browser?' erscheinen")

    # alte Antwort im Puffer und Müll werden weggeworfen, Antwort in Stücken mit \r\n funktioniert
    m.rx.extend(b"G2\n\xff\xfeblabla\n")
    m.zufall.append(2)
    m.antworten.append(("roh", [b"G", b"1\r", b"\n"]))
    runde([m], [m])
    pruefe(m.ergebnisse() and m.ergebnisse()[-1] == "R 1 2 %d" % SOLL[1][2],
           "06: alte Daten dürfen nicht zählen: " + str(m.ergebnisse()[-1:]))

    # ungültige Antworten werden ignoriert, danach kommt die richtige
    m.zufall.append(0)
    m.antworten.append(("roh", [b"G7\nHallo\nG\n", b"G2\n"]))
    runde([m], [m])
    pruefe(m.ergebnisse()[-1] == "R 2 0 %d" % SOLL[2][0], "06: ungültige Zeilen ignorieren: " + m.ergebnisse()[-1])

    # B setzt die Punkte zurück
    m.gedrueckt_b = True
    warte(lambda: m.zeilen[-1] == "P 0 0", 2)
    pruefe(m.zeilen[-1] == "P 0 0", "06: Taste B soll 'P 0 0' schicken")
    kein_absturz([m], "06 Sonderfälle")
    m.beenden()


def test_ki_hardware():
    print("06: Ton, Schütteln und Neopixel-Ampel")
    m = Geraet("M", "06_ssp_ki.py", ersetze=(("N_PIXEL = 0", "N_PIXEL = 8"),))
    m.starten()
    time.sleep(0.1)
    pruefe(m.pixel_pin == "pin1", "06: Neopixel gehören an Pin 1 (Pin 0 braucht der Ton): " + str(m.pixel_pin))
    gelb = (40, 40, 0)
    faelle = [(1, 0, (0, 40, 0), ("play", "music.BA_DING")),      # du gewinnst: grün
              (0, 1, (40, 0, 0), ("play", "music.WAWAWAWAA")),    # du verlierst: rot
              (2, 2, (40, 20, 0), None)]                          # unentschieden: orange
    for g, c, farbe, melodie in faelle:
        m.pixel_log.clear()
        m.toene.clear()
        m.zufall.append(c)
        m.antworten.append(g)
        runde([m], [m])
        anzahl_gelb = [sum(1 for p in bild if p == gelb) for bild in m.pixel_log[:3]]
        pruefe(anzahl_gelb == [3, 2, 1], "06: Countdown soll 3, 2, 1 Neopixel gelb zeigen: " + str(anzahl_gelb))
        pruefe(m.pixel_log[-1] == [farbe] * 8, "06: Endfarbe für du=%d/micro:bit=%d: %s" % (g, c, m.pixel_log[-1]))
        pruefe([t for t in m.toene if t[0] == "pitch"] == [("pitch", 440)] * 3, "06: 3 Töne beim Countdown: " + str(m.toene))
        pruefe((melodie is None) or (melodie in m.toene), "06: Melodie fehlt: " + str(m.toene))
    # nicht sicher: blau
    m.pixel_log.clear()
    m.antworten.append("-")
    runde([m], [m])
    pruefe(m.pixel_log[-1] == [(0, 0, 40)] * 8, "06: bei X blau: " + str(m.pixel_log[-1]))
    # Taste B löscht die Ampel
    m.gedrueckt_b = True
    warte(lambda: m.zeilen[-1] == "P 0 0", 2)
    time.sleep(0.2)
    pruefe(m.pixel_log[-1] == [(0, 0, 0)] * 8, "06: Taste B löscht die Ampel")
    kein_absturz([m], "06 Hardware")
    m.beenden()

    print("06: Schütteln startet die Runde")
    m = Geraet("M", "06_ssp_ki.py")
    m.starten()
    time.sleep(0.1)
    m.antworten.append(2)
    m.zufall.append(1)
    vor = m.ende
    m.geschuettelt = True
    warte(lambda: m.ende > vor)
    time.sleep(0.7)
    pruefe(m.ergebnisse() and m.ergebnisse()[-1] == "R 2 1 1", "06: Schütteln soll eine Runde starten: " + str(m.ergebnisse()))
    # Schütteln während der Runde darf keine zweite Runde auslösen
    m.antworten.extend([0, 0])
    m.zufall.extend([0, 0])
    anzahl_c = m.anzahl_countdown()
    vor = m.ende
    m.geschuettelt = True
    time.sleep(0.5)
    m.geschuettelt = True                      # mitten im Countdown nochmals schütteln
    warte(lambda: m.ende > vor)
    time.sleep(1.0)
    pruefe(m.anzahl_countdown() == anzahl_c + 3, "06: genau eine weitere Runde, nicht zwei: %d statt %d" % (m.anzahl_countdown(), anzahl_c + 3))
    kein_absturz([m], "06 Schütteln")
    m.beenden()


def test_vorlage():
    print("06: Vorlage läuft ohne Absturz (mit leeren TODOs)")
    m = Geraet("M", "06_ssp_ki_vorlage.py")
    m.starten()
    time.sleep(0.1)
    m.antworten.append(1)
    m.gedrueckt_a = True
    time.sleep(1.5)
    pruefe(m.zeilen[:1] == ["?"], "Vorlage: ohne TODO 1 kommt sofort '?': " + str(m.zeilen[:3]))
    pruefe(m.fehler is None, "Vorlage: Absturz: " + repr(m.fehler))
    kein_absturz([m], "Vorlage")
    m.beenden()


def test_duell_alle_kombinationen():
    print("07: alle 9 Kombinationen (verlustfreier Funk)")
    ae, a, b = neues_duell()
    punkte_a = [0, 0]
    punkte_b = [0, 0]
    n = 0
    for ga in range(3):
        for gb in range(3):
            a.antworten.append(ga)
            b.antworten.append(gb)
            ok = runde([a, b], [a] if n % 2 == 0 else [b])
            n += 1
            pruefe(ok, "07: Runde %d/%d nicht beendet" % (ga, gb))
            ea = SOLL[ga][gb]
            pruefe(a.ergebnisse() and a.ergebnisse()[-1] == "R %d %d %d" % (ga, gb, ea),
                   "07: A falsch bei %d/%d: %s" % (ga, gb, a.ergebnisse()[-1:]))
            pruefe(b.ergebnisse() and b.ergebnisse()[-1] == "R %d %d %d" % (gb, ga, -ea),
                   "07: B falsch bei %d/%d: %s" % (gb, ga, b.ergebnisse()[-1:]))
            for p, e in ((punkte_a, ea), (punkte_b, -ea)):
                if e == 1:
                    p[0] += 1
                elif e == -1:
                    p[1] += 1
            pruefe(a.zeilen[-1] == "P %d %d" % tuple(punkte_a), "07: Punkte A: " + a.zeilen[-1])
            pruefe(b.zeilen[-1] == "P %d %d" % tuple(punkte_b), "07: Punkte B: " + b.zeilen[-1])
    pruefe(a.zeilen[:4] == ["C3", "C2", "C1", "?"], "07: A beginnt mit " + str(a.zeilen[:4]))
    pruefe(b.zeilen[:4] == ["C3", "C2", "C1", "?"], "07: B beginnt mit " + str(b.zeilen[:4]))
    kein_absturz([a, b], "07 Kombinationen")
    a.beenden()
    b.beenden()


def test_duell_unsicher_und_stumm():
    print("07: unsicheres Handzeichen und stummer Browser")
    ae, a, b = neues_duell()
    # A unsicher -> beide wiederholen
    a.antworten.append("-")
    b.antworten.append(1)
    runde([a, b], [a])
    pruefe(a.zeilen[-1] == "X" and b.zeilen[-1] == "X", "07: beide sollen X melden: %s / %s" % (a.zeilen[-1], b.zeilen[-1]))
    pruefe("Image.CONFUSED" in a.anzeigen and "Image.CONFUSED" in b.anzeigen, "07: beide zeigen CONFUSED")
    pruefe(not a.ergebnisse() and not b.ergebnisse(), "07: unsichere Runde darf kein R ergeben")
    # B unsicher
    a.antworten.append(0)
    b.antworten.append("-")
    runde([a, b], [b])
    pruefe(a.zeilen[-1] == "X" and b.zeilen[-1] == "X", "07: (B unsicher) beide X")
    # Browser von A antwortet nicht
    a.antworten.append(None)
    b.antworten.append(2)
    runde([a, b], [a])
    pruefe(a.zeilen[-1] == "X" and b.zeilen[-1] == "X", "07: (A stumm) beide X")
    pruefe("scroll:Browser?" in a.anzeigen, "07: A zeigt 'Browser?'")
    # danach funktioniert eine normale Runde
    a.antworten.append(2)
    b.antworten.append(1)
    runde([a, b], [a])
    pruefe(a.ergebnisse()[-1] == "R 2 1 1" and b.ergebnisse()[-1] == "R 1 2 -1", "07: normale Runde nach Abbrüchen")
    kein_absturz([a, b], "07 unsicher")
    a.beenden()
    b.beenden()


def test_duell_alte_nachrichten():
    print("07: alte, verspätete und kaputte Funknachrichten")
    ae, a, b = neues_duell()

    # 1) alte Handzeichen anderer Runden liegen schon in der Queue
    for g in (a, b):
        g.funk_queue.extend(["G,55,2", "G,56,0", "G,57,2"])
    a.antworten.append(0)
    b.antworten.append(1)

    # 2) während des Countdowns und während des Wartens kommen weitere alte Nachrichten
    def stoeren():
        time.sleep(0.15)
        for g in (a, b):
            g.funk_queue.append("G,58,2")
        time.sleep(0.4)
        for g in (a, b):
            g.funk_queue.append("G,59,0")
    t = threading.Thread(target=stoeren)
    t.start()
    runde([a, b], [a])
    t.join()
    pruefe(a.ergebnisse() and a.ergebnisse()[-1] == "R 0 1 -1", "07: A darf alte G nicht benutzen: " + str(a.ergebnisse()[-1:]))
    pruefe(b.ergebnisse() and b.ergebnisse()[-1] == "R 1 0 1", "07: B darf alte G nicht benutzen: " + str(b.ergebnisse()[-1:]))

    # 3) Wiederholung der Startnachricht der soeben gespielten Runde startet keine neue Runde
    rid_a = a.globs["letzte_runde"]
    rid_b = b.globs["letzte_runde"]
    pruefe(rid_a == rid_b, "07: beide haben dieselbe Rundennummer")
    c_vorher = a.anzahl_countdown(), b.anzahl_countdown()
    for g in (a, b):
        g.funk_queue.append("S,%d,1" % rid_a)
        g.funk_queue.append("S,%d,2" % rid_a)
    time.sleep(0.8)
    pruefe((a.anzahl_countdown(), b.anzahl_countdown()) == c_vorher, "07: alter Start darf keine Runde auslösen")

    # 4) kaputte Nachrichten stören nicht (auch nicht im Leerlauf)
    for text in ["", "hallo", "S,abc,3", "S,5,9", "G,5,7", "S,1,2,3", "G,,1", "S,4", "äö"]:
        for g in (a, b):
            g.funk_queue.append(text)
        time.sleep(0.05)
    time.sleep(0.5)
    pruefe((a.anzahl_countdown(), b.anzahl_countdown()) == c_vorher, "07: kaputte Nachrichten lösen keine Runde aus")

    # 5) danach läuft eine normale Runde richtig
    a.antworten.append(2)
    b.antworten.append(2)
    runde([a, b], [b])
    pruefe(a.ergebnisse()[-1] == "R 2 2 0" and b.ergebnisse()[-1] == "R 2 2 0", "07: Unentschieden nach Störungen")
    kein_absturz([a, b], "07 alte Nachrichten")
    a.beenden()
    b.beenden()


def test_duell_gleichzeitiger_start():
    print("07: beide drücken Taste A gleichzeitig")
    for ids_a, ids_b in (([10], [20]), ([20], [10]), ([15], [15])):
        ae, a, b = neues_duell(ids_a=ids_a, ids_b=ids_b)
        a.antworten.append(1)
        b.antworten.append(2)
        ok = runde([a, b], [a, b])
        pruefe(ok, "07: gleichzeitiger Start %s/%s nicht beendet" % (ids_a, ids_b))
        pruefe(a.ergebnisse() and a.ergebnisse()[-1] == "R 1 2 -1", "07: A bei gleichzeitigem Start %s/%s: %s" % (ids_a, ids_b, a.ergebnisse()[-1:]))
        pruefe(b.ergebnisse() and b.ergebnisse()[-1] == "R 2 1 1", "07: B bei gleichzeitigem Start %s/%s: %s" % (ids_a, ids_b, b.ergebnisse()[-1:]))
        pruefe(a.globs["letzte_runde"] == b.globs["letzte_runde"], "07: gleiche Rundennummer nach gleichzeitigem Start")
        pruefe(a.anzahl_countdown() == 3 and b.anzahl_countdown() == 3, "07: genau eine Runde gespielt")
        kein_absturz([a, b], "07 gleichzeitig")
        a.beenden()
        b.beenden()


def test_duell_spaeter_einstieg():
    print("07: erste Startnachrichten gehen verloren")
    for verloren in (1, 2):
        ae, a, b = neues_duell()
        ae.verwerfe_an["B"] = verloren
        a.antworten.append(0)
        b.antworten.append(2)
        ok = runde([a, b], [a])
        pruefe(ok, "07: Einstieg nach %d verlorenen Starts: nicht beendet" % verloren)
        pruefe(a.ergebnisse() and a.ergebnisse()[-1] == "R 0 2 1", "07: A nach %d verlorenen Starts: %s" % (verloren, a.ergebnisse()[-1:]))
        pruefe(b.ergebnisse() and b.ergebnisse()[-1] == "R 2 0 -1", "07: B nach %d verlorenen Starts: %s" % (verloren, b.ergebnisse()[-1:]))
        kein_absturz([a, b], "07 später Einstieg")
        a.beenden()
        b.beenden()


def test_duell_andere_gruppe():
    print("07: ein Paar in einer anderen Gruppe wird nicht gestört")
    ae = Aether()
    a = Geraet("A", "07_ssp_duell.py", ae, seed=1)
    b = Geraet("B", "07_ssp_duell.py", ae, seed=2)
    c = Geraet("C", "07_ssp_duell.py", ae, ersetze=(("GRUPPE = 7", "GRUPPE = 8"),), seed=3)
    for g in (a, b, c):
        g.starten()
    time.sleep(0.1)
    a.antworten.append(1)
    b.antworten.append(0)
    runde([a, b], [a])
    pruefe(a.ergebnisse()[-1] == "R 1 0 1", "07: Paar in Gruppe 7 spielt richtig")
    pruefe(c.anzahl_countdown() == 0 and c.gruppe == 8, "07: Gerät in Gruppe 8 bleibt unberührt")
    kein_absturz([a, b, c], "07 Gruppen")
    for g in (a, b, c):
        g.beenden()


def test_duell_funkverlust():
    print("07: Funk verliert Nachrichten (30 %)")
    zahlen = {"beide R": 0, "beide X": 0, "gemischt": 0}
    for seed in (1, 2, 3, 4):
        ae, a, b = neues_duell(verlust=0.3, seed=seed)
        for i in range(3):
            ga, gb = (seed + i) % 3, (seed * 2 + i) % 3
            a.antworten[:] = []          # Reste einer abgebrochenen Runde (z. B. Start nie angekommen)
            b.antworten[:] = []
            a.antworten.append(ga)
            b.antworten.append(gb)
            ra, rb = len(a.ergebnisse()), len(b.ergebnisse())
            runde([a, b], [a], nachlauf=0.8)
            neu_a, neu_b = len(a.ergebnisse()) > ra, len(b.ergebnisse()) > rb
            if neu_a and neu_b:
                zahlen["beide R"] += 1
                pruefe(a.ergebnisse()[-1] == "R %d %d %d" % (ga, gb, SOLL[ga][gb]), "07 Verlust: A falsch: " + a.ergebnisse()[-1])
                pruefe(b.ergebnisse()[-1] == "R %d %d %d" % (gb, ga, SOLL[gb][ga]), "07 Verlust: B falsch: " + b.ergebnisse()[-1])
            elif not neu_a and not neu_b:
                zahlen["beide X"] += 1
            else:
                zahlen["gemischt"] += 1
        kein_absturz([a, b], "07 Funkverlust")
        a.beenden()
        b.beenden()
    print("   Ergebnis bei 30 %% Verlust: %s" % zahlen)
    pruefe(zahlen["beide R"] >= 8, "07 Verlust: die meisten Runden sollen trotz Verlusten klappen")
    # Eine Runde, in der nur eine Seite ein Resultat hat, ist möglich (Funk hat keine Bestätigung), soll aber selten sein.
    pruefe(zahlen["gemischt"] <= 1, "07 Verlust: zu viele einseitige Runden: %s" % zahlen)


# ---------- Lektion 1: Reaktionsspiel und Turnier ----------

def test_reaktion():
    print("08: Reaktionsspiel")
    m = Geraet("M", "08_reaktion.py")
    m.starten()
    time.sleep(0.1)

    # zu früh gedrückt
    m.gedrueckt_a = True
    time.sleep(0.15)
    m.gedrueckt_b = True
    time.sleep(0.5)
    pruefe("Image.SAD" in m.anzeigen, "08: zu früh soll Image.SAD zeigen: " + str(m.anzeigen[-5:]))
    pruefe(("play", "music.WAWAWAWAA") in m.toene, "08: zu früh soll WAWAWAWAA spielen")
    pruefe(not any(a.endswith("ms") or "Rekord" in a for a in m.anzeigen), "08: zu früh darf keine Zeit zeigen")
    time.sleep(1.0)

    # erste Runde: Rekord, zweite Runde langsamer: kein Rekord
    zeiten = []
    for reaktion_s, erwartet_rekord in ((0.06, True), (0.25, False)):
        m.anzeigen.clear()
        m.gedrueckt_a = True
        ok = warte(lambda: any(a.startswith("99999:99999") for a in m.anzeigen), 6)
        pruefe(ok, "08: das Display soll nach der Wartezeit aufleuchten")
        time.sleep(reaktion_s)
        m.gedrueckt_b = True
        warte(lambda: any(a.startswith("scroll:") and "ms" in a for a in m.anzeigen), 3)
        text = [a for a in m.anzeigen if a.startswith("scroll:")]
        pruefe(len(text) == 1, "08: genau eine Anzeige der Zeit: " + str(text))
        if text:
            zahl = int(text[0].split(":")[1].split(" ")[0])
            zeiten.append(zahl)
            pruefe(text[0].endswith("Rekord!") == erwartet_rekord, "08: Rekord-Anzeige falsch: " + text[0])
        time.sleep(0.3)
    # 0.06 s echt = ca. 300 ms im micro:bit, 0.25 s echt = ca. 1250 ms
    pruefe(len(zeiten) == 2 and 150 < zeiten[0] < 800, "08: gemessene Zeit 1 unplausibel: " + str(zeiten))
    pruefe(len(zeiten) == 2 and 800 < zeiten[1] < 2500, "08: gemessene Zeit 2 unplausibel: " + str(zeiten))
    kein_absturz([m], "08 Reaktion")
    m.beenden()


def tipp_wahl(g, ziel):
    """Taste A so oft drücken, bis die Wahl von Gerät g = ziel ist."""
    while g.globs["wahl"] != ziel:
        g.gedrueckt_a = True
        warte(lambda: not g.gedrueckt_a, 2)
        time.sleep(0.02)


def neues_turnier(verlust=0.0, seed=0):
    ae = Aether(verlust, seed)
    geraete = []
    for i in (1, 2, 3):
        geraete.append(Geraet("S%d" % i, "09_ssp_turnier.py", ae, ersetze=(("SPIELER = 1", "SPIELER = %d" % i),), seed=seed * 3 + i))
    for g in geraete:
        g.starten()
    time.sleep(0.1)
    return ae, geraete


def turnier_runde(geraete, wahlen, spaet=None, nachlauf=0.9):
    """Alle wählen und drücken B. spaet = (Index, Sekunden): dieser Spieler drückt B später."""
    for g, w in zip(geraete, wahlen):
        tipp_wahl(g, w)
    vor = [g.globs["runde"] for g in geraete]
    for i, g in enumerate(geraete):
        if spaet and spaet[0] == i:
            threading.Timer(spaet[1], lambda g=g: setattr(g, "gedrueckt_b", True)).start()
        else:
            g.gedrueckt_b = True
    ok = warte(lambda: all(g.globs["runde"] > v for g, v in zip(geraete, vor)), 25)
    time.sleep(nachlauf)
    return ok


def erwartete_punkte(wahlen):
    return [sum(1 for j in range(3) if j != i and SOLL[wahlen[i]][wahlen[j]] == 1) for i in range(3)]


def test_turnier_alle_kombinationen():
    print("09: Turnier zu dritt, alle 27 Kombinationen")
    ae, geraete = neues_turnier()
    total = [0, 0, 0]
    for w1 in range(3):
        for w2 in range(3):
            for w3 in range(3):
                wahlen = [w1, w2, w3]
                ok = turnier_runde(geraete, wahlen)
                pruefe(ok, "09: Runde %s nicht beendet" % wahlen)
                for i, p in enumerate(erwartete_punkte(wahlen)):
                    total[i] += p
                ist = [g.globs["punkte"] for g in geraete]
                pruefe(ist == total, "09: Punkte nach %s: ist %s, soll %s" % (wahlen, ist, total))
    pruefe(len(set(g.globs["runde"] for g in geraete)) == 1, "09: alle in derselben Runde")
    kein_absturz(geraete, "09 Kombinationen")
    for g in geraete:
        g.beenden()


def test_turnier_stoerungen():
    print("09: Turnier: später Spieler, fehlender Spieler, alte und kaputte Nachrichten")
    ae, geraete = neues_turnier()
    # einer drückt erst 1,5 s (echt) später
    ok = turnier_runde(geraete, [0, 1, 2], spaet=(2, 0.8))
    pruefe(ok and [g.globs["punkte"] for g in geraete] == erwartete_punkte([0, 1, 2]), "09: später Spieler: " + str([g.globs["punkte"] for g in geraete]))
    punkte = [g.globs["punkte"] for g in geraete]

    # alte und kaputte Nachrichten liegen schon in der Queue
    geraete[0].funk_queue.extend(["2,0,0", "3,0,1", "hallo"])
    geraete[1].funk_queue.extend(["1,0,2", "", "9,9,9"])
    ok = turnier_runde(geraete, [2, 2, 1])
    soll = erwartete_punkte([2, 2, 1])
    punkte = [p + s for p, s in zip(punkte, soll)]
    pruefe(ok and [g.globs["punkte"] for g in geraete] == punkte, "09: alte Nachrichten: %s statt %s" % ([g.globs["punkte"] for g in geraete], punkte))

    # Spieler 3 fehlt: die anderen zeigen nach der Wartezeit ein trauriges Gesicht
    vor_runden = [g.globs["runde"] for g in geraete]
    tipp_wahl(geraete[0], 1)
    tipp_wahl(geraete[1], 0)
    geraete[0].gedrueckt_b = True
    geraete[1].gedrueckt_b = True
    warte(lambda: geraete[0].globs["runde"] > vor_runden[0] and geraete[1].globs["runde"] > vor_runden[1], 30)
    time.sleep(0.6)
    pruefe("Image.SAD" in geraete[0].anzeigen and "Image.SAD" in geraete[1].anzeigen, "09: ohne dritten Spieler soll SAD erscheinen")
    pruefe([g.globs["punkte"] for g in geraete] == punkte, "09: Timeout gibt keine Punkte")
    # Runden sind jetzt nicht mehr gleich (der dritte hat nicht mitgezählt): trotzdem soll die nächste Runde klappen
    pruefe(geraete[2].globs["runde"] != geraete[0].globs["runde"], "09: Test-Annahme: Rundennummern sind verschieden")
    ok = turnier_runde(geraete, [0, 2, 1])
    punkte = [p + s for p, s in zip(punkte, erwartete_punkte([0, 2, 1]))]
    pruefe(ok and [g.globs["punkte"] for g in geraete] == punkte, "09: Wiedereinstieg nach Rundenunterschied: %s statt %s" % ([g.globs["punkte"] for g in geraete], punkte))
    pruefe(len(set(g.globs["runde"] for g in geraete)) == 1, "09: danach wieder alle in derselben Runde")
    kein_absturz(geraete, "09 Störungen")
    for g in geraete:
        g.beenden()


def test_turnier_funkverlust():
    print("09: Turnier mit Funkverlust (30 %)")
    gut = schlecht = 0
    for seed in (1, 2):
        ae, geraete = neues_turnier(verlust=0.3, seed=seed)
        for i in range(3):
            wahlen = [(seed + i) % 3, (seed * 2 + i + 1) % 3, (i * 2 + seed) % 3]
            vor = [g.globs["punkte"] for g in geraete]
            turnier_runde(geraete, wahlen, nachlauf=1.2)
            neu = [g.globs["punkte"] - v for g, v in zip(geraete, vor)]
            if neu == erwartete_punkte(wahlen):
                gut += 1
            elif neu == [0, 0, 0]:
                schlecht += 1
            else:
                pruefe(False, "09 Verlust: falsche Punkte %s für %s (soll %s)" % (neu, wahlen, erwartete_punkte(wahlen)))
        kein_absturz(geraete, "09 Funkverlust")
        for g in geraete:
            g.beenden()
    print("   Ergebnis bei 30 %% Verlust: %d richtig, %d ohne Ergebnis" % (gut, schlecht))
    pruefe(gut >= 4, "09 Verlust: die meisten Runden sollen trotz Verlusten klappen")


if __name__ == "__main__":
    t_start = time.time()
    test_ki_alle_kombinationen()
    test_ki_sonderfaelle()
    test_ki_hardware()
    test_vorlage()
    test_duell_alle_kombinationen()
    test_duell_unsicher_und_stumm()
    test_duell_alte_nachrichten()
    test_duell_gleichzeitiger_start()
    test_duell_spaeter_einstieg()
    test_duell_andere_gruppe()
    test_duell_funkverlust()
    test_reaktion()
    test_turnier_alle_kombinationen()
    test_turnier_stoerungen()
    test_turnier_funkverlust()
    with open(AUSGABE, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(set(alle_zeilen))) + "\n")
    print("%d Prüfungen, %d Fehler (%.0f s)." % (geprueft, fehler, time.time() - t_start))
    sys.exit(1 if fehler else 0)
