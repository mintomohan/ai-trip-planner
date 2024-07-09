import streamlit as st
import numpy as np
import os
from recommendations import recommend_destinations, load_preferences

preferences = load_preferences()

app_name = "Trip Planner"
st.set_page_config(page_title=app_name, page_icon="✈️", layout="wide")
st.title(app_name)
st.write("Select your preferences from the list below:")

selected_preferences = []

hide_full_screen = '''
<style>
[data-testid=StyledFullScreenButton] {visibility: hidden;}
</style>
'''

st.markdown(hide_full_screen, unsafe_allow_html=True) 

cols = st.columns(7)  # Display 7 cards per row
for i, preference in enumerate(preferences):
    with cols[i % 7]:
        # Create a container for each card
        with st.container(border=True):
            # Checkbox
            checkbox_selected = st.checkbox(preference["name"], key=f"checkbox_{i}")
            # Image
            image_path = preference["image"]
            if os.path.exists(image_path):
                st.image(image_path, use_column_width=True, output_format='PNG')
            # Selected Checkbox
            if checkbox_selected:
                selected_preferences.append(preference["name"])


# Radio button for month
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
selected_month = st.radio("Select your travel month:", months, horizontal=True)

# Find button
if st.button("Find Destination"):
    if not selected_preferences:
        st.write("Please select at least one preference.")
    elif not selected_month:
        st.write("Please select a month of travel.")
    else:
        top_3_destinations = recommend_destinations(selected_preferences, selected_month)
        
        st.write(f"Based on the preferences, visiting the following destinations is recommended:")
        for item in top_3_destinations:
            with st.container(border=True):
                st.subheader(f"**{item['destination']}**")
                st.write(f"Match : {item['percentage_match']}%")
                st.write(item['summary'])


with st.container(border=True):
    st.markdown("""
        © 2024 Minto Mohan
        
        Licensed under GNU GPLv3
        """)
    st.markdown('**Image Attributions:**')
    st.markdown("""
        <style>
        .small-font {
            font-size: 12px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <p class="small-font">
        <a href="https://www.flaticon.com/free-icons/ship" title="ship icons">Ship icons created by Freepik - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/skiing" title="skiing icons">Skiing icons created by monkik - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/nutrition" title="nutrition icons">Nutrition icons created by Roundicons Premium - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/yoga" title="yoga icons">Yoga icons created by dDara - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/party" title="party icons">Party icons created by tulpahn - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/environment" title="environment icons">Environment icons created by Freepik - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/historical" title="historical icons">Historical icons created by Freepik - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/mona-lisa" title="mona-lisa icons">Mona-lisa icons created by Good Ware - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/photographer" title="photographer icons">Photographer icons created by dDara - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/honeymoon" title="Honeymoon icons">Honeymoon icons created by SBTS2018 - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/sea" title="sea icons">Sea icons created by Freepik - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/thailand" title="thailand icons">Thailand icons created by Wichai.wi - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/luxury" title="luxury icons">Luxury icons created by Freepik - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/night-life" title="night life icons">Night life icons created by Freepik - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/lion" title="lion icons">Lion icons created by Icongeek26 - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/culinary" title="culinary icons">Culinary icons created by Freepik - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/historical" title="historical icons">Historical icons created by smalllikeart - Flaticon</a><br>
        <a href="https://www.flaticon.com/free-icons/event" title="event icons">Event icons created by Freepik - Flaticon</a>
        </p>
        """, unsafe_allow_html=True)