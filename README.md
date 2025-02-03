# MetroMind – A safety net for metro travelers
## Inspiration

Metro incidents are a common challenge faced by urban commuters, leading to delays, stress, and productivity loss. Inspired by the vision of smarter and more reliable public transit, we created MetroMind to leverage AI and data analytics in solving real-world transportation issues. Our goal is to provide commuters with better planning tools and transit operators with actionable insights for improved service reliability.

## What It Does

MetroMind is an AI-powered predictive analytics dashboard that:

- Forecasts metro disruptions in real-time using a Multilayer Perceptron (MLP) model.
- Displays historical metro incident data and trends in an intuitive format.
- Helps commuters make informed decisions about alternate routes or departure times.
- Supports metro management in identifying peak disruption hours and planning resources effectively.

## Installation Instructions

Follow the steps below to set up and run the project locally:

### 1. Clone the Repository
Clone the repository to your local machine using the following command:

git clone [https://github.com/dneha1210/ConUhackWinner25.git](https://github.com/dneha1210/ConUhackWinner25.git)

### 2. Set Up a Virtual Environment

python -m venv .venv

For Windows:

.venv\Scripts\activate


For Mac/Linux:

source .venv/bin/activate

### 3. Install Required Libraries

pip install pandas numpy streamlit matplotlib seaborn plotly datetime scikit-learn

### 4. CSV File

Ensure that the CSV file is located in the Scripts folder in your project directory. The code will use this file for processing. Code is located at .venv/Scripts/DRWConUHack.py .  

### 5. Run the Project

To run the main script using Streamlit, use the following command:

streamlit run Scripts/DRWConUHack.py

## Contributors

- Kunal Das
- Layla Beylouneh
- Marie Sophie Roy
- Neha Sanjay Deshmukh









