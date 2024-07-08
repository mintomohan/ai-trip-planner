import streamlit as st
import numpy as np
import os
from recommendations import recommend_destinations, load_preferences

preferences = load_preferences()



# Streamlit UI
st.set_page_config(layout="wide")
st.title("Nufly")
st.write("Select your preferences from the list below:")

# Create checkboxes for each preference using cards layout
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
            
            if checkbox_selected:
                selected_preferences.append(preference["name"])


# Add a single radio button for selecting the month
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
        
        st.write(f"Based on your preferences, we recommend you to visit:")
        for item in top_3_destinations:
            with st.container(border=True):
                st.subheader(f"**{item['destination']}**")
                st.write(f"Match : {item['percentage_match']}%")
                st.write(item['summary'])



st.markdown('[Adventurer icons created by max.icons - Flaticon](https://www.flaticon.com/free-icons/adventurer)')
# <a href="https://www.flaticon.com/free-icons/ship" title="ship icons">Ship icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/skiing" title="skiing icons">Skiing icons created by monkik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/nutrition" title="nutrition icons">Nutrition icons created by Roundicons Premium - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/yoga" title="yoga icons">Yoga icons created by dDara - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/party" title="party icons">Party icons created by tulpahn - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/environment" title="environment icons">Environment icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/historical" title="historical icons">Historical icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/mona-lisa" title="mona-lisa icons">Mona-lisa icons created by Good Ware - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/photographer" title="photographer icons">Photographer icons created by dDara - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/honeymoon" title="Honeymoon icons">Honeymoon icons created by SBTS2018 - Flaticon</a>
# 
# 