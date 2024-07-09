from dotenv import load_dotenv
load_dotenv()
import json
import numpy as np
import pandas as pd
from langchain_anthropic import ChatAnthropic
import logging

APP_VERSION = 'v2'
N = 5

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



def load_preferences():
    with open(f'app/config/{APP_VERSION}/preferences.json', 'r') as file:
        preferences = json.load(file)
    return preferences



def load_destination_data(file_path, selected_month):
    month_mapping = {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December"
    }
    
    full_month = month_mapping.get(selected_month, selected_month)
    
    df = pd.read_csv(file_path)
    df_filtered = df[df['Month'] == full_month]
    
    destinations = df_filtered['Destination'].unique()
    categories = df_filtered['Category'].unique()
    
    score_matrix = np.zeros((len(destinations), len(categories)))
    
    for i, destination in enumerate(destinations):
        for j, category in enumerate(categories):
            score = df_filtered[(df_filtered['Destination'] == destination) & (df_filtered['Category'] == category)]['Score']
            if not score.empty:
                score_matrix[i][j] = score.values[0]
    
    return score_matrix, list(destinations), list(categories)



def generate_prompt(destination, month, preferences):
    preferences_str = ", ".join(preferences)
    prompt = (
        f"As an expert travel agent, generate a brief summary about a destination for a specific month, "
        f"matching the user's preferences. The content should include an overview and key attractions in a single paragraph. "
        f"The overall content should be 100-150 words.\n\n"
        f"Generate the content:\n"
        f"Destination: {destination}\n"
        f"Month: {month}\n"
        f"Preferences: {preferences_str}\n"
    )
    return prompt



def invoke_llm(prompt_text):
    llm = ChatAnthropic(model='claude-3-5-sonnet-20240620', temperature=0.1)
    response = llm.invoke(prompt_text).content
    return response



def recommend_destinations(selected_preferences, selected_month):
    logging.debug(selected_preferences)
    logging.debug(selected_month)

    score_matrix, destinations, categories = load_destination_data(f'app/config/{APP_VERSION}/destination_rankings.csv', selected_month)
    logging.debug(score_matrix)
    logging.debug(destinations)
    logging.debug(categories)
    
    results = []
    
    max_score = len(selected_preferences) * 10

    # Create user preference vector A
    user_preference_vector = np.zeros(len(categories))
    for pref in selected_preferences:
        if pref in categories:
            user_preference_vector[categories.index(pref)] = 1

    # Calculate the total scores for all destinations using dot product
    total_scores = np.dot(score_matrix, user_preference_vector)
    logging.debug('-'*20)
    logging.debug(score_matrix)
    logging.debug(user_preference_vector)
    logging.debug(total_scores)
    logging.debug('-'*20)

    # Calculate percentage matches for all destinations
    percentage_matches = (total_scores / max_score) * 100

    # Combine destinations with their percentage matches
    destination_scores = list(zip(destinations, percentage_matches))

    # Sort destinations by percentage match in descending order and select the top N
    top_n_destinations = sorted(destination_scores, key=lambda x: x[1], reverse=True)[:N]
    logging.debug(f"top_n_destinations = {top_n_destinations}")

    results = []

    # Generate prompts and summaries for the top n destinations
    for destination, percentage_match in top_n_destinations:
        prompt = generate_prompt(destination, selected_month, selected_preferences)
        #logging.debug(prompt)
        summary = invoke_llm(prompt)
        
        results.append({
            "destination": destination,
            "percentage_match": int(percentage_match),
            "summary": summary
        })
    logging.debug('='*50)
    return results
