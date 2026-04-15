🚀 Hiring Process Bottleneck Analyser
An interactive Streamlit application designed to help HR teams and Talent Acquisition managers identify inefficiencies in their recruitment pipeline. This tool automates the calculation of cycle times and visualizes candidate attrition to drive data-led hiring decisions.

📊 Project Overview
Recruitment is often slowed down by invisible bottlenecks. This application allows users to upload their own hiring data and set custom benchmarks to instantly see where the process is lagging.
Key Metrics Tracked:
Total Candidates: 200 in the current pipeline.
Average Total Hire Time: 27.7 days from application to joining.
Hiring Rate: 68 successful hires (34.0% of applicants).
Offer Acceptance Rate: 84.0% (68 of 81 offers accepted).

🛠️ Features
1. Dynamic Benchmark Settings
Users can adjust expected days for each recruitment stage using interactive sliders:
Application → Screening: 5 days 
Screening → Interview 1: 4 days 
Interview 1 → Interview 2: 3 days 
Interview 2 → Offer: 4 days 
Offer → Joining: 14 days 

2. Automated Bottleneck Detection
The app compares actual performance against user-defined benchmarks to flag critical delays:
Primary Bottleneck Detected: Offer → Joining is averaging 20.6 days (6.6 days over the 14-day target).
Secondary Bottleneck: Application → Screening is averaging 11.2 days (6.2 days over the 5-day target).

3. Candidate Funnel Visualization
A Plotly-powered funnel chart tracks candidate drop-offs at every stage:
Biggest Drop-off Point: Interview 1, where 75 candidates were lost (37.5% of total).

🏗️ Tech Stack
Language: Python
Data Manipulation: Pandas
Visualization: Plotly
Web Framework: Streamlit

📂 Data Input
The application accepts Excel (.xlsx) files. A sample dataset, hiring_bottleneck_dataset_200.xlsx, is provided in the repository to demonstrate the required schema.

💡 How to Run
Clone the repository.

Install dependencies: pip install -r requirements.txt.

Run the app: streamlit run app.py.


Built by Aarthi as part of the Hiring Process Bottleneck Analysis project.
