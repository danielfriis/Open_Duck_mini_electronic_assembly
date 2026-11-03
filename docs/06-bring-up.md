# Bring-up checklist

Work through this in order. Stop at the first check that fails.

## Before any cells go in

- [ ] BMS: B− to P− does **not** beep in continuity mode.
- [ ] Cell wires: black on B−, yellow on BM, red on B+.
- [ ] Charger: BAT− on P−, BAT+ on P+.
- [ ] Every joint at the switch is heat-shrunk.
- [ ] Both cells charged, within 0.05 V of each other.

## Pack

- [ ] B− to B+: 6.0–8.4 V. B− to BM and BM to B+: 3.0–4.2 V each.
- [ ] P− to P+ about equal to B− to B+ (plug in USB-C briefly if it reads 0 V).
- [ ] Switch: 0 V in one position, pack voltage in the other. ON side marked.

## Body

- [ ] Plus and minus in separate WAGO connectors, every wire pushed fully in.
- [ ] Servo board jumpers on VM and ON. Switch on: PWR LED lights.

## Head, without the Pi

- [ ] Stripboard: 5 V to GND does not beep. Across the signal-strip cut does not beep.
- [ ] Switch on: 5.0 V ± 0.1 between the stripboard rails. UBEC jumper (if any) on 5 V.
- [ ] Switch off. Ear servos on with brown toward GND.

## With the Pi

- [ ] Pi on the header. USB cable from the servo board in the Pi's **middle** micro-USB (marked USB).
- [ ] Switch on. The Pi boots without an under-voltage warning.
- [ ] Run `python3 mini_bdx_runtime/mini_bdx_runtime/feet_contacts.py` and press each foot switch.

## First charge

- [ ] Plug in USB-C, check the charger LED, watch the pack rise toward 8.4 V.
- [ ] Let one full cycle finish so the BMS can balance the cells.

## Working on the robot

Switch off before plugging or unplugging anything. The slide switch does the same as disconnecting the battery; you do not need to open the WAGO connectors.
