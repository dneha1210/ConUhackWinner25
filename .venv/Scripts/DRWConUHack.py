import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from scipy.stats import norm

# Read CSV file
df = pd.read_csv("Incidents_-_réseau_du_métro.csv")

# Set up the Streamlit app title and description
st.title("😇 STM Metro Incident Dashboard")
st.write("This app shows historical incidents in Montreal's metro system and predicts future incidents.")

# Data Cleaning and Preparation
df["Heure de l'incident"] = pd.to_datetime(df["Heure de l'incident"], format="%H:%M", errors='coerce').dt.hour
df = df.dropna(subset=["Heure de l'incident"])  # Drop rows with invalid time entries

df["Jour calendaire"] = pd.to_datetime(df["Jour calendaire"], errors='coerce')
df = df.dropna(subset=["Jour calendaire"])  # Drop rows with invalid dates

# Count Incidents per Metro Line
incident_counts = df["Ligne"].value_counts()

# Pie Chart for Metro Line Incidents
st.subheader("📊 Most Affected Metro Lines")
color_map = {"Ligne orange": "darkorange", "Ligne bleue": "blue", "Ligne jaune": "yellow", "Ligne verte": "green"}
filtered_incidents = incident_counts[incident_counts.index.isin(color_map.keys())]
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(filtered_incidents.values, labels=filtered_incidents.index, autopct='%1.1f%%', colors=[color_map[line] for line in filtered_incidents.index], startangle=90, wedgeprops={"edgecolor": "black"})
ax.set_title("Percentage of Metro Incidents by Line")
st.pyplot(fig)

# Incidents by Hour and Metro Line
incident_by_hour_line = df.groupby(["Heure de l'incident", "Ligne"]).size().unstack(fill_value=0)
st.subheader("📈 Incident Distribution by Hour")
fig, ax = plt.subplots()
incident_by_hour_line.plot(kind='bar', stacked=True, ax=ax, color=[color_map.get(line, "gray") for line in incident_by_hour_line.columns], legend=False)
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Number of Incidents")
ax.set_title("Incidents by Hour")
st.pyplot(fig)


# Incidents by Station
station_incidents = df["Code de lieu"].value_counts().head(10)
st.subheader("🚉 Top 10 Stations with Most Incidents")
fig, ax = plt.subplots()
station_incidents.plot(kind='bar', ax=ax, color='lightgreen')
ax.set_xlabel("Station Code")
ax.set_ylabel("Number of Incidents")
ax.set_title("Top 10 Stations with Most Incidents")
st.pyplot(fig)

# Incidents by Type
incident_types = df["Type d'incident"].value_counts()
st.subheader("🔧 Types of Incidents")
fig, ax = plt.subplots()
incident_types.plot(kind='bar', ax=ax, color='lightcoral')
ax.set_xlabel("Incident Type")
ax.set_ylabel("Number of Incidents")
ax.set_title("Types of Incidents")
st.pyplot(fig)

# Incident Duration Analysis
df["Heure de reprise"] = pd.to_datetime(df["Heure de reprise"], format="%H:%M", errors='coerce').dt.hour
df["Incident Duration"] = (df["Heure de reprise"] - df["Heure de l'incident"]) * 60  # Convert to minutes
st.subheader("⏳ Incident Duration Analysis")
fig, ax = plt.subplots()
df["Incident Duration"].plot(kind='hist', ax=ax, bins=20, color='purple')
ax.set_xlabel("Incident Duration (minutes)")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of Incident Durations")
st.pyplot(fig)

# Heatmap of Incidents by Hour and Day
df["Jour de la semaine"] = pd.to_datetime(df["Jour calendaire"]).dt.day_name()
heatmap_data = df.pivot_table(index="Jour de la semaine", columns="Heure de l'incident", values="Numero d'incident", aggfunc='count')
st.subheader("🔥 Heatmap of Incidents by Hour and Day")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap="YlOrRd", ax=ax)
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Day of the Week")
ax.set_title("Incidents by Hour and Day")
st.pyplot(fig)

# Machine Learning Section
st.subheader("🔮 Incident Type Prediction Using Machine Learning")
label_encoders = {}
scaler = StandardScaler()
mlp = MLPClassifier(hidden_layer_sizes=(50, 30), max_iter=500, random_state=42)

if "model_trained" not in st.session_state:
    st.session_state.model_trained = False
    st.session_state.label_encoders = {}
    st.session_state.scaler = StandardScaler()
    st.session_state.mlp = MLPClassifier(hidden_layer_sizes=(50, 30), max_iter=500, random_state=42)

if st.button("Train and Evaluate Model"):
    for col in ["Ligne", "Jour de la semaine", "Type d'incident"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        st.session_state.label_encoders[col] = le

    X = df[["Ligne", "Heure de l'incident", "Jour de la semaine"]]
    y = df["Type d'incident"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    st.session_state.scaler.fit(X_train)
    X_train = st.session_state.scaler.transform(X_train)
    X_test = st.session_state.scaler.transform(X_test)

    st.session_state.mlp.fit(X_train, y_train)
    st.session_state.model_trained = True

    y_pred = st.session_state.mlp.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"Model Accuracy: {accuracy:.2f}")
    conf_interval = norm.interval(0.95, loc=accuracy, scale=np.sqrt((accuracy * (1 - accuracy)) / len(y_test)))
    st.write(f"95% Confidence Interval for Accuracy: ({conf_interval[0]:.2f}, {conf_interval[1]:.2f})")

# Predict Future Incidents
st.subheader("🔮 Predict Future Incidents")
future_date = st.date_input("Select a Future Date", value=datetime.today())
selected_line = st.selectbox("Select a Metro Line", ["Ligne verte", "Ligne jaune", "Ligne bleue", "Ligne orange"])
time_of_day = st.slider("Select Hour of the Day", min_value=0, max_value=23, value=12)

if st.button("Predict Incident Likelihood"):
    if st.session_state.model_trained:
        line_encoded = st.session_state.label_encoders["Ligne"].transform([selected_line])[0]
        day_of_week = future_date.weekday()
        # Ensure feature names match those used in training
        input_data = pd.DataFrame([[line_encoded, time_of_day, day_of_week]], columns=["Ligne", "Heure de l'incident", "Jour de la semaine"])

        # Now transform without warning
        input_data = st.session_state.scaler.transform(input_data)
        predicted_probabilities = st.session_state.mlp.predict_proba(input_data)
        incident_likelihood = np.max(predicted_probabilities) * 100
        
        color = "green" if incident_likelihood < 50 else "red"
        st.markdown(f"<p style='color:{color}; font-size:20px;'>Likelihood of an incident occurring: {incident_likelihood:.2f}%</p>", unsafe_allow_html=True)
    else:
        st.write("Please train the model first by clicking the 'Train and Evaluate Model' button.")