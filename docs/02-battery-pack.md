# Battery pack

Parts: 18650 cell holder (2 cells), 2× 18650 cells, 2S BMS (HX-2S-JH20), USB-C 2S charger board, slide switch.

## How the BMS works

The HX-2S-JH20 has two groups of pads:

| Pad | Group | Connects to |
|---|---|---|
| B− | Battery | Cell 1 negative (bottom of the pack) |
| BM | Battery | Midpoint between the cells |
| B+ | Battery | Cell 2 positive (top of the pack) |
| P− | Protected output | Charger BAT−, WAGO minus |
| P+ | Protected output | Charger BAT+, slide switch |

The protection MOSFETs sit between **B−** and **P−**. They open on over-charge, over-discharge or over-current. That is why everything outside the pack, including the charger, connects to the **P** pads.

On boards of this type, B+ and P+ are usually the same copper. TNKR's drawings label one pad "B+/P+". **Unverified** for this exact board: the manufacturer's manual does not say. The wiring below is correct either way, because the cells go on B+ and the output on P+.

## Solder order

Order matters. Do not change it.

1. **Third lead on the holder.** Solder a yellow wire to the metal strip between the two cell positions. This is BM. Keep leads 8–10 cm. No cells in the holder yet.
2. **Tin everything.** Tin the BMS pads (B−, BM, B+, P−, P+) and all wire ends at about 350 °C. Work quickly: the pads are heavy copper.
3. **Continuity check.** Multimeter in continuity (beep) mode. **B− to P− must not beep.** If it does, the BMS is faulty. B+ to P+ probably beeps; the wiring does not depend on it.
4. **Cell wires to the BMS, in this order:** black to **B−**, then yellow to **BM**, then red to **B+**. Put the red wire on the **B+** pad, not P+. Never connect B+ before B−.
5. **Charger to the BMS:** BAT− to **P−** first, then BAT+ to **P+**. Some boards print BAT as OUT. BAT− must reach P−, not B−, or the BMS cannot protect during charging.
6. **Switch:** P+ to the switch. The switch's other leg to WAGO plus (see [03-power-distribution.md](03-power-distribution.md)). Heat-shrink every joint at the switch: the lugs are close together.
7. **P− to WAGO minus.**

After this, P+ carries two wires (charger BAT+, switch) and P− carries two wires (charger BAT−, WAGO minus).

## Wire gauge

| Wire | Gauge |
|---|---|
| Cell wires B−, B+ | 20 AWG |
| BM sense wire | 22 AWG |
| P+ → switch → WAGO, P− → WAGO | 18 AWG |
| Charger wires | 20 AWG |

Source: TNKR wiring table (step 52).

## Cells

Charge both cells first. Their voltages must be within **0.05 V** of each other, or the BMS may shut off. Insert them following the holder's + and − marks. A small spark on the second cell is normal: the BMS capacitors charge.

## Measurements

With cells inserted:

| Between | Expect |
|---|---|
| B− and B+ | 6.0–8.4 V |
| B− and BM | 3.0–4.2 V |
| BM and B+ | 3.0–4.2 V |
| P− and P+ | About the same as B− to B+ |

If P− to P+ reads 0 V, the BMS is asleep. Plug in the USB-C charger for a few seconds to wake it.

## Switch test

Measure across the switched output (switch out to P−). One position reads 0 V, the other reads full pack voltage. Mark the ON side.

## Switch on plus or minus?

TNKR puts the switch on P+. The GitHub diagram puts it on P−. Both cut the power. This repo follows TNKR (P+), because then the robot's chassis and all grounds stay connected to the pack minus even when switched off, which is the usual convention. If your pack is already built with the switch on minus, it works; just swap the roles of the WAGO connectors accordingly.
