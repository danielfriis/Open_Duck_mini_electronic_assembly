# TNKR guide errata

Found by comparing the TNKR Open Duck Mini V2 guide (steps, 2D/3D views, connection table and BOM) with the kit, the BMS manual, the GitHub docs and the TNKR runtime code. Checked 3 November 2026. Step numbers refer to the TNKR assembly instructions.

| # | Topic | TNKR shows | Reality | This repo |
|---|---|---|---|---|
| 1 | Pack connector | XT60 between switch and loads (steps 37, 39, 40, 52) | No XT60 in the kit BOM. The BOM lists one "2.1mm barrel jack" (Power), which no step, drawing or connection table uses. | No pack connector. The switch cuts power. |
| 2 | Fuse | "The fuse goes on wire 3" (step 37) | No fuse in the kit BOM. | Build without, or add an inline fuse. |
| 3 | Cell positive wire | Step 5 text and step 52 table: B+. Step 5 drawing: the P+ pad, labelled "B+/P+". Step 35 drawing: missing. | The BMS has separate B+ and P+ pads. The connection table attaches this wire to "Wire 3" instead of a pad, so drawings without wire 3 drop it. | Red cell wire on **B+**. |
| 4 | B+ and P+ | Drawn as one pad "B+/P+" | Two pads on the board. Probably the same copper; not stated in the manufacturer's manual. | Wiring works either way. |
| 5 | Switch position | On P+ (steps 37, 52) | GitHub diagram has it on P−. Both work. | P+, as TNKR. |
| 6 | Servo board power | Green screw terminal (step 39) | GitHub shows the barrel jack input. A 2.1 mm barrel connector is typically rated for only a few amps. | Screw terminal. |
| 7 | Right foot GPIO | Photo says "gpio 26" (step 53) | Connection table: pin 13. Runtime code: GPIO 27 (pin 13). | Pin 13. |
| 8 | Foot switch ground | Both C (COM) terminals to pin 9 with the IMU ground (step 53) | Three wires on one pin. | Pins 14 and 20. |
| 9 | Eye LEDs | Two LEDs with 100 Ω resistors on pins 16 and 18, cathode to pin 14 (step 51) | GitHub shows three LEDs (eyes and projector) on pins 16, 18, 22 with no resistors. The runtime has eyes on GPIO 23/24 and an optional projector on GPIO 25. | Two LEDs with resistors, cathodes to the stripboard GND. |
| 10 | LED rows in the connection table | Resistor 1 lead A and lead B both to pin 18; LED 1 + also to pin 18. Same for resistor 2 and pin 16. | Correct order is Pi pin → resistor → LED +. | Follow the step 51 drawing, not the table. |
| 11 | Ear servo power | From the UBEC (step 46) | GitHub's pin table powers them from the Pi's pin 2. | UBEC via the stripboard. |
| 12 | Microphone | 3V on pin 1, GND on pin 6, DOUT on pin 38, clocks shared with the amplifier (step 50) | Not in GitHub's pin table. Pin 1 already feeds the IMU and pin 6 the stripboard. Shared clocks put two wires on pins 12 and 35. | 3V on pin 17, GND on pin 39, clocks chained through the microphone pads. |
| 13 | Amplifier power | VIN on pin 2, GND on pin 34 | Pin 2 also takes the UBEC output in TNKR's table. | VIN and GND from the stripboard. |
| 14 | Leg motor sockets | Text: left in the "I²C socket", right in the "UART socket" (step 47) | Drawing and table: servo bus 1 and servo bus 2. | The two servo bus ports. |
| 15 | Kit contents | FAQ: camera and microphone not included | BOM lists both. | Check your box. |
| 16 | Pi header | BOM: Raspberry Pi Zero 2 W | The W model usually ships without a header. | Solder a 2×20 header if yours has none. |
| 17 | Motor configuration power | GitHub: use "the battery pack" | TNKR step 1: the cell holder and two cells are enough; the finished pack comes later. | As TNKR. |
| 18 | Servo board A/B jumper | Only a label in the step 47 drawing: "set to B". No step text mentions it; step 39 sets only VM and ON. | Waveshare: B = USB control, A = UART header. The Pi uses USB. | A/B jumper on B. Listed in the bring-up checklist. |
| 19 | Pi under-voltage level | "Below 4.75 V" (step 44) | The Pi flags under-voltage at about 4.63 V. | Aim for 5.0–5.1 V. |
