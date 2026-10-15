// Testskript für ki/gemeinsam/logik.js (Spiellogik und Protokoll-Parser)
// Start: node ki/test/test-logik.js
// Wenn ki/test/ausgabe-microbit.txt existiert (von simuliere_microbit.py erzeugt), werden auch
// alle Zeilen daraus mit dem Parser geprüft.
const fs = require('fs');
const path = require('path');
const L = require('../gemeinsam/logik.js');

let fehler = 0, geprueft = 0;
function pruefe(bedingung, text) {
  geprueft++;
  if (!bedingung) { fehler++; console.log('FEHLER: ' + text); }
}
function gleich(ist, soll, text) {
  pruefe(JSON.stringify(ist) === JSON.stringify(soll), text + ' (ist ' + JSON.stringify(ist) + ', soll ' + JSON.stringify(soll) + ')');
}

// ---- 1. Alle 9 Kombinationen (0 = Stein, 1 = Papier, 2 = Schere) ----
const soll = [   // soll[ich][gegner]
  [0, -1, 1],    // Stein: gegen Stein =, gegen Papier verloren, gegen Schere gewonnen
  [1, 0, -1],    // Papier
  [-1, 1, 0],    // Schere
];
for (let i = 0; i < 3; i++) for (let g = 0; g < 3; g++) {
  gleich(L.ergebnis(i, g), soll[i][g], 'ergebnis(' + L.NAMEN[i] + ', ' + L.NAMEN[g] + ')');
}

// ---- 2. Erkennung: häufigstes Handzeichen der letzten 500 ms ----
function serie(klasse, p, von, bis, schritt = 50) {
  const l = [];
  for (let t = von; t <= bis; t += schritt) l.push({ t, klasse, p });
  return l;
}
const jetzt = 10000;
gleich(L.entscheide(serie('stein', 0.95, 9500, 10000), jetzt), 0, 'klar Stein');
gleich(L.entscheide(serie('papier', 0.95, 9500, 10000), jetzt), 1, 'klar Papier');
gleich(L.entscheide(serie('schere', 0.95, 9500, 10000), jetzt), 2, 'klar Schere');
gleich(L.entscheide(serie('nichts', 0.99, 9500, 10000), jetzt), null, 'nichts = nicht sicher');
gleich(L.entscheide([], jetzt), null, 'keine Bilder');
gleich(L.entscheide(serie('stein', 0.6, 9500, 10000), jetzt), null, 'alles unter der Schwelle');
gleich(L.entscheide(serie('stein', 0.8, 9500, 10000), jetzt), 0, 'genau auf der Schwelle zählt');
gleich(L.entscheide(serie('stein', 0.95, 9000, 9400), jetzt), null, 'Bilder älter als 500 ms zählen nicht');
gleich(L.entscheide(serie('stein', 0.95, 9500, 9550), jetzt), null, 'zu wenige sichere Bilder');
// Mischung: 6 Papier, 3 Stein, 4 unsichere Schere -> Papier
gleich(L.entscheide([
  ...serie('papier', 0.9, 9500, 9750), ...serie('stein', 0.9, 9800, 9900),
  ...serie('schere', 0.5, 9500, 9650),
], jetzt), 1, 'Mehrheit gewinnt, unsichere Bilder zählen nicht');
// Gleichstand
gleich(L.entscheide([...serie('papier', 0.9, 9500, 9700), ...serie('stein', 0.9, 9750, 9950)], jetzt), null, 'Gleichstand');
// Hand kommt spät: viele "nichts"-Bilder, dann 4 Bilder Stein -> Stein ("nichts" stimmt nicht mit ab)
gleich(L.entscheide([...serie('nichts', 0.95, 9500, 9800), ...serie('stein', 0.95, 9850, 10000)], jetzt), 0, 'späte Hand wird nicht von nichts übertönt');
// Hand kommt zu spät: nur 2 Bilder Stein -> nicht sicher
gleich(L.entscheide([...serie('nichts', 0.95, 9500, 9900), ...serie('stein', 0.95, 9950, 10000)], jetzt), null, 'Hand zu spät (nur 2 Bilder)');
// "nichts" zwischen zwei Handzeichen ändert die Mehrheit nicht
gleich(L.entscheide([...serie('papier', 0.9, 9500, 9700), ...serie('nichts', 0.9, 9750, 9900), ...serie('stein', 0.9, 9950, 10000)], jetzt), 1, 'Papier gegen 2 Stein, nichts egal');
// Gross-/Kleinschreibung in der Klasse wird in erkennung.js normalisiert; hier der Klassen-Parser:
gleich(L.klasseZuCode(' Stein '), 0, 'klasseZuCode Leerzeichen/Gross');
gleich(L.klasseZuCode('Class 1'), null, 'klasseZuCode unbekannt');

