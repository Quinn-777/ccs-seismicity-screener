# CO₂ Storage — Induced Seismicity Risk Screener

A semi-quantitative screening tool that estimates induced-seismicity risk for CO₂ geological storage sites using only geological parameters available **before** injection begins.

**Live app:** http://localhost:8501

---

## Why this exists

Most existing induced-seismicity tools (ORION, TOUGH-FLAC, ECLIPSE) require operational data — injection rate, pressure, volume — which by definition does not exist before a site starts injecting. That leaves a gap at the earliest and cheapest decision point: screening candidate sites during pre-injection characterization.

This tool implements a framework I developed for an AP Research paper, which scores a site using eight geological parameters drawn from peer-reviewed literature, each with a threshold and a weight. It is intended as a *screening* aid — a way to rank and flag candidate sites — not a replacement for site-specific geomechanical modeling.

## The scoring formula

Each parameter contributes a determination value `d` based on its risk level, weighted by `w`, and gated by an availability flag `a`:

```
Risk Score (%) = Σ(aᵢ · wᵢ · dᵢ) / Σ(aᵢ · wᵢ) × 100
```

- `d` = 1 (high risk), 0.5 (moderate), 0 (low)
- `w` = 2 for primary parameters, 1 for secondary
- `a` = 1 if data is available, 0 if not

Missing parameters are excluded from **both** the numerator and the denominator. This means absent data reduces the number of contributing parameters rather than biasing the score up or down — a site with five known parameters is still scored meaningfully.

## Parameters and thresholds

| Parameter | Level | w | Threshold | Source |
|---|---|---|---|---|
| Fault permeability | primary | 2 | <1 mD → high · 1–100 mD → moderate · >100 mD → low | Cao et al. (2025) |
| Fluid pathways | primary | 2 | pathway present → high · absent → low | Oye et al. (2022) |
| Fault roughness | secondary | 1 | rough/immature → high · smooth/mature → low | Wang et al. (2024) |
| Fault size / length | primary | 2 | <200 m → low · 200–1000 m → moderate · ≥1000 m → high | Rutqvist et al. (2016) |
| Fault continuity | primary | 2 | continuous → high · heterogeneous → low | Rutqvist et al. (2016) |
| Stress state | primary | 2 | µmob ≥ 0.6 → high · <0.6 → low | Vilarrasa et al. (2019) |
| Proximity to basement | primary | 2 | <1 km → high · ≥1 km → low | Skoumal et al. (2018) |
| Caprock integrity | secondary | 1 | <50 m → high · ≥50 m → low | CO₂CRC et al. (2013) |

## Validation

The framework was tested retrospectively against three injection projects:

| Site | Risk Score | Recorded events | Mmax |
|---|---|---|---|
| Illinois Basin-Decatur | 61.54% | 221 | 1.2 |
| In Salah | 50.00% | 9506 | 1.7 |
| Basel | 85.71% | 10500 | 3.4 |

Predicted ranking: Basel > Illinois > In Salah.
Observed ranking: Basel > In Salah > Illinois.

**The framework correctly identifies Basel as highest risk but inverts the Illinois / In Salah pair.** This inversion is stable — it persists under an equal-weighting scheme and under sensitivity analysis excluding every parameter with a contested evidence basis, which suggests it reflects a property of the framework rather than one questionable data point.

One likely factor: "number of recorded earthquakes" may measure monitoring network density and recording duration as much as it measures hazard. In Salah recorded 9506 events against Decatur's 221, but the two sites differ substantially in instrumentation. Choosing a validation metric that is not confounded by detectability is an open problem for this framework.

### Known limitations

- Basel is an Enhanced Geothermal System (water injection), not a CO₂ storage project. It is included because it is one of the few well-documented injection-induced seismicity sequences with felt events, but the fluid properties and reservoir mechanics differ from supercritical CO₂ injection.
- Three case studies is a small validation set.
- Several parameters were assigned from qualitative descriptions in the literature rather than measured values that could be tested against a threshold directly.
- Primary/secondary assignment is based on the descriptive verbs authors use ("determine" vs. "influence"), which involves judgment.

## Repository structure

```
seismic_score.py    Scoring engine, threshold classifiers, and test suite
app.py              Streamlit web interface
[ccs_tool.py]       Command-line version
```

The scoring logic is kept separate from the interface so that the same tested code backs both the CLI and the web app, and so the thresholds can be changed without touching the formula.

## Running it

**Web app:**
```bash
pip install streamlit
streamlit run app.py
```

**Command line:**
```bash
python ccs_tool.py
```

**Tests:**
```bash
python seismic_score.py
```

The test suite covers threshold boundary values, the categorical classifiers' fallback behavior, the formula's behavior at 0% / 100% / all-missing, and all three validation cases.

## Notes on corrections

Building this tool surfaced several errors in the original paper, which are corrected here:

- **Fault permeability direction** was stated inconsistently — the Method section had the threshold reversed relative to Table 1 and to the underlying mechanism (low-permeability faults accumulate pressure and are more slip-prone).
- **Fault roughness direction** was reversed. Wang et al. (2024) report more numerous and larger acoustic-emission events with lower b-values on rough faults, so rough/immature is the higher-risk case.
- **In Salah stress state** was scored as contributing to the numerator despite being classified as low risk (µ = 0.4 < 0.6), an arithmetic error. Corrected, In Salah scores 50.00% rather than 64.29%.

## Author

Qiuhe Gao · 2026

Built as an extension of an AP Research investigation into geological screening for CO₂ storage.
