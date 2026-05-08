# Storytelling using Data Visualization — One-Stop Streamlit Teaching App v9

A classroom-ready, instructor-led Streamlit application for the PGDM-BDA course **Storytelling using Data Visualization** at Goa Institute of Management.

The app is designed as a **single teaching environment** for the course: explanations, diagrams, flowcharts, interactive graphs, quizzes, activities, business cases, model solutions, visual redesign exercises, rubrics, exam preparation, and final workshop support are all built into the application.

> **Teaching goal:** The instructor should be able to conduct the complete course without depending on a separate PPT, handout, or external teaching source.

---

## Current Version: v9

### Key updates in v9

- Removed Student Mode completely.
- The app now runs in **Instructor-only mode**.
- Replaced the earlier live-teaching prompt wording with **Theoratical Concepts** across the instructor interface.
- Retained projector-friendly mode for classroom delivery.
- Retained all full teaching supports: examples, graphs, flowcharts, diagrams, model answers, right/wrong interpretation, misinterpretation vs clarification, and downloadable notes.

---

## Handbook

A complete instructor handbook is included in this repository:

- [Open the Instructor Handbook](HANDBOOK.md)

The handbook explains how to use the app for session planning, live teaching, activities, quizzes, case discussions, final workshop delivery, and assessment.

---

## What the App Includes

### Teaching and delivery

- Instructor-only delivery environment
- Projector-friendly mode
- Course roadmap
- CLO-aligned session structure
- 75-minute teaching flow for every session
- Session-wise teaching notes
- Theoratical Concepts section for instructor notes
- Tell me the story feature for concept narration
- Ready-to-use examples and explanations
- Flowcharts, diagrams, and visual reasoning paths

### Interactive learning features

- Interactive visual demonstrations
- Chart selection engine
- Visualization master gallery
- Before–After Visual Makeover Studio
- Misleading Chart Clinic
- Dashboard Design Studio
- Storytelling Framework Builder
- Annotation and Title Lab
- Upload and Auto-Story Lab
- Final Integrated Workshop

### Practice and assessment

- Large quiz bank with reveal-answer explanations
- Activity bank with model solutions
- Business Case Library with complete case solutions
- Business Role-Play Mode
- Rubrics and Exam Question Bank
- Downloadable datasets, reflections, teaching notes, and solutions

---

## Main App Sections

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

---

## Installation

Use a fresh virtual environment. Avoid running from the base Anaconda environment if it has PyArrow/protobuf conflicts.

### macOS / Linux

```bash
git clone https://github.com/dr-alok-tiwari/storytelling_using_data_visualization.git
cd storytelling_using_data_visualization
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### Windows

```bash
git clone https://github.com/dr-alok-tiwari/storytelling_using_data_visualization.git
cd storytelling_using_data_visualization
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

---

## Dependencies

The app uses only no-cost/open-source Python libraries:

- streamlit
- pandas
- numpy
- plotly
- openpyxl, only for Excel upload support

---

## Recommended Classroom Use

Use the app in this sequence for each class:

1. Open **Instructor Delivery Planner** for the session flow.
2. Move to **Session Learning Studio**.
3. Use **Theoratical Concepts** for concept explanation.
4. Use **Tell me the story** for narrative explanation.
5. Run the interactive demo and diagram.
6. Conduct the mini-lab or activity.
7. Reveal model solution and clarify misconceptions.
8. Use quiz questions for formative checking.
9. Download or save teaching notes and reflections when needed.

---

## Notes

- No API calls.
- No paid tools.
- No external datasets required.
- Built-in synthetic datasets are generated inside the app.
- Dataset downloads are available as CSV from the app.
- The app is designed for classroom teaching, student practice, and assessment preparation.

---

## Instructor

**Dr. Alok Tiwari**  
Assistant Professor — Big Data Analytics  
Goa Institute of Management, Goa
