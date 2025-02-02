import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Read CSV file
df = pd.read_csv("Incidents_-_réseau_du_métro.csv")

# Set up the Streamlit app title and description
st.title("😇 STM Metro Incident Dashboard")
st.write("This app shows historical incidents in Montreal's metro system.")

# Data Cleaning and Preparation
df["Heure de l'incident"] = pd.to_datetime(df["Heure de l'incident"], format="%H:%M", errors='coerce').dt.hour
df = df.dropna(subset=["Heure de l'incident"])  # Drop rows with invalid time entries

# Count Incidents per Metro Line
incident_counts = df["Ligne"].value_counts()

# Show as Pie Chart
st.subheader("📊 Most Affected Metro Lines")
# Define colors matching the R script
color_map = {
    "Ligne orange": "darkorange",
    "Ligne bleue": "blue",
    "Ligne jaune": "yellow",
    "Ligne verte": "green"
}

# Filter only the four metro lines of interest
filtered_incidents = incident_counts[incident_counts.index.isin(color_map.keys())]

# Create Pie Chart using Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    filtered_incidents.values,  # Use .values instead of column names
    labels=filtered_incidents.index,  # Labels should be the index
    autopct='%1.1f%%',
    colors=[color_map[line] for line in filtered_incidents.index],
    startangle=90,
    wedgeprops={"edgecolor": "black"}
)
ax.set_title("Percentage of Metro Incidents by Line")

# Display Pie Chart in Streamlit
st.pyplot(fig)

# Count Incidents per Hour with Metro Line
incident_by_hour_line = df.groupby(["Heure de l'incident", "Ligne"]).size().unstack(fill_value=0)

# Filter only the 4 metro lines
incident_by_hour_line = incident_by_hour_line[["Ligne orange", "Ligne bleue", "Ligne jaune", "Ligne verte"]]

# Show Data in Table for Peak Hours
#st.subheader("⏰ Peak Hours for Metro Incidents")
#if incident_by_hour_line.empty:
 #   st.warning("\ud83d\udea8 Warning: No valid timestamps found in 'Heure de l'incident'. Check CSV format!")
#else:
  #  st.write(incident_by_hour_line)

# Bar Chart for Incident Distribution by Hour with Metro Line
st.subheader("📈 Incident Distribution by Hour")
fig, ax = plt.subplots()
incident_by_hour_line.plot(kind='line', ax=ax, color=[color_map.get(line, "gray") for line in incident_by_hour_line.columns])
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Number of Incidents")
ax.set_title("Incidents by Hour and Metro Line")
ax.legend(title="Metro Line")
st.pyplot(fig)

# Dropdown to Select Metro Line (filtered to specific lines)
allowed_lines = ["Ligne verte", "Ligne jaune", "Ligne orange", "Ligne bleue"]
available_lines = [line for line in allowed_lines if line in df["Ligne"].unique()]
selected_line = st.selectbox("Select a Metro Line:", available_lines)

# Filter Data for Selected Line
filtered_df = df[df["Ligne"] == selected_line]

# Show Filtered Table
st.dataframe(filtered_df.head(10))

# Incidents by Month/Year
df["Année civile"] = pd.to_datetime(df["Année civile"], format="%Y")
df["Month_Year"] = df["Année civile"].dt.to_period('M').astype(str)
incidents_by_month_year = df.groupby("Month_Year").size()

st.subheader("📅 Incidents by Month and Year")
fig, ax = plt.subplots()
incidents_by_month_year.plot(kind='line', ax=ax, marker='o')
ax.set_xlabel("Month and Year")
ax.set_ylabel("Number of Incidents")
ax.set_title("Incidents by Month and Year")
plt.xticks(rotation=45)
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