#!/usr/bin/env python3
"""Build the terminal-level wiring diagram from parts.csv and connections.csv.

Every part is drawn as a box with one dot per pad or terminal. Every row in
connections.csv becomes one wire between two dots. Edit the CSV files, then run:

    python3 tools/build_wiring_diagram.py                 # English, writes diagrams/wiring-*.svg/.png
    python3 tools/build_wiring_diagram.py --lang da --out /tmp/da   # Danish labels

Three diagrams are built: power, head and signals. A part can appear in more
than one; each diagram shows only the pins whose wires both end inside it.

Requires Graphviz (`dot`) on PATH.
"""
import argparse
import csv
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NET_STYLE = {
    "PACK_NEG": ("#1b1b1b", "solid", 2.4),
    "GND": ("#1b1b1b", "solid", 2.0),
    "PACK_MID": ("#d4a017", "solid", 2.0),
    "PACK_POS": ("#d0701c", "solid", 2.4),
    "P_POS": ("#d0701c", "solid", 2.4),
    "V7": ("#d0701c", "solid", 2.4),
    "V5": ("#cc3434", "solid", 2.0),
    "V3": ("#e0708a", "solid", 1.6),
    "I2C": ("#3563c4", "solid", 1.6),
    "I2S": ("#14868a", "solid", 1.6),
    "LED": ("#c08a12", "solid", 1.6),
    "EAR": ("#7a4cc2", "solid", 1.6),
    "FOOT": ("#3d8a4a", "solid", 1.6),
    "SPK": ("#777777", "solid", 1.6),
    "USB": ("#555555", "dashed", 1.6),
    "BUS": ("#8a5a2a", "bold", 2.0),
    "CSI": ("#555555", "dashed", 1.6),
}

# Nets left out of a diagram even when both ends are in it (they are drawn elsewhere).
EXCLUDE_NETS = {"head": {"I2S"}}

# Diagram -> {part: column}. Columns run left to right.
DIAGRAMS = {
    "power": {"cells": 0, "chg": 0, "bms": 1, "sw": 2, "wagop": 3, "wagom": 3,
              "sb": 4, "ubec": 4, "legl": 5, "legr": 5, "strip": 5, "neck": 6},
    "head": {"ubec": 0, "strip": 1, "earr": 2, "earl": 2, "amp": 2, "pi": 3,
             "r1": 4, "r2": 4, "ledr": 5, "ledl": 5},
    "signals": {"sb": 0, "imu": 0, "footl": 0, "footr": 0, "cam": 0, "pi": 1,
                "mic": 2, "amp": 3, "spk": 4},
}

AREAS = {
    "en": {"pack": "Battery pack", "body": "Body", "head": "Head"},
    "da": {"pack": "Batteripakke", "body": "Krop", "head": "Hoved"},
}

LEGEND = {
    "en": [("V7", "7.4 V (switched) / pack +"), ("V5", "5 V"), ("V3", "3.3 V"), ("GND", "GND / minus"),
           ("PACK_MID", "BM midpoint"), ("I2C", "I2C"), ("I2S", "I2S audio"), ("LED", "LED"),
           ("EAR", "Ear servo signal"), ("FOOT", "Foot switch"), ("BUS", "Servo bus"), ("USB", "USB / CSI")],
    "da": [("V7", "7,4 V (efter afbryder) / pakke +"), ("V5", "5 V"), ("V3", "3,3 V"), ("GND", "GND / minus"),
           ("PACK_MID", "BM midtpunkt"), ("I2C", "I2C"), ("I2S", "I2S lyd"), ("LED", "LED"),
           ("EAR", "Ørerservo-signal"), ("FOOT", "Fodkontakt"), ("BUS", "Servo-bus"), ("USB", "USB / CSI")],
}

PIN_DA = {
    "Red (+) top of pack": "Rød (+) toppen af pakken",
    "Yellow BM midpoint": "Gul BM midtpunkt",
    "Black (−) bottom of pack": "Sort (−) bunden af pakken",
    "DC+ screw terminal": "DC+ skrueterminal",
    "DC− screw terminal": "DC− skrueterminal",
    "Bus in": "Bus ind",
    "5V rail": "5V-bane",
    "GND rail": "GND-bane",
    "Right ear signal lane": "Højre øre signalbane",
    "Left ear signal lane": "Venstre øre signalbane",
    "Micro-USB (USB)": "Micro-USB (USB)",
    "Camera connector": "Kamerastik",
    "SEL (leave open)": "SEL (lad være åben)",
    "Brown GND": "Brun GND",
    "Red VCC": "Rød VCC",
    "Orange SIG": "Orange SIG",
}


def read_parts(lang):
    parts = {}
    with open(ROOT / "parts.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            pins = []
            for item in row["pins"].split("|"):
                pid, label = item.split("=", 1)
                if lang == "da":
                    label = PIN_DA.get(label, label).replace("3.3V", "3,3V")
                pins.append((pid, label))
            parts[row["part"]] = {
                "area": row["area"],
                "label": row["label_" + lang],
                "pins": pins,
            }
    return parts


def read_connections():
    with open(ROOT / "connections.csv", newline="") as fh:
        return list(csv.DictReader(fh))


def check(parts, wires):
    errors = []
    for w in wires:
        for side in ("from", "to"):
            part, pin = w[side + "_part"], w[side + "_pin"]
            if part not in parts:
                errors.append(f"{w['id']}: unknown part {part}")
            elif pin not in {p for p, _ in parts[part]["pins"]}:
                errors.append(f"{w['id']}: unknown pin {part}.{pin}")
        if w["net"] not in NET_STYLE:
            errors.append(f"{w['id']}: unknown net {w['net']}")
    used = {(w[s + "_part"], w[s + "_pin"]) for w in wires for s in ("from", "to")}
    for name, part in parts.items():
        for pid, _ in part["pins"]:
            if (name, pid) not in used and pid != "sel":
                errors.append(f"unused pin {name}.{pid}")
    return errors


def node_label(part, shown):
    rows = [f'<tr><td colspan="3" bgcolor="#eef0ea" cellpadding="6"><b>{html.escape(part["label"])}</b></td></tr>']
    for pid, label in part["pins"]:
        if pid not in shown:
            continue
        rows.append(
            f'<tr><td port="{pid}_w" width="14"><font color="#1b1b1b">●</font></td>'
            f'<td align="center">{html.escape(label)}</td>'
            f'<td port="{pid}_e" width="14"><font color="#1b1b1b">●</font></td></tr>'
        )
    return '<<table border="1" color="#9aa39b" cellborder="0" cellspacing="0" cellpadding="3" bgcolor="white">' + "".join(rows) + "</table>>"


def build_dot(parts, wires, lang, cols):
    out = [
        "digraph wiring {",
        '  graph [rankdir=LR, splines=spline, nodesep=0.45, ranksep=1.6, bgcolor="white", fontname="Helvetica", pad=0.4, newrank=true];',
        '  node [shape=plain, fontname="Helvetica", fontsize=12];',
        '  edge [arrowhead=none, fontname="Helvetica", fontsize=9, fontcolor="#666666"];',
    ]
    shown = {}
    for w in wires:
        for side in ("from", "to"):
            shown.setdefault(w[side + "_part"], set()).add(w[side + "_pin"])
    if "mic" in cols:
        shown.setdefault("mic", set()).add("sel")
    for name in cols:
        out.append(f"  {name} [label={node_label(parts[name], shown.get(name, set()))}];")
    for c in sorted(set(cols.values())):
        members = " ".join(n for n, v in cols.items() if v == c)
        out.append(f"  {{rank=same; {members}}}")
    for w in wires:
        color, style, width = NET_STYLE[w["net"]]
        a, b = w["from_part"], w["to_part"]
        pa, pb = w["from_pin"], w["to_pin"]
        if cols[a] > cols[b]:
            a, b, pa, pb = b, a, pb, pa  # always draw left to right so ranks follow the columns
        if cols[a] < cols[b]:
            ta, tb = f"{pa}_e:e", f"{pb}_w:w"
        else:
            ta, tb = f"{pa}_e:e", f"{pb}_e:e"
        constraint = "true" if cols[a] != cols[b] else "false"
        out.append(
            f'  {a}:{ta} -> {b}:{tb} '
            f'[color="{color}", style="{style}", penwidth={width}, xlabel="{w["id"]}", constraint={constraint}];'
        )
    nets = {w["net"] for w in wires}
    rows = "".join(
        f'<tr><td><font color="{NET_STYLE[n][0]}"><b>━━━</b></font></td><td align="left">{html.escape(t)}</td></tr>'
        for n, t in LEGEND[lang] if n in nets or (n == "V7" and nets & {"P_POS", "PACK_POS"}) or (n == "USB" and "CSI" in nets)
    )
    out.append(f'  legend [label=<<table border="1" color="#9aa39b" cellborder="0" cellpadding="3" bgcolor="white"><tr><td colspan="2"><b>{"Legend" if lang == "en" else "Forklaring"}</b></td></tr>{rows}</table>>];')
    first = min(cols, key=lambda n: (cols[n], n))
    out.append(f"  {{rank=same; legend; {' '.join(n for n in cols if cols[n] == cols[first])}}}")
    out.append("}")
    return "\n".join(out)


def select(wires, name, cols):
    skip = EXCLUDE_NETS.get(name, set())
    return [w for w in wires if w["from_part"] in cols and w["to_part"] in cols and w["net"] not in skip]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["en", "da"], default="en")
    ap.add_argument("--out", default=str(ROOT / "diagrams"), help="output directory")
    args = ap.parse_args()

    parts = read_parts(args.lang)
    wires = read_connections()
    errors = check(parts, wires)
    covered = set()
    for name, cols in DIAGRAMS.items():
        covered |= {w["id"] for w in select(wires, name, cols)}
    errors += [f"{w['id']}: not in any diagram" for w in wires if w["id"] not in covered]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    for name, cols in DIAGRAMS.items():
        sub = select(wires, name, cols)
        dot = build_dot(parts, sub, args.lang, cols)
        base = outdir / f"wiring-{name}"
        subprocess.run(["dot", "-Tsvg", "-o", str(base.with_suffix(".svg"))], input=dot, text=True, check=True)
        subprocess.run(["dot", "-Tpng", "-Gdpi=110", "-o", str(base.with_suffix(".png"))], input=dot, text=True, check=True)
        print(f"{name}: {len(sub)} wires -> {base}.svg/.png")


if __name__ == "__main__":
    main()
