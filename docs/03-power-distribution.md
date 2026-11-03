# Power distribution

## WAGO split in the body

The switched 7.4 V rail feeds two loads: the servo board and the UBEC in the head. Two WAGO lever connectors make the split without solder.

| Connector | In | Out 1 | Out 2 |
|---|---|---|---|
| WAGO plus | Slide switch output | Servo board DC+ | UBEC IN+ |
| WAGO minus | BMS P− | Servo board DC− | UBEC IN− |

Use 3-way connectors: WAGO 221-413, or 221-613 (same function, rated for 6 mm²). The 221 series takes 0.2–4 mm² wire (24–12 AWG). Strip 11 mm and push the wire fully in. Do not use WAGO connectors for thin signal wires.

## Servo board

Waveshare Bus Servo Adapter (A).

- **Power:** connect DC+ and DC− to the **green screw terminal**. The board also has a round DC jack, and the kit includes 2.1 mm barrel plugs that fit it, but a 2.1 mm barrel connector is typically rated for only a few amps. Fourteen STS3215 servos can draw much more when the robot stands up or walks.
- **Jumpers:** set to **VM** and **ON**. Switch the pack on and check that the PWR LED lights.
- **Data:** USB-C on the servo board to the **middle** micro-USB port on the Pi (marked USB). The right-hand micro-USB on the Pi is power only.
- **Servo bus:** the leg servos plug into servo bus 1 and servo bus 2 as daisy chains. The TNKR text for step 47 calls these "I²C" and "UART" sockets; the drawing and table call them servo bus 1 and 2. Use the two servo bus ports. Direction is corrected in software.

## UBEC

The UBEC sits in the head and converts the 7.4 V rail to 5 V for the Pi, amplifier and ear servos.

- **Before connecting anything to its output,** switch on and measure **5.0 V ± 0.1**. If the UBEC has a 5 V / 6 V jumper, it must be on 5 V. 6 V can damage the Pi.
- Feeding the Pi through its GPIO 5V pin bypasses the Pi's USB fuse. Below 4.75 V the Pi shows an under-voltage warning.

## Removing the head

Most wires through the neck already have connectors:

| Wire | Disconnect |
|---|---|
| USB Pi → servo board | USB plug |
| IMU (4 wires) | Dupont connector at the Pi header |
| Foot switches (4 wires) | Dupont connectors at the Pi header |
| Servo bus to neck and head servos | Servo bus plugs |
| 7.4 V to the UBEC | **None by default** |

Add a connector in the 7.4 V pair between the WAGO connectors and the neck. The current is low (Pi, ears, LEDs and audio, under 2 A at 7.4 V), so a spare 2.1 mm barrel plug and jack from the kit works, or an XT30. An XT60 is oversized for this line.

## No pack connector

The TNKR guide shows an XT60 on the pack output (steps 37–40, 52). The kit does not include one, and it is not needed: the slide switch cuts power, and the pack charges in place over USB-C.
