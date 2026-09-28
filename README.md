# PharmEasy Regional Pulse Pipeline

**1. Headline Finding:** Guntur experienced a massive anomalous order surge, resulting in a +122.19% Month-on-Month sales increase from April to May 2026.

**2. Repository Artifacts:**
* **app.py**: Streamlit dashboard — live data exploration.
* **Embedded CII narrative**: Embedded in the dashboard — what the data means.
* **memo.md**: One-page memo — the recommendation.
* **presentation_storyline.md**: Presentation storyline — how you'd defend it live.

**3. Recommended Review Order:** 
1. `app.py` (Dashboard) -> 2. `memo.md` -> 3. `presentation_storyline.md`

**4. Key Unverified Assumption:** The Guntur growth spike is assumed to be driven by sustainable organic demand rather than a one-time data duplication error upstream of the raw export. 

---

## Setup and Execution Instructions

To run this pipeline end-to-end, open your terminal in this repository's folder and execute the following 3 commands in order:

**1. Generate and Clean the Data:**
```bash
python generate_dataset.py && python clean_data.py

**2. Build the SQLite Metrics Engine:**
```bash
python build_db.py && python queries.py

**3. Launch the Dashboard:**
```bash
pip install pandas streamlit plotly
streamlit run app.py