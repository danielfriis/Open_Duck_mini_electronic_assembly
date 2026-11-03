# Open Duck Mini v2 — Electrical Documentation

Clear, verified wiring documentation for the [Open Duck Mini v2](https://github.com/apirrone/Open_Duck_Mini), written while building the TNKR kit.

The official sources disagree with each other in places: the GitHub assembly guide, the TNKR step-by-step guide, TNKR's connection table and TNKR's runtime code. This repo collects one consistent wiring that matches the parts in the kit and the pin numbers in the code, and it lists every disagreement we found.

## What is different from the official guides

- **Every Pi header pin carries one wire.** No splices on a 5V or GND bus.
- **Power is distributed with WAGO lever connectors in the body** and a small stripboard in the head.
- **No XT60.** The TNKR guide shows one, but the kit does not include it. The pack switch does the job.
- **Battery wiring follows the BMS manufacturer,** not TNKR's drawings, which merge the B+ and P+ pads.
- **Pins are checked against the runtime code,** not against photos.

## Contents

| File | Contents |
|---|---|
| [docs/01-overview.md](docs/01-overview.md) | System overview and power architecture |
| [docs/02-battery-pack.md](docs/02-battery-pack.md) | BMS pads, solder order, charger, switch, measurements |
| [docs/03-power-distribution.md](docs/03-power-distribution.md) | WAGO split, servo board, UBEC, head disconnect |
| [docs/04-head-wiring.md](docs/04-head-wiring.md) | Stripboard, ear servos, LEDs, amplifier and microphone |
| [docs/05-pinout.md](docs/05-pinout.md) | Raspberry Pi header map, verified against the code |
| [docs/06-bring-up.md](docs/06-bring-up.md) | Checks before and at first power-on |
| [docs/07-tnkr-errata.md](docs/07-tnkr-errata.md) | Every disagreement found in the TNKR guide |
| [docs/bom-electrical.md](docs/bom-electrical.md) | Electrical parts: kit contents and extras |
| [connections.csv](connections.csv) | Every wire: from, to, net, gauge. The single source of truth |
| [diagrams/](diagrams/) | Schematic, stripboard layout, header map |

## Status

Written during a build in November 2026. Some points are not yet confirmed on the bench. They are marked **Unverified** in the docs. Open an issue or pull request when you confirm or disprove one.

## Scope

- Open Duck Mini v2 as sold by TNKR (tnkr.ai), with the BOM listed in [docs/bom-electrical.md](docs/bom-electrical.md).
- Pin numbers checked against [tnkrai/Open_Duck_Mini_Runtime](https://github.com/tnkrai/Open_Duck_Mini_Runtime). The upstream runtime ([apirrone/Open_Duck_Mini_Runtime](https://github.com/apirrone/Open_Duck_Mini_Runtime)) may differ.

## Safety

You are wiring a 2S lithium-ion pack. A short circuit can melt wires and start a fire. Check every joint with a multimeter before you connect cells, and never leave a charging pack unattended.

## Credits and license

Based on the Open Duck Mini project by Antoine Pirrone and contributors, and on the TNKR build guide. This repo contains no TNKR text or images; it refers to TNKR steps by number.

Licensed under Apache-2.0, the same license as the upstream project.
