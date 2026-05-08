# Storytelling using Data Visualization — Instructor-Led Streamlit Teaching App

A classroom-ready, one-stop Streamlit application for the PGDM-BDA course **Storytelling using Data Visualization** at Goa Institute of Management.

This project is designed for live teaching, guided practice, classroom discussion, case analysis, visual critique, formative assessment, and final workshop delivery. The app is intended to replace the need for separate PPT decks, handouts, or external teaching notes during regular class delivery.

> **Core idea:** students should not merely create attractive charts; they should learn how to convert data into clear, ethical, persuasive, and decision-oriented visual stories for managerial audiences.

---

## Current Version

**v9 — Instructor-only teaching version**

### v9 updates

- Removed Student Mode completely.
- App now runs in instructor-only mode.
- Replaced the previous live-teaching prompt label with **Theoratical Concepts** across the visible interface.
- Retained projector-friendly mode for classroom delivery.
- Retained complete teaching support: examples, diagrams, charts, flowcharts, activities, quizzes, business cases, model answers, right/wrong interpretations, and misinterpretation-versus-clarification notes.

---

## Instructor Handbook

A complete instructor handbook is included in this repository:

- [Open the Instructor Handbook](HANDBOOK.md)

The handbook explains how to use the app session by session, how to conduct activities, how to use the case solutions, how to run the final workshop, and how to assess student outputs.

---

## Course Alignment

The app supports the PGDM-BDA Term 1 course **Storytelling using Data Visualization**.

### Course Learning Outcomes

| CLO | Outcome |
|---|---|
| CLO1 | Explain the role of data visualization in presenting analytics-driven solutions to management problems. |
| CLO2 | Select and design appropriate charts, dashboards, and visual layouts for different business contexts and stakeholder needs. |
| CLO3 | Construct coherent and decision-oriented narratives from data using visualization tools and storytelling frameworks. |
| CLO4 | Communicate business insights and strategic recommendations effectively through visual stories. |

---

## What the App Includes

### Teaching delivery

- Instructor-only delivery environment
- Projector-friendly mode
- Course roadmap
- CLO-aligned session structure
- 75-minute teaching flow for every session
- Session-wise teaching notes
- **Theoratical Concepts** section for instructor notes
- **Tell me the story** feature for narrative explanation
- Ready-to-use examples and classroom explanations
- Flowcharts, diagrams, and visual reasoning paths

### Visual learning tools

- Interactive visual demonstrations
- Chart Selection Engine
- Visualization Master Gallery
- Before–After Visual Makeover Studio
- Misleading Chart Clinic
- Dashboard Design Studio
- Storytelling Framework Builder
- Annotation and Title Lab
- Upload and Auto-Story Lab
- Final Integrated Workshop

### Practice and assessment

- Large quiz bank with reveal-answer explanations
- Activity Bank with model solutions
- Business Case Library with complete case solutions
- Business Role-Play Mode
- Rubrics and Exam Question Bank
- Downloadable datasets, reflections, teaching notes, case solutions, and story drafts

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

Use a fresh virtual environment. Avoid running the app directly from the base Anaconda environment if it has PyArrow/protobuf conflicts.

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
- openpyxl, for Excel upload support

No API keys, paid services, or external datasets are required.

---

## Recommended Classroom Workflow

Use the app in this sequence for each 75-minute class:

1. Open **Instructor Delivery Planner** for the session flow.
2. Move to **Session Learning Studio**.
3. Use **Theoratical Concepts** for conceptual framing.
4. Use **Tell me the story** for narrative explanation.
5. Show the diagram or flowchart.
6. Run the interactive demo.
7. Conduct the mini-lab or activity.
8. Reveal the model solution and discuss misinterpretations.
9. Use quiz questions for formative checking.
10. Close with reflection and action-oriented takeaway.

---

## Recommended Repository Structure

```text
storytelling_using_data_visualization/
├── app.py
├── requirements.txt
├── README.md
└── HANDBOOK.md
```

---

## Notes for Instructors

- The app is designed for live classroom projection.
- Built-in synthetic datasets are generated inside the app.
- Dataset downloads are available as CSV.
- The app supports teaching, revision, case discussion, and assessment preparation.
- Instructors can use the built-in rubrics and model answers to evaluate student outputs consistently.

---

## Instructor

**Dr. Alok Tiwari**  
Assistant Professor — Big Data Analytics  
Goa Institute of Management, Goa
