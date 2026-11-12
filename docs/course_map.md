# Foundations of Data Science: Course Map

Graduate level, one meeting per week, online or in person. Materials are Python/Jupyter (Colab-ready). Grading: assignments 30%, quizzes 25%, project 35%, participation 10%.

A single real dataset, the CDC's NHANES 2017-2018 survey, runs from week 1 through week 9 and returns in week 13, so students build one pipeline and keep extending it. Weeks 10 through 12 bring in a weekly flu series, a hospital contact network, and a text corpus.

| Wk | Topic | Dataset | Libraries introduced | Notebook | Assessment |
|---:|---|---|---|---|---|
| 1 | What data science is; the question/data/explore/model/decide loop; project brief | NHANES | pandas, eda_toolkit | `week_01_intro` | |
| 2 | Data handling: joins, skip patterns, missingness mechanisms, imputation | NHANES (4 components) | eda_toolkit | `week_02_data_handling` | HW1 posted |
| 3 | Statistics recap: distributions, CIs, bootstrap, survey weights, Table 1, effect sizes | NHANES | eda_toolkit, scipy | `week_03_statistics_recap` | HW1 due |
| 4 | Exploratory data analysis and confounding | NHANES | eda_toolkit | `week_04_eda` | Quiz 1; project problem statement |
| 5 | Visualization and communication | NHANES | matplotlib, seaborn | `week_05_visualization` | HW2 posted |
| 6 | Regression: adjusted comparisons, interactions, diagnostics, ridge | NHANES (SBP) | statsmodels, model_tuner, model_metrics | `week_06_regression` | HW2 due; Quiz 2; project pitches |
| 7 | Classification: logistic regression, trees, forests, boosting | NHANES (diabetes) | model_tuner, model_metrics, xgboost | `week_07_classification` | HW3 posted |
| 8 | Evaluation: cutoffs, ROC/PR, DeLong, calibration, bootstrap, the screening rule | NHANES (diabetes) | model_metrics, model_tuner | `week_08_evaluation` | HW3 due; Quiz 3 |
| 9 | Unsupervised: k-means, PCA, stability, hierarchical | NHANES | scikit-learn | `week_09_unsupervised` | HW4 posted |
| 10 | Time series: decomposition, autocorrelation, time-based splits, Holt-Winters, Fourier regression | CDC FluView weekly ILI | statsmodels | `week_10_time_series` | HW4 due; Quiz 4; HW5 posted |
| 11 | Networks: centrality, mixing, communities, spreading, temporal structure | SocioPatterns hospital ward | networkx | `week_11_networks` | |
| 12 | Language models: TF-IDF, embeddings, zero-shot prompting, evaluation discipline | 20 Newsgroups subset | scikit-learn, openai (optional) | `week_12_language_models` | HW5 due; Quiz 5; HW6 posted |
| 13 | Ethics and fairness: audit of the week 8 model by group | NHANES (diabetes) | equiboots | `week_13_fairness` | HW7 posted |
| 14 | Project presentations | | | | Project; HW6, HW7 due |

Guest lectures: 30-minute openers in weeks 6 through 12, speaker TBD.

## Assignments

| | Topic | Data | Status |
|---|---|---|---|
| HW1 | Joins and skip-pattern missingness | NHANES SMQ + BPQ | written, with solution key |
| HW2 | EDA findings log and two charts | student's project data | brief in week 5 notebook |
| HW3 | Regression: crude vs adjusted, interaction, diagnostics, ridge | project or NHANES SBP | brief in week 6 notebook |
| HW4 | Full classifier evaluation with a recommendation | project or NHANES | brief in week 8 notebook |
| HW5 | Decompose and forecast a weekly/monthly series; beat seasonal naive | project or FluView region | brief in week 10 notebook |
| HW6 | Text routing with an extension; cost per document | project or newsgroups | brief in week 12 notebook |
| HW7 | Re-run the fairness audit with HbA1c as the label | NHANES GHB_J | brief in week 13 notebook |