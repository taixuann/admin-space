# Paper map — fixture revision GOLD-2

## Scope and contribution

Schindler and Bechtold study the initial anodic oxidation of dopamine on a gold electrode near physiological pH. The paper combines cyclic voltammetry at pH 5.8 and 7.0 with a pH-dependent species-distribution calculation. Its central contribution is a proposed fast, reversible one-electron oxidation followed by deprotonation to a semiquinone radical; later reactions are proposed to depend on pH. This is a mechanistic proposal from electrochemical observations, not direct identification or isolation of the radical.

## Study map and routes

- **Context and question** — Introduction, accepted-manuscript pp. 2–3. Prior literature proposes multiple oxidation pathways; the study targets the first anodic step and a radical-based alternative.
- **Materials and solution preparation** — §2.1, pp. 4–5; see EXP-01. Dopamine hydrochloride, phosphate buffer at pH 5.8 and 7.0, buffer/reagent details, and freshly prepared dopamine solutions are reported. The abstract uses “phosphate buffered saline,” while the methods/results/captions mostly say “phosphate buffer”; the exact NaCl content of every CV solution is not consistently explicit. Preserve this wording uncertainty when comparing ionic-strength-sensitive results.
- **Electrochemical protocol** — §2.2, pp. 4–5; see EXP-02. Three-electrode CV, Au working electrode (2 mm diameter; 3.14 mm²), Pt-wire counter, Ag/AgCl (3 M KCl) reference, argon deoxygenation for 8 min, room temperature, dopamine 0.5/2/5 mM, pH 5.8/7.0, scan rates 5/10/20/50/100 mV/s, duplicate measurements and means. Reference potential was checked before and after measurements.
- **Species calculation** — §3, pp. 5–7; see EXP-03 and FND-01. The plotted distribution uses pKa values (9.05, 10.58, and 12.07) from Sanchez-Rivera et al. [21] and CurTiPot v4.2 [24]. The cited pKa measurement conditions differ from this study's CV conditions; the distribution is not a direct measurement in the CV cell.
- **Results and data** — §4.1, pp. 7–11; Figures 3–5, pp. 9–11; Table 1, pp. 7–8; see FND-02, FND-03, and FND-05. CV peak positions/currents and pH-dependent visual auto-oxidation are reported. Figure 5 shows anodic peak current against square root of scan rate with two repetitions and standard-deviation bars. EXP-04 captures the Figure 4 auto-oxidation demonstration, including the source's different stated pH ranges.
- **Interpretation** — §§4.1–4.3 and §5, pp. 11–15; Figure 6, p. 12, and Figure 7, p. 14; see FND-04, FND-06–FND-08. The proposed semiquinone and dimerization route is an author interpretation. The paper notes rapid follow-up chemistry, a diffusion-layer reaction location, and difficulty isolating individual products.

## Figure and table inventory

All seven figures and Table 1 are present in the approved PDF and classified `MATERIAL` for this fixture. Figures 3–5 and Table 1 are material result evidence; Figure 4 documents the pH/time-dependent auto-oxidation visual result. Figures 1, 2, 6, and 7 provide material chemical/speciation/mechanism context. The relevant panels and axes were visually checked in the PDF; captions alone were not used as visual verification. No supplement is cited in the accepted manuscript. All 29 bibliography entries are accounted for in `reference-map.md`; cited works are not treated as direct current-paper evidence.

## Coverage limits and interpretation guardrails

- Report that the paper studied the accepted-manuscript version; do not silently substitute the final typeset article.
- Do not call the semiquinone directly observed or structurally identified. Distinguish measured CV peaks, the calculated species distribution, and the authors' proposed mechanism.
- Keep the duplicate count (`n = 2`) and conditions attached to numerical CV findings where reported.
- Preserve the phosphate-buffer/PBS wording ambiguity; do not infer a 0.5 M NaCl content for the CV solutions.
- The pH-speciation calculation imports published pKa values determined under different stated temperature/concentration/ionic-strength conditions. This limits direct quantitative transfer to the CV experiment.
- Figure 4's caption gives pH and elapsed time, but the article does not fully specify every solution/preparation detail for that visual demonstration. No unreported concentration or replicate count is added.

## Object routes

- Process narrative routes to `EXP-01` (reagents/buffers/solutions), `EXP-02` (CV), and `EXP-03` (species calculation).
- Figure 5's reversibility inference routes to `FND-03` and `EXP-02`.
- Table 1's pH comparison routes to `FND-02` and `EXP-02`.
- Figure 4's qualitative auto-oxidation evidence routes to `FND-05`; the pH-dependent follow-up interpretation routes to `FND-08`.
- The proposed semiquinone pathway routes to `FND-04`; it remains `INTERPRETED` rather than `OBSERVED`.
- The observed scan-rate relation routes to `FND-03`, while its reversibility interpretation routes to `FND-07`.
- The observed cathodic-current comparison routes to `FND-06`, while the faster-follow-up explanation routes to `FND-08`.