// analysiere() liefert die Zahlen hinter der Entscheidung (fürs Log)
const an = L.analysiere([...serie('nichts', 0.95, 9500, 9800), ...serie('stein', 0.5, 9850, 10000)], jetzt);
gleich([an.code, an.gesamt, an.gueltig], [null, 11, 0], 'analysiere zählt Bilder und sichere Bilder');
gleich(L.analysiere([], jetzt).code, null, 'analysiere ohne Bilder');

// ---- 3. Protokoll: micro:bit -> Browser ----
gleich(L.parseVonMicrobit('C3'), { typ: 'C', n: 3 }, 'C3');
gleich(L.parseVonMicrobit('C1\r'), { typ: 'C', n: 1 }, 'C1 mit \\r');
gleich(L.parseVonMicrobit('?'), { typ: '?' }, '?');
gleich(L.parseVonMicrobit('X'), { typ: 'X' }, 'X');
gleich(L.parseVonMicrobit('R 1 0 1'), { typ: 'R', ich: 1, gegner: 0, ergebnis: 1 }, 'R Sieg');
gleich(L.parseVonMicrobit('R 0 1 -1'), { typ: 'R', ich: 0, gegner: 1, ergebnis: -1 }, 'R Niederlage');
gleich(L.parseVonMicrobit('R 2 2 0'), { typ: 'R', ich: 2, gegner: 2, ergebnis: 0 }, 'R unentschieden');
gleich(L.parseVonMicrobit('P 2 11'), { typ: 'P', ich: 2, gegner: 11 }, 'P');
for (const muell of ['', 'C4', 'C0', 'R 3 0 1', 'R 1 0 2', 'R 1 0', 'P x y', 'hallo', 'G1', 'Traceback (most recent call last):']) {
  gleich(L.parseVonMicrobit(muell), null, 'ungültig: "' + muell + '"');
}

// ---- 4. Protokoll: Browser -> micro:bit ----
gleich(L.formatAnMicrobit(0), 'G0\n', 'G0');
gleich(L.formatAnMicrobit(1), 'G1\n', 'G1');
gleich(L.formatAnMicrobit(2), 'G2\n', 'G2');
gleich(L.formatAnMicrobit(null), 'G-\n', 'G- bei null');

// ---- 5. Zeilenpuffer: Stücke, \r\n, halbe Zeilen ----
const zp = new L.ZeilenPuffer();
gleich(zp.push('C3\r\nC'), ['C3'], 'Puffer: erste Zeile, Rest bleibt');
gleich(zp.push('2\r\n?\r\n'), ['C2', '?'], 'Puffer: Zeile über zwei Stücke');
gleich(zp.push('R 1 0 '), [], 'Puffer: halbe Zeile');
gleich(zp.push('1\n\n\nX\n'), ['R 1 0 1', 'X'], 'Puffer: leere Zeilen weg');
zp.push('x'.repeat(300));
gleich(zp.push('\n'), [], 'Puffer: Müll ohne Zeilenende wird verworfen');

// ---- 6. Zeilen aus der micro:bit-Simulation (falls vorhanden) ----
const datei = path.join(__dirname, 'ausgabe-microbit.txt');
if (fs.existsSync(datei)) {
  const lines = fs.readFileSync(datei, 'utf8').split('\n').filter(z => z.trim());
  for (const z of lines) pruefe(L.parseVonMicrobit(z) !== null, 'Simulation: Zeile nicht lesbar: "' + z + '"');
  console.log(lines.length + ' Zeilen aus der Simulation geprüft.');
} else {
  console.log('(ausgabe-microbit.txt fehlt: erst simuliere_microbit.py laufen lassen)');
}

console.log(geprueft + ' Prüfungen, ' + fehler + ' Fehler.');
process.exit(fehler ? 1 : 0);
