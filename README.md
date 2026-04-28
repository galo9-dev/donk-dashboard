# donk Dashboard 🎯

Interactive dashboard analyzing the career statistics of Danil 'donk' Kryshkovets, widely considered the best CS2 player in the world.

## Live Demo
[donk-dashboard on Streamlit Cloud](https://donk-dashboard-m2yrvk8hxdkufmzlrbjfkk.streamlit.app)

## What it shows
- Career overview with key performance metrics (Rating, KPR, tournaments won)
- Rating 2.0 evolution across all tournaments with Spirit
- Kill difference (+/-) per tournament
- KPR vs DPR comparison over time
- Average rating per year
- List of all tournaments won with Spirit
- Filter by tournament type: All, Majors, IEM, BLAST

## Technologies
- Python, Pandas, Plotly, Streamlit

## Dataset
Data manually collected from HLTV.org — covers all 58 tournaments played with Team Spirit from 2023 to 2026, including Rating 2.0, KPR, DPR, and kill differential per event.

## How to run locally
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `streamlit run src/app.py`