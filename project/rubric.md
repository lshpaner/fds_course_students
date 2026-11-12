# Final Project Rubric (25 points)

Score each row 0 to its maximum. Half points allowed. Comments required for any row scored below half.

| # | Criterion | 0 | Half | Full | Max |
|---|---|---|---|---|---|
| 1 | **Decision framing** | no decision-maker named, or the question is "predict X" | decision named but costs of error not stated | who decides, what changes, and what each error costs, stated in the first paragraph | 3 |
| 2 | **Data handling** | joins and missing-data choices undocumented | choices made but assumptions (MCAR/MAR/MNAR) not stated | every join and imputation choice written down with its assumption and a sensitivity check | 3 |
| 3 | **Uncertainty** | point estimates only | intervals on some headline numbers | every headline number has an interval, by formula or bootstrap, and the text reads the interval not the point | 2 |
| 4 | **EDA and findings log** | modeling started without exploration | EDA done but not connected to the model | findings log present, hypotheses tested in later sections, at least one confounder checked | 2 |
| 5 | **Communication chart** | default plot, no title sentence | clean plot, generic title | finding-as-title, honest axes, source line, readable by the decision-maker without the text | 2 |
| 6 | **Baseline and model** | no baseline | baseline present, gap not discussed | cost-free baseline reported; chosen model justified by the size of its gain against its complexity | 3 |
| 7 | **Evaluation** | in-sample or random split on time data | held-out but default cutoff and no interval | held out correctly, operating point chosen from the decision, bootstrap interval, baseline comparison on the same test set | 3 |
| 8 | **Fairness** | no per-group analysis | per-group table, no interpretation | per-group metrics with intervals, which criterion was chosen and what it traded, who bears the cost of errors | 2 |
| 9 | **Recommendation** | none, or restates the model metrics | recommendation present but in model units | stated in the decision-maker's units with the trade-off visible ("flags 43%, catches 80%, 3.4 tests per case") | 2 |
| 10 | **Reproducibility** | notebook does not run; data committed | runs with manual steps | fetch script, gitignored data, runs top to bottom from raw, README with setup steps, all members in the git log | 3 |

**Talk (part of row 9 and 5):** 12 minutes, hard stop. One chart per claim. The decision-maker's question answered in the first two minutes and the last one.

**Automatic deductions:** committed data files (-2), notebook does not execute (-3), no team member can explain a method used (-2 per method).