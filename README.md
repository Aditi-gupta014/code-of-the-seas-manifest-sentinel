# Manifest Sentinel — Code of the Seas

## How to run
```bash
pip install -r requirements.txt
python generator.py
python injector.py
python detector.py
streamlit run app.py
```

## Pipeline
Clean baseline -> controlled tampering -> suspect manifest -> rule checks + statistical anomaly detection -> evidence score -> classification -> reconstruction labels -> dashboard.

## Seed
42

## Important
`private_injection_log.csv` is the answer key for evaluation only. The detector never reads it.

## Environment variables
None required.

## Files
- generator.py: generates clean synthetic manifest
- injector.py: creates realistic corruption and private truth
- detector.py: detection + explanation + reconstruction labels
- app.py: Streamlit dashboard
