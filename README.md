# AI Construction Intelligence Dashboard

##  Project Overview
The AI Construction Intelligence Dashboard is a web-based analytics project built using Python and Streamlit. It helps in analyzing construction project performance by tracking delays, cost overruns, and predicting future delays using Machine Learning (Linear Regression).
This project provides interactive dashboards and visual insights to improve decision-making in construction management.
##  Features
-  Track multiple construction projects  
-  Analyze delay (Planned vs Actual days)  
-  Calculate cost overrun automatically  
-  AI-based delay prediction using Machine Learning  
-  Interactive charts using Plotly  
-  Add new projects dynamically  
-  Download updated dataset as CSV
  
## ⚙️ Tech Stack
- Python  
- Streamlit  
- Pandas  
- Plotly   
- Scikit-learn 
  
## Machine Learning Model
- Algorithm: Linear Regression  
- Input Features:
  - Planned Days  
  - Budget  
- Output:
  - Predicted Delay
    
## Dataset Structure
The project uses a CSV file (`projects.csv`) with the following columns:
- PROJECT_ID  
- PROJECT_NAME  
- PLANNED_DAYS  
- ACTUAL_DAYS  
- BUDGET  
- ACTUAL_COST  
- DELAY  
- COST_OVERRUN
   
##  How to Run the Project
1. Install Dependencies
    pip install streamlit pandas plotly scikit-learn
2.Run the App
    streamlit run app.py
3.Open in Browser
     http://localhost:8501
