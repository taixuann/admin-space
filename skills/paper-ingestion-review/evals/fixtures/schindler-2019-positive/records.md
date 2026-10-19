# Experimental Records — fixture revision GOLD-2

All IDs and revisions are fixture-local. These records summarize paper-reported procedures; they are not laboratory notebook records.

## EXP-01 — Reagent, buffer, and dopamine-solution preparation

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Type:** `PREPARATION`
- **Technique:** solution preparation
- **Subject/system:** dopamine solutions and pH buffers used in the paper
- **Inputs:** dopamine hydrochloride; KH2PO4 and Na2HPO4; NaCl for the separately described PBS preparation; acetate reagents for pH 5.0 buffer.
- **Reported operation and output:** 0.1 M phosphate buffers were prepared by mixing 0.1 M KH2PO4 and Na2HPO4 solutions to pH 5.8 or 7.0. A PBS preparation is described as adding 0.5 M NaCl to phosphate buffer. Dopamine hydrochloride solutions of 0.5, 2, and 5 mM were made immediately before use because dopamine oxidizes quickly. A 0.05 M acetate buffer at pH 5.0 was also prepared for the auto-oxidation demonstration. Buffers were stored at 4 °C in the dark.
- **Source locator:** accepted manuscript §2.1, pp. 4–5; Figure 4 caption, p. 9.
- **Provenance / uncertainty:** the abstract calls the CV medium PBS, while §2.2, Table 1 and figure captions use phosphate buffer. The paper does not unambiguously say whether 0.5 M NaCl was present in each CV solution. Do not resolve this by inference.
- **Linked findings:** FND-01, FND-02, FND-03, FND-05, FND-06.

## EXP-02 — Cyclic-voltammetry experiment

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Type:** `MEASUREMENT`
- **Technique:** cyclic voltammetry
- **Subject/system:** dopamine hydrochloride in phosphate buffer on a gold working electrode
- **Inputs/system:** dopamine hydrochloride (0.5, 2, or 5 mM) in 0.1 M phosphate buffer at pH 5.8 or 7.0; gold working electrode, 2 mm diameter (3.14 mm²); Pt-wire counter electrode; Ag/AgCl reference electrode (3 M KCl).
- **Operation/output:** three-electrode CV with an EG&G 264A potentiostat; potential recorded on a Rikadenki X–Y recorder. Scan rates were 5, 10, 20, 50, and 100 mV/s over −100 to +800 mV for the representative traces. Solutions were deoxygenated with Ar for 8 min; measurements were at room temperature. The reference potential was checked against a redox buffer before and after. The gold electrode was cleaned with abrasive zeolite powder and rinsed after each CV. Experiments were recorded in duplicate; means are reported.
- **Source locator:** accepted manuscript §2.2, pp. 4–5; §4.1, pp. 7–11; Figures 3 and 5; Table 1, pp. 7–8.
- **Linked findings:** FND-02, FND-03, FND-04, FND-06.

## EXP-03 — pH-dependent dopamine species-distribution calculation

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Type:** `ANALYSIS`
- **Technique:** acid-base species-distribution calculation
- **Subject/system:** dopamine species in aqueous solution as a function of pH
- **Inputs:** published dopamine pKa values pKa1 = 9.05, pKa2 = 10.58, and pKa3 = 12.07 from Sanchez-Rivera et al. [21]; CurTiPot version 4.2 [24]; pH range shown in Figure 2, with CV pH values 5.8 and 7.0 indicated.
- **Operation/output:** calculate species fractions as a function of pH and use the distribution to identify the dominant dopamine species discussed as available for initial oxidation.
- **Source locator:** accepted manuscript §3, pp. 5–7; Figure 2 caption, p. 6.
- **Provenance / uncertainty:** pKa values were measured at 20 °C, dopamine concentration 0.125 mM, and ionic strength 0.5 M NaCl. The manuscript does not establish those conditions as identical to the CV solutions. The exact calculation input file is not reported.
- **Linked findings:** FND-01, FND-04.

## EXP-04 — Air-exposed dopamine auto-oxidation demonstration

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Type:** `TREATMENT`
- **Technique:** air-exposed solution aging with qualitative visual observation
- **Subject/system:** dopamine solutions at pH 5.0, 6.1, 6.5, and 7.0
- **Inputs:** dopamine solutions; exact concentration and full preparation details for this demonstration are not specified in the reported figure/text.
- **Operation/output:** the manuscript describes air auto-oxidation in the pH range 5.8–7.0. Figure 4 describes dopamine auto-oxidation and shows solution appearance at pH 5.0, 6.1, 6.5, and 7.0 after 24 h and 96 h at room temperature. The text's stated air-oxidation range starts at pH 5.8, while the figure includes pH 5.0; retain this scope difference and do not infer identical exposure details for every solution.
- **Parameters:** pH=5.0, 6.1, 6.5, 7.0; exposure=air; elapsed time=24 h and 96 h; temperature=room temperature; concentration=not reported for this demonstration; replicate count=not reported.
- **Source locator:** accepted manuscript §4.1 and Figure 4 caption/image, pp. 9–10.
- **Linked findings:** FND-05.
