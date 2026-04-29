# antenna-calculator
- [Antenna Design and Integration Fundamentals - YouTube](https://www.youtube.com/watch?v=46SbGxS73dY)
- [Resonant Magnet-Field Antennas Pt.2:AM-Modulation & Measuring Bandwidth, Q-Factor and Damping-Factor - YouTube](https://www.youtube.com/watch?v=gJlkWt3VYxM)
- [Universal Equivalent Circuits for All Antennas - Jan 2022 - YouTube](https://www.youtube.com/watch?v=vQ9BFdmFHCM)
- [Antenna Bandwidth — Lesson 3 - YouTube](https://www.youtube.com/watch?v=_WuVv4tWVd8)
- [What is Antenna Impedance? (Explained) - YouTube](https://www.youtube.com/watch?v=5JfTa9FGkVQ)
- [Antenna: Key Parameters That Define Performance (Radiation, Gain, Beamwidth, Directivity, Beamwidth & More). - YouTube](https://www.youtube.com/playlist?list=PLFxhgwM1F4yyWeuTR8ZoQEBZbfgJu5fjl)
- [Measuring Antenna Bandwidth with R&S ZVL - YouTube](https://www.youtube.com/watch?v=Z1vquNziEmQ)

### Types of antennas
- Meander (Line)
  - [What is meander line antenna| meander line patch antenna| antenna basic|antenna theory - YouTube](https://www.youtube.com/watch?v=bmmNgCtWt2c)
  - [THE STUDY AND IMPLEMENTATION OF MEANDER-LINE ANTENNA FOR AN INTEGRATED TRANSCEIVER DESIGN](https://www.diva-portal.org/smash/get/diva2:299692/FULLTEXT01.pdf)
- Inverted-F Antenna (IFA) 
- [(Microstrip) Patch antenna - Wikipedia](https://en.wikipedia.org/wiki/Patch_antenna)
  - [Microstrip Patch Antenna - GeeksforGeeks](https://www.geeksforgeeks.org/electronics-engineering/microstrip-patch-antenna/)

### Notes
- ```Markdown
  The image shows a **Printed Inverted-F Antenna (PIFA)** that has been modified with a **meander line** structure. This specific design is a common variant of the **Meander Line Antenna (MLA)** used in compact devices like smartphones, IoT modules, and Bluetooth/Wi-Fi devices.
  
  Designing this antenna involves three main steps: calculating the total resonant length, accounting for the dielectric substrate, and matching the impedance.
  
  ### 1. The Resonant Frequency Equation
  The fundamental principle of a PIFA or Monopole antenna is that its total length ($L_{total}$) should be approximately a quarter-wavelength ($\lambda/4$) of the target frequency.
  
  The general formula for the total electrical length is:
  $$L_{total} \approx \frac{c}{4 \cdot f \cdot \sqrt{\epsilon_{eff}}}$$
  
  Where:
  *   **$c$**: Speed of light ($\approx 3 \times 10^8$ m/s)
  *   **$f$**: Target frequency (e.g., 2.4 GHz)
  *   **$\epsilon_{eff}$**: Effective dielectric constant of the PCB material (usually FR4).
  
  ### 2. Total Physical Length ($L_{total}$)
  Based on the dimensions provided in your diagram, the total length of the conductive path is the sum of all horizontal and vertical segments from the feed point to the open end:
  
  $$L_{total} = L_6 + L_3 + (3 \times L_4) + (2 \times L_2) + (2 \times L_5) + L_1$$
  
  *Note: In meander antennas, the actual resonant frequency is often lower than the calculated path length suggests because of "coupling" between the parallel meander lines. This is why engineers usually multiply the theoretical length by a "velocity factor" or use simulation software.*
  
  ### 3. Effective Dielectric Constant ($\epsilon_{eff}$)
  Since the antenna is printed on a PCB, the signal travels partly through the board (substrate) and partly through the air. You must calculate the effective dielectric constant:
  
  $$\epsilon_{eff} = \frac{\epsilon_r + 1}{2} + \frac{\epsilon_r - 1}{2} \left[ 1 + 12 \frac{h}{W} \right]^{-0.5}$$
  
  *   **$\epsilon_r$**: Relative permittivity of the board (FR4 is typically 4.4).
  *   **$h$**: Thickness of the PCB substrate.
  *   **$W$**: Width of the trace ($W_2$ in your diagram).
  
  ### 4. Impedance Matching (The "F" Shape)
  The left side of your diagram shows a "Via to ground" and a "Feed point." This is the Inverted-F structure.
  *   **The distance between the Feed and the Ground ($D_5$)** controls the input impedance (typically 50 Ohms).
  *   Increasing $D_5$ increases the inductive reactance. 
  *   **$W_1$ and $W_2$**: The width of the traces affects the bandwidth. Wider traces ($W_1$) generally provide a wider frequency bandwidth.
  
  ### 5. Summary of Design Variables
  *   **To lower the frequency:** Increase the number of meander turns or increase lengths $L_2/L_5$.
  *   **To tune for 50 Ohms:** Adjust the gap $D_5$ between the ground via and the feed point.
  *   **To improve bandwidth:** Increase the trace widths $W_1$ and $W_2$.
  
  **Practical Tip:** Because of the complex interactions (mutual coupling) between the meandered segments ($L_4$), these antennas are rarely built using equations alone. Most engineers use the equations to get a "starting guess" and then use **EM Simulation software** (like CST, HFSS, or OpenEMS) to fine-tune the dimensions $D, L, \text{and } W$.

  ```
### Tutorials
- [AN-B-027: Designing Printed Antennas for Bluetooth Low Energy](./files/REN_AN-B-027_Designing_Printed_Antennas_for_Bluetooth_Low_Energy_Rev2.5_APN_20240627_1.pdf)
  - https://www.renesas.com/en/document/apn/b-027-designing-printed-antennas-bluetooth-low-energy
- [A Complete Guide For PCB 2.4G Antenna Design | C&T RF Antennas Inc | Antenna Manufacturer](https://lcantennas.com/a-complete-guide-for-pcb-2-4g-antenna-design/)
- [Antenna Design – PCB Antenna Design](https://pcbantennas.com/antenna-design/)
- [How to Design a PCB Antenna for 2.4GHz](https://circuitdigest.com/article/how-to-design-a-pcb-antenna-for-24ghz)
- [AN043 -- Small Size 2.4 GHz PCB Antenna (Rev. D)](https://www.ti.com/lit/an/swra117d/swra117d.pdf)
- [KarthikT23/HFSS-Microstrip-Patch-Antenna: Designing a 2.4 GHz antenna using Ansys HFSS](https://github.com/KarthikT23/HFSS-Microstrip-Patch-Antenna)
- [WissamAntoun/Circularly-Polarized-Patch-Antenna-HFSS: A microstrip patch antenna with circularly polarized matched to 50 Ω and operating at 2.4 GHz. SImulation done on HFSS](https://github.com/WissamAntoun/Circularly-Polarized-Patch-Antenna-HFSS)
