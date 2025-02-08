import streamlit as st
import requests
from PIL import Image
from datetime import datetime
import pandas as pd

NASA_API_KEY = "DtqHuAGJcS4npQRr5mhZqRmGtxYRuPp85e3MJKsh"

# Fetch asteroid data
def fetch_asteroids(start_date):
    asteroid_url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={start_date}&api_key={NASA_API_KEY}"
    try:
        response = requests.get(asteroid_url)
        response.raise_for_status()
        data = response.json()
        return data.get("near_earth_objects", {}).get(start_date, [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching asteroid data: {e}")
        return []

# Fetch image of the day
def fetch_image_of_the_day():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching image of the day: {e}")
        return {}

# Fetch astronomical events for the current year (for major events)
def fetch_astronomical_events(year):
    # This API provides general solar system bodies, not specific events like eclipses.
    # So for major events like eclipses, we can manually list them or use a custom API if available.
    events = [
        {"title": "Solar Eclipse", "date": f"{year}-04-08", "description": "Total solar eclipse visible across parts of the United States."},
        {"title": "Lunar Eclipse", "date": f"{year}-05-05", "description": "Total lunar eclipse visible in parts of the world."},
        {"title": "Meteor Shower - Perseids", "date": f"{year}-08-12", "description": "Annual Perseid meteor shower peaks."},
        {"title": "Supermoon", "date": f"{year}-08-01", "description": "The moon will appear larger and brighter than usual."},
        {"title": "Equinox", "date": f"{year}-09-23", "description": "Autumnal equinox marks the start of autumn."}
    ]
    return events

# Display image of the day
def display_image_of_the_day():
    data = fetch_image_of_the_day()
    if data:
        title = data.get("title", "No Title")
        image_url = data.get("url", "")
        explanation = data.get("explanation", "No explanation available.")
        st.image(image_url, use_container_width=True)
        st.write(f"**{title}**")
        st.write(explanation)

# Display asteroid data
def display_asteroid_data():
    # Date selector
    selected_date = st.date_input("Select Date for Asteroids", datetime.today())

    # Format selected date to YYYY-MM-DD
    formatted_date = selected_date.strftime("%Y-%m-%d")
    asteroids = fetch_asteroids(formatted_date)
    
    if asteroids:
        st.write(f"Asteroids passing Earth on {formatted_date}:")
        asteroid_data = []
        for asteroid in asteroids:
            name = asteroid.get("name", "N/A")
            close_approach = asteroid.get("close_approach_data", [{}])[0].get("close_approach_date", "N/A")
            miss_distance = asteroid.get("close_approach_data", [{}])[0].get("miss_distance", {}).get("kilometers", "N/A")
            speed = asteroid.get("close_approach_data", [{}])[0].get("relative_velocity", {}).get("kilometers_per_hour", "N/A")
            description = asteroid.get("absolute_magnitude_h", "No description available.")
            asteroid_data.append([name, close_approach, miss_distance, speed, description])
        
        asteroid_df = pd.DataFrame(asteroid_data, columns=["Asteroid Name", "Close Approach Date", "Miss Distance (km)", "Speed (km/h)", "Description"])
        st.table(asteroid_df)
    else:
        st.write(f"No asteroid data found for {formatted_date}.")

# Display astronomical events
def display_astronomical_events(year):
    events = fetch_astronomical_events(year)
    if events:
        st.write(f"Astronomical events for the year {year}:")
        for event in events:
            title = event.get("title", "No Title")
            description = event.get("description", "No description available.")
            date = event.get("date", "N/A")
            st.write(f"**{title}**")
            st.write(f"Date: {date}")
            st.write(f"Description: {description}")
    else:
        st.write(f"No astronomical events found for the year {year}.")

# Main function
def main():
    st.title("Astro Dashboard")
    
    options = ["Image of the Day", "Asteroid Tracker", "Astronomical Events"]
    selection = st.sidebar.radio("Choose an option", options)

    if selection == "Image of the Day":
        display_image_of_the_day()
    elif selection == "Asteroid Tracker":
        display_asteroid_data()
    elif selection == "Astronomical Events":
        current_year = datetime.now().year
        display_astronomical_events(current_year)

if __name__ == "__main__":
    main()
