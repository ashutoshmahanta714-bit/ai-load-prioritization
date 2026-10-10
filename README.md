# Adaptive Load Prioritization — research prototype v0.1

Prepared for Ashutosh Mahanta from the supplied seed-fund proposal slides.

## What works
- Configurable criticality, efficiency and stability scores.
- Weighted ranking and budget-constrained allocation.
- Full/zero switching and partial allocation for controllable loads.
- Streamlit dashboard with editable loads and CSV export.
- Reproducible 96-step simulation and fixed-criticality comparator.
- Offline random-forest demand forecast using explicitly synthetic data.
- Allocation tests including 1,000 randomized supply budgets.

## Windows quick start
Extract this folder. Open Command Prompt in the extracted folder.
Use your installed Python 3.12:

    py -3.12 -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r requirements.txt
    python -m streamlit run app.py

Other commands:

    python -m unittest test_controller.py
    python simulate.py
    python forecast.py

The default dashboard reproduces: hospital 25 kW, pump 20 kW,
residential 25 kW, shops zero, streetlights zero at 70 kW supply.
All priorities and weights are illustrative, not calibrated site values.

## Model and control distinction
The weighted score is a deterministic baseline, not a trained AI model.
The random forest forecasts the next interval's total demand from previous
values and time features. It is an offline experiment, not a deployed
controller. A real integration needs site data and validation first.
Evaluation uses a chronological split and a persistence baseline.
Synthetic forecast accuracy cannot demonstrate real-world performance.

## Limitations
The example is a greedy ranking heuristic, not a globally optimal multi-objective
optimizer. It does not model feeder topology, power flow, inrush, storage,
voltage/frequency dynamics, minimum service, fairness or switching dwell time.
The two ranking methods may give identical results; no improvement is claimed.
Critical coverage is served demand / demand for loads with criticality >=0.8.
Controllable=True assumes continuously reducible demand, which must be checked
for each real device. Every changing interval is recalculated in simulation;
there is no live sensor connection or automatic physical switching.
No hospital or utility control is authorized or suitable with this prototype.

## Next stages
1. Demonstrate the low-voltage indicator prototype described in HARDWARE.md.
2. Collect timestamped demand, supply, load type and switching measurements.
3. Replace synthetic training data and validate across operating conditions.
4. Add electrical/network constraints, essential-service limits, hysteresis,
   minimum on/off times, operator override and communication-failure behavior.
5. Perform hardware-in-loop and supervised lab tests before site trials.

Streamlit setup reference:
https://docs.streamlit.io/get-started/installation/command-line

## Streamlit Community Cloud
Select this repository, branch `main`, and entrypoint `app.py`.
Choose Python 3.12 in Advanced settings. No secrets are required.
