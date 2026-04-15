<h1>🚀 Hiring Process Bottleneck Analyser</h1>
An interactive Streamlit application designed to help HR teams and Talent Acquisition managers identify inefficiencies in their recruitment pipeline. This tool automates the calculation of cycle times and visualizes candidate attrition to drive data-led hiring decisions.

<h1>📊 Project Overview</h1>
Recruitment is often slowed down by invisible bottlenecks. This application allows users to upload their own hiring data and set custom benchmarks to instantly see where the process is lagging.
Key Metrics Tracked:
Total Candidates: 200 in the current pipeline.
Average Total Hire Time: 27.7 days from application to joining.
Hiring Rate: 68 successful hires (34.0% of applicants).
Offer Acceptance Rate: 84.0% (68 of 81 offers accepted).

<h1>🛠️ Features</h1>
<b>Dynamic Benchmark Settings</b>
Users can adjust expected days for each recruitment stage using interactive sliders:
<ul>Application → Screening: 5 days </ul>
<ul>Screening → Interview 1: 4 days </ul>
<ul>Interview 1 → Interview 2: 3 days </ul>
<ul>Interview 2 → Offer: 4 days </ul>
<ul>Offer → Joining: 14 days </ul>

<b>Automated Bottleneck Detection</b>
The app compares actual performance against user-defined benchmarks to flag critical delays:
<ul>Primary Bottleneck Detected: Offer → Joining is averaging 20.6 days (6.6 days over the 14-day target).</ul>
<ul>Secondary Bottleneck: Application → Screening is averaging 11.2 days (6.2 days over the 5-day target).</ul>

<b>Candidate Funnel Visualization</b>
A Plotly-powered funnel chart tracks candidate drop-offs at every stage:
Biggest Drop-off Point: Interview 1, where 75 candidates were lost (37.5% of total).

<h1>🏗️ Tech Stack</h1>
Language: Python
Data Manipulation: Pandas
Visualization: Plotly
Web Framework: Streamlit

<h1>📂 Data Input</h1>
The application accepts Excel (.xlsx) files. A sample dataset, hiring_bottleneck_dataset_200.xlsx, is provided in the repository to demonstrate the required schema.

<h1>💡 How to Run</h1>
Clone the repository.
Install dependencies: pip install -r requirements.txt.
Run the app: streamlit run app.py.


Built by Aarthi as part of the Hiring Process Bottleneck Analysis project.
