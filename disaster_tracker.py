import requests
import heapq
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


#Earthquake class to hold earthquake data
class Earthquake:
    def __init__(self, magnitude, place, timestamp):
        self.magnitude = magnitude
        self.place = place
        self.timestamp = timestamp

    def __str__(self):
        return f"M {self.magnitude} - {self.place} at {self.timestamp}"    
    # Heap comparison based on magnitude
    def __lt__(self, other):
        return self.magnitude < other.magnitude


#Earthquake API
URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
#parameters for the API request
params = {
    "format": "geojson",    #return data in GeoJSON format
    "starttime": "2025-09-01",
    "endtime": "2025-09-15",
    "minmagnitude": 5.0,    #minimum magnitude of earthquakes to retrieve
}

#Fetch earthquake data from the API
response = requests.get(URL, params=params)

#Check if the request was successful
if response.status_code == 200:
    #Parse the JSON response
    data = response.json()
    earthquakes = []  #List to hold earthquake objects


#Iterate through each earthquake event and print details
    for eq in data['features']:
        mag = eq['properties']['mag']
        place = eq['properties']['place']
        time = eq['properties']['time']
        earthquakes.append(Earthquake(mag, place, time))

    if len(earthquakes) == 0:
        st.warning("No earthquakes found in the specified date range.")
else:
    st.error("Failed to fetch earthquake data")

#Convert to DataFrame for easier handling
data = [{"magnitude": q.magnitude, "place": q.place, "timestamp": q.timestamp} for q in earthquakes]
df = pd.DataFrame(data)

#Streamlit app
st.title("Global Disaster Tracker")
st.subheader("Earthquake Data (Sept 1 - Sept 15, 2025)")

#Display raw data
st.dataframe(df)
#Show top 5 strongest earthquakes
st.subheader("Top 5 Strongest Earthquakes")
max_heap = [(-q.magnitude, q) for q in earthquakes]
heapq.heapify(max_heap)
top_5 = [heapq.heappop(max_heap)[1] for _ in range(min(5, len(max_heap)))]

for i, q in enumerate(top_5, start=1):
    st.write(f"{i}. {q}")

    
#Visualization
st.subheader("Earthquake Magnitude Distribution")
labels = [q.place.split(",")[0] for q in earthquakes]                    #short labels

plt.figure(figsize=(16, 6))
plt.bar(labels, [q.magnitude for q in earthquakes], color='orange')
plt.xticks(rotation=45, ha='right')                                      #rotate x labels for better readability
plt.xlabel("Location")
plt.ylabel("Magnitude")
plt.tight_layout()
st.pyplot(plt)
