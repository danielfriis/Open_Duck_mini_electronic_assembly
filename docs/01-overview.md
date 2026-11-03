# System overview

![Full schematic](../diagrams/schematic.png)

## Power architecture

```mermaid
flowchart TD
  CELLS["2× 18650 in series<br/>6.0–8.4 V"] -->|B−, BM, B+| BMS["2S BMS<br/>HX-2S-JH20"]
  CHG["USB-C charger (2S)"] -->|BAT+ → P+, BAT− → P−| BMS
  BMS -->|P+| SW["Slide switch"]
  SW --> WP["WAGO plus"]
  BMS -->|P−| WM["WAGO minus"]
  WP --> SB["Servo board<br/>screw terminal DC+/DC−"]
  WM --> SB
  WP -->|through neck| UBEC["UBEC 5 V"]
  WM -->|through neck| UBEC
  SB -->|servo bus 1 + 2| STS["14× Feetech STS3215"]
  UBEC --> STRIP["Head stripboard<br/>5V and GND rails"]
  STRIP --> PI["Raspberry Pi Zero 2 W<br/>pin 2 / pin 6"]
  STRIP --> AMP["MAX98357A amplifier"]
  STRIP --> EARS["2× SG90 ear servos"]
  STRIP --> LEDGND["LED cathodes"]
  PI -->|USB data| SB
```

There are two rails:

| Rail | Source | Feeds |
|---|---|---|
| 7.4 V (switched) | Battery pack through the slide switch | Servo board (14 bus servos), UBEC |
| 5 V | UBEC in the head | Raspberry Pi, amplifier, ear servos |
| 3.3 V | Raspberry Pi pins 1 and 17 | IMU, microphone |

All grounds are common. The BMS protects on the negative side, so every minus wire downstream of the pack connects to **P−**, never to **B−**.

## Body and head

| Location | Parts |
|---|---|
| Body | Battery pack (cells, BMS, charger, switch), WAGO connectors, servo board, IMU, foot switches, leg servos |
| Head | UBEC, stripboard, Raspberry Pi, amplifier and speaker, microphone, eye LEDs, ear servos, camera |
| Through the neck | 7.4 V pair to the UBEC, USB cable Pi → servo board, IMU (4 wires), foot switches (4 wires), servo bus to neck/head servos |

See [03-power-distribution.md](03-power-distribution.md#removing-the-head) for making the head removable.
