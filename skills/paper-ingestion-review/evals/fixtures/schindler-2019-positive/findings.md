# Paper Findings — fixture revision GOLD-2

All IDs and revisions are fixture-local. Each statement is limited to the accepted manuscript and preserves the distinction between observation, calculation, and author interpretation.

## FND-01 — Dominant calculated dopamine species at the two CV pH values

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Origin / Evidence Mode:** `CURRENT_PAPER` / `DERIVED`
- **Type:** speciation result
- **Evidence Kind:** calculated species distribution
- **Claim:** Using published pKa inputs [21] and CurTiPot [24], the paper's calculated distribution identifies fully protonated I-DPAH3+ as the dominant dopamine species at pH 5.8 and pH 7.0.
- **Conditions / limits:** the pKa source used 20 °C, 0.125 mM dopamine, and ionic strength 0.5 M NaCl; transfer to the CV conditions is assumed by the paper and is not a direct in-cell species measurement.
- **Locator / lineage:** accepted manuscript §3 and Figure 2, pp. 5–7; EXP-03; references R021 and R024.

## FND-02 — Anodic peak-current comparison at 5 mM dopamine

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Origin / Evidence Mode:** `CURRENT_PAPER` / `OBSERVED`
- **Type:** quantitative electrochemical result
- **Evidence Kind:** tabulated and plotted current measurement
- **Claim:** At 5 mM dopamine and 50 mV/s, the reported anodic peak-current magnitudes are approximately 41 µA at pH 5.8 and 48 µA at pH 7.0 (reported signed values −41 and −48 µA).
- **Conditions / uncertainty:** Au electrode (3.14 mm²); phosphate medium wording as reported; means of duplicate measurements (`n = 2`). The article describes only a modest difference between pH conditions; do not interpret this comparison alone as a mechanism test.
- **Locator / lineage:** accepted manuscript §4.1, p. 9; Table 1, pp. 7–8; EXP-02.

## FND-03 — Anodic peak-current relation to scan rate

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Origin / Evidence Mode:** `CURRENT_PAPER` / `DERIVED`
- **Type:** scan-rate relation
- **Evidence Kind:** relation derived from plotted current data
- **Claim:** Figure 5 shows a linear relation between anodic peak current and square root of scan rate at both pH values.
- **Conditions / uncertainty:** three concentrations (0.5, 2, 5 mM), five scan rates (5–100 mV/s), Au electrode; plotted means of two repetitions with standard-deviation bars. The plotted relation is transcribed from Figure 5 and is not an independent reanalysis of raw data.
- **Locator / lineage:** accepted manuscript §4.1 and Figure 5, p. 11; EXP-02.

## FND-07 — Reversibility interpretation from the scan-rate relation

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Origin / Evidence Mode:** `CURRENT_PAPER` / `INTERPRETED`
- **Type:** electrochemical interpretation
- **Evidence Kind:** author interpretation of a plotted relation
- **Claim:** The authors use the linear anodic peak-current versus square-root-scan-rate relation to support an electrochemically reversible electron-transfer process.
- **Conditions / uncertainty:** interpretation of Figure 5 for the reported concentrations, pH conditions, and scan rates; it is not an independent reanalysis of raw voltammetry.
- **Locator / lineage:** accepted manuscript §4.1 and Figure 5, p. 11; EXP-02.
- **Derived From:** FND-03.

## FND-04 — Proposed one-electron/EC semiquinone pathway

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Origin / Evidence Mode:** `CURRENT_PAPER` / `INTERPRETED`
- **Type:** proposed mechanism
- **Evidence Kind:** author-proposed reaction pathway
- **Claim:** The authors propose that anodic one-electron oxidation of I-DPAH3+ forms a radical intermediate followed by deprotonation to a semiquinone; they propose dimerization as a possible subsequent route toward oligomeric precursors.
- **Conditions / uncertainty:** proposal for oxidation on Au in the studied pH 5.8–7.0 range. The radical was not directly isolated or structurally identified in this study; the paper itself notes difficulty identifying individual products.
- **Locator / lineage:** accepted manuscript §§4.2–4.3, pp. 11–13, and Figure 7, p. 14; EXP-02 and EXP-03; prior-work context R009, R018, R019, R021, and R025–R029.

## FND-05 — Qualitative time- and pH-dependent auto-oxidation appearance

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Origin / Evidence Mode:** `CURRENT_PAPER` / `OBSERVED`
- **Type:** qualitative visual result
- **Evidence Kind:** qualitative photographic observation
- **Claim:** Figure 4 presents dopamine solutions at pH 5.0, 6.1, 6.5, and 7.0 after 24 h and 96 h at room temperature; the accompanying text reports more visible colored/aggregated oxidation products at higher pH and little visible aggregation at pH 5 after four days.
- **Conditions / limits:** the figure caption supplies pH and elapsed times, but the full preparation details and replicate count for this visual demonstration are not fully specified. Do not quantify color or infer an unreported concentration.
- **Locator / lineage:** accepted manuscript §4.1 and Figure 4, pp. 9–10; EXP-01 and EXP-04.

## FND-06 — Lower cathodic peak-current magnitude at pH 7

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Origin / Evidence Mode:** `CURRENT_PAPER` / `OBSERVED`
- **Type:** quantitative electrochemical comparison
- **Evidence Kind:** tabulated cathodic peak-current measurement
- **Claim:** At 5 mM dopamine and 50 mV/s, the cathodic peak-current magnitude is reported to decrease from 23 µA at pH 5.8 to 3 µA at pH 7.0.
- **Conditions / uncertainty:** Au electrode; duplicate experiments; buffer/PBS wording uncertainty remains. This Finding records the current comparison only; the reaction-rate explanation is separate in FND-08.
- **Locator / lineage:** accepted manuscript §4.3, p. 13; Table 1; EXP-02.

## FND-08 — Faster follow-up chemistry interpretation of the lower cathodic current

- **Paper:** `PAPER-SCHINDLER-2019`
- **State:** `NEEDS_REVIEW`
- **Origin / Evidence Mode:** `CURRENT_PAPER` / `INTERPRETED`
- **Type:** electrochemical interpretation
- **Evidence Kind:** author interpretation of a cathodic-current comparison
- **Claim:** The authors interpret the lower cathodic peak-current magnitude at pH 7.0 as evidence that follow-up reactions consume anodically formed species more rapidly before the reverse scan than at pH 5.8.
- **Conditions / uncertainty:** the proposed reaction-rate explanation is the authors' interpretation of the reported CV comparison; it is not an independently measured reaction rate.
- **Locator / lineage:** accepted manuscript §4.3, p. 13; Table 1; EXP-02; FND-06.
- **Derived From:** FND-06.
