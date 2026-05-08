# Storytelling using Data Visualization — One-Stop Streamlit Teaching App v7

This is a classroom-ready Streamlit app for the PGDM-BDA course **Storytelling using Data Visualization**.

It is designed to replace PPT-based delivery and provide a single interactive teaching environment with explanations, diagrams, live visualizations, quizzes, activities, business cases, storytelling builders, role play, rubrics, exam preparation, upload-based exploration, and final workshop tools.

## New in v7

- Removed transcript-style delivery wording and kept the app in clean Instructor / Student delivery modes.
- Added **complete model solutions for every business case** with evidence, recommendation, limitation, and expected student answer.
- Added model-solution guidance in the Activity Bank, Visual Makeover Studio, Upload and Auto-Story Lab, and Final Integrated Workshop.
- Added **Instructor Mode / Student Mode** toggle.
- Added **Projector-friendly mode** for larger classroom display.
- Added **Instructor Delivery Planner** with complete 75-minute teaching flow for each session.
- Added **What should I say now?** prompts for live teaching moments.
- Added **Before–After Visual Makeover Studio** for weak-to-strong chart redesign.
- Added **Rubrics and Exam Question Bank** with model answers and CSV export.
- Added **Upload and Auto-Story Lab** for CSV/Excel files.
- Added **Business Role-Play Mode** for CEO, finance, operations, marketing, and analyst perspectives.
- Added downloadable **session teaching notes** and delivery plans.
- Retained v5/v6 features: Tell me the story, expanded quiz bank, activity bank, visualization gallery, final workshop, no-PyArrow table rendering, and timestamp-safe Plotly markers.

## Main Sections

1. Home
2. Course Roadmap
3. Instructor Delivery Planner
4. Session Learning Studio
5. Chart Selection Engine
6. Visualization Master Gallery
7. Before–After Visual Makeover Studio
8. Misleading Chart Clinic
9. Dashboard Design Studio
10. Storytelling Framework Builder
11. Annotation and Title Lab
12. Business Case Library
13. Business Role-Play Mode
14. Activity Bank
15. Quiz Zone
16. Rubrics and Exam Question Bank
17. Upload and Auto-Story Lab
18. Final Integrated Workshop
19. Resources

## Installation

Use a fresh virtual environment. Avoid running from the base Anaconda environment if it has PyArrow/protobuf conflicts.

### macOS / Linux

```bash
cd storytelling_streamlit_app_one_stop_v7
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### Windows

```bash
cd storytelling_streamlit_app_one_stop_v7
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Dependencies

The app uses no-cost/open-source Python libraries:

- streamlit
- pandas
- numpy
- plotly
- openpyxl, only for Excel upload support

## Notes

- No API calls.
- No paid tools.
- External datasets are optional; built-in synthetic datasets are generated inside the app.
- Dataset downloads are available as CSV from the app.
