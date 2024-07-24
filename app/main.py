import streamlit as st
import numpy as np
import os
from recommendations import recommend_destinations, load_preferences
import json

translations = []

def load_translations(language_code):
    with open(f'app/config/translations/{language_code}.json', 'r', encoding='utf-8') as file:
        return json.load(file)



def month_radio_labels(option):
    months = [
                translations['month_jan'],
                translations['month_feb'],
                translations['month_mar'],
                translations['month_apr'],
                translations['month_may'],
                translations['month_jun'],
                translations['month_jul'],
                translations['month_aug'],
                translations['month_sep'],
                translations['month_oct'],
                translations['month_nov'],
                translations['month_dec']
            ]
    return months[option-1]



def get_month_names_eng(id:int):
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return months[id-1]



preferences = load_preferences()

app_title = 'Trip Planner'
if 'app_title' not in st.session_state:    
    st.set_page_config(page_title=app_title, page_icon="✈️", layout="wide", initial_sidebar_state="collapsed")
else:
    st.set_page_config(page_title=st.session_state.app_title, page_icon="✈️", layout="wide", initial_sidebar_state="collapsed")

language = st.sidebar.selectbox('Select Language', ['English', 'Japanese'])
language_code = 'en' if language == 'English' else 'ja'
translations = load_translations(language_code)

st.session_state.app_title = translations['app_title']

st.title(translations['app_title'])
st.write(translations['select_preferences_message'])

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
            checkbox_selected = st.checkbox(translations[preference["key"]], key=f"checkbox_{i}")
            # Image
            image_path = preference["image"]
            if os.path.exists(image_path):
                st.image(image_path, use_column_width=True, output_format='PNG')
            # Selected Checkbox
            if checkbox_selected:
                selected_preferences.append(preference["key"])


# Radio button for month
months = range(1,13)
selected_month = st.radio(label='Month', label_visibility="hidden", options=months, format_func=month_radio_labels, horizontal=True)

# Find button
if st.button(translations["button_label_find_destination"]):
    if not selected_preferences:
        st.write(translations["msg_preference_not_selected"])
    elif not selected_month:
        st.write(translations["msg_month_not_selected"])
    else:
        print(selected_preferences)
        print(selected_month)
        eng = load_translations('en')
        selected_preferences_en = [eng[p] for p in selected_preferences]
        selected_month_en = get_month_names_eng(selected_month)
        print(selected_preferences_en)
        print(selected_month_en)
        top_3_destinations = recommend_destinations(selected_preferences_en, selected_month_en, language_code)
        
        st.write(translations["msg_display_results"])
        for item in top_3_destinations:
            with st.container(border=True):
                st.subheader(f"**{translations[item['destination']]}**")
                st.write(f"{translations['match']} : {item['percentage_match']}%")
                st.write(item['summary'])


with st.expander("License & Attributions"):
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