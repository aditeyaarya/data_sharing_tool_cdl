# CDL Intake UI (Streamlit)

A minimal, modular Streamlit app to collect CDL meeting metadata with required-field enforcement and CSV persistence.

## Features
- Required fields: Date, Stream, Founder name, Venture name, Venture manager name, Link
- Optional: Comments
- Submit button stays **disabled** until all required fields are valid
- Validated URL (quick pre-check + strict Pydantic `HttpUrl`)
- Appends submissions to `data/entries.csv`

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py