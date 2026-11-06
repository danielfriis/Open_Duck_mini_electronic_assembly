# Power distribution

## WAGO split in the body

The switched 7.4 V rail feeds two loads: the servo board and the UBEC in the head. Two WAGO lever connectors make the split without solder.

| Connector | In | Out 1 | Out 2 |
|---|---|---|---|
| WAGO plus | Slide switch output | Servo board DC+ | UBEC IN+ |
| WAGO minus | BMS P− | Servo board DC− | UBEC IN− |

Use 3-way connectors: WAGO 221-413 or 221-613. They do the same job but take different wire sizes:

| Connector | Wire range |
|---|---|
| 221-413 | 0.14–4 mm² (24–12 AWG) |
| 221-613 | 0.5–6 mm² (20–10 AWG) |

With the 221-613, every wire must be 20 AWG or thicker. A 22 AWG lead does not clamp reliably; use a 221-413 for it, or extend it with 20 AWG first. Strip 11 mm and push the wire fully in. Do not use WAGO connectors for thin signal wires.

## Servo board

Waveshare Bus Servo Adapter (A).

- **Power:** connect DC+ and DC− to the **green screw terminal**. The board also has a round DC jack, and the kit includes 2.1 mm barrel plugs that fit it, but a 2.1 mm barrel connector is typically rated for only a few amps. Fourteen STS3215 servos can draw much more when the robot stands up or walks.
- **Power jumpers:** set to **VM** and **ON** (TNKR step 39). Switch the pack on and check that the PWR LED lights.
- **A/B jumper:** set to **B**. B selects USB control; A selects the UART header (Waveshare wiki). TNKR shows this only as a label in the step 47 drawing ("set to B"); no step text mentions it.
- **Data:** USB-C on the servo board to the **middle** micro-USB port on the Pi (marked USB). With the SD card on the left, the right-hand micro-USB (PWR IN) is power only.
- **Servo bus:** the leg servos plug into servo bus 1 and servo bus 2 as daisy chains. The TNKR text for step 47 calls these "I²C" and "UART" sockets; the drawing and table call them servo bus 1 and 2. Use the two servo bus ports. Direction is corrected in software.

## UBEC

The UBEC sits in the head and converts the 7.4 V rail to 5 V for the Pi, amplifier and ear servos. TNKR's drawing (step 40) shows a Henge 5 A UBEC printed "INPUT 7V–25.2V".

- **5 V / 6 V jumper on 5 V.** 6 V can damage the Pi.
- **Before connecting anything to its output,** switch on and measure **5.0 V ± 0.1**.
- **Input floor 7 V.** The pack runs 6.0–8.4 V, and the servos pull it lower under load. Below about 7 V the 5 V rail can sag and the Pi can reset before the BMS cuts off. Recharge when the pack rests at about 7.0–7.2 V.
- Feeding the Pi through its GPIO 5V pin bypasses the Pi's USB fuse. The Pi flags under-voltage below about 4.63 V. TNKR says 4.75 V; either way, aim for 5.0–5.1 V.
- **Never plug a USB power supply into the Pi's PWR port** while the UBEC feeds pin 2. The two supplies would run in parallel with no protection.

## Removing the head

Most wires through the neck already have connectors:

| Wire | Disconnect |
|---|---|
| USB Pi → servo board | USB plug |
| IMU (4 wires) | Dupont connector at the Pi header |
| Foot switches (4 wires) | Dupont connectors at the Pi header |
| Servo bus to neck and head servos | Servo bus plugs |
| 7.4 V to the UBEC | **None by default** |

Add a connector in the 7.4 V pair between the WAGO connectors and the neck. The current is low (Pi, ears, LEDs and audio, under 2 A at 7.4 V). A disconnect needs a matching pair: a 2.1 mm barrel plug **and** an inline 2.1 mm barrel jack, or an XT30 pair. The kit has 2.1 mm barrel plugs; you probably have to buy the jack. An XT60 is oversized for this line.

## No pack connector

The TNKR guide shows an XT60 on the pack output (steps 37, 39, 40, 52). The kit does not include one, and it is not needed: the slide switch cuts power, and the pack charges in place over USB-C.
