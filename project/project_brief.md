# Course Project

Teams of three. Thirty-five percent of the grade. You choose a problem where someone has a real decision to make, find public data that bears on it, and work the full loop: question, data, exploration, model, evaluation, recommendation.

## The one rule

**A problem with no decision attached will be sent back.** "Predict X because the data is there" is not a project. "The county has to decide where to put two new clinics; here is what the data say about where need is highest" is.

Your write-up must be able to answer, in its first paragraph: who decides, what changes depending on the answer, and what it costs to be wrong in each direction.

## Deliverables

| | When | What | Weight (of 35) |
|---|---|---|---|
| 1. Problem statement | chapter 4 | one page: the decision, who makes it, what data exists, what has been tried, the first two rows of your findings log | 5 |
| 2. Proposal pitch | chapter 6 | five-minute talk: the question, the data you have *actually loaded*, one summary table or plot, your plan and its risks | 5 |
| 3. Final notebook and talk | chapter 14 | a notebook that runs top to bottom from raw data, a 12-minute talk, and a two-page summary written for the decision-maker | 25 |

## What the final deliverable has to contain

Every item below maps to a chapter of the course, and the rubric scores each one.

1. **The decision** (chapter 1): who, what changes, cost of each error.
2. **Data handling** (chapter 2): how the data were obtained and joined; every missing-data decision, written down with the mechanism you assumed.
3. **Uncertainty** (chapter 3): every headline number carries an interval.
4. **EDA and the findings log** (chapter 4): what you saw before modeling, and which rows of the log you tested.
5. **One decision-maker chart** (chapter 5): the finding as the title, source line, honest axes.
6. **Modeling** (chapters 6 through 12, whichever apply): a baseline that costs nothing, the model you chose, and why the gap over the baseline is worth the complexity.
7. **Evaluation** (chapter 8): on held-out data, at the operating point the decision-maker would use, with a bootstrap interval, and a comparison to the baseline.
8. **Fairness** (chapter 13): per-group performance for whatever groups the decision touches, and one sentence on who bears the cost of each kind of error.
9. **The recommendation**: in the decision-maker's units, with the trade-offs visible.
10. **Reproducibility**: `make data_gen` style fetch script, gitignored data, a notebook that runs clean, a README that says how.

## Example problems

You may pick one of these or bring your own. Each has public data; part of the project is finding and vetting it.

- Which neighborhoods should a city prioritize for traffic-calming, given collision records? (city open-data portals: [LA](https://data.lacity.org/), [NYC](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95), [Chicago](https://data.cityofchicago.org/))
- Can a clinic predict which patients will miss appointments, and what would it do with the prediction? ([public no-show dataset](https://www.kaggle.com/datasets/joniarroba/noshowappointments); [NHANES](https://wwwn.cdc.gov/nchs/nhanes/) access-to-care modules)
- Where should a bike-share add docks, based on trip and station data? ([Citi Bike](https://citibikenyc.com/system-data), [Divvy](https://divvybikes.com/system-data), [Metro Bike Share](https://bikeshare.metro.net/about/data/))
- Which factors predict whether a Kickstarter campaign funds, and what should a creator change? ([Kaggle](https://www.kaggle.com/datasets/kemical/kickstarter-projects))
- Is air quality in a city improving, and does the answer depend on where you live? ([EPA AirNow](https://www.airnow.gov/), [OpenAQ](https://openaq.org/))
- When will the next flu season peak in a given HHS region, and how far ahead can a hospital plan staffing? ([CDC FluView via Delphi Epidata](https://cmu-delphi.github.io/delphi-epidata/api/fluview.html))
- Which hospital-ward staff should be prioritized for vaccination to slow an outbreak? (SocioPatterns contact networks)
- Does lab-measured diabetes (HbA1c) tell a different fairness story than self-reported diabetes? (NHANES `GHB_J`; extends chapter 13)

## Data rules

- Public data only. No scraping behind logins; no data with personal identifiers.
- Raw data fetched by script into a gitignored `data/` folder. If the fetch can't be scripted, document the manual steps and the download date.
- Cite the source and its license in the README.

## Team rules

- Every member commits code. The git log is part of the grade.
- One member presents each deliverable; rotate.
- Disagreements about scope come to the forum early. "We couldn't agree so we did both" is a scope failure, not a compromise.
