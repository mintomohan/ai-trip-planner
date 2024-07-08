from dotenv import load_dotenv
load_dotenv()
import os
import json
import numpy as np
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Sample data: Destination scores matrix
B = np.array([
    [7, 2, 3, 8, 6, 9, 5, 10, 8, 7, 7, 6, 6],  # Beijing
    [6, 3, 2, 9, 7, 8, 5, 7, 6, 6, 8, 7, 5],   # Guangzhou
    [5, 7, 3, 6, 6, 7, 6, 5, 5, 6, 6, 6, 6],   # Dalian
    [6, 3, 2, 8, 8, 8, 7, 9, 8, 7, 8, 8, 6],   # Hangzhou
    [8, 5, 1, 9, 7, 9, 6, 7, 8, 8, 7, 7, 7],   # Hong Kong
    [7, 3, 6, 8, 8, 9, 6, 8, 8, 8, 8, 7, 7],   # Seoul
    [7, 2, 2, 9, 7, 9, 5, 9, 8, 7, 7, 7, 6],   # Shanghai
    [6, 4, 2, 8, 7, 8, 6, 6, 7, 7, 7, 7, 6],   # Shenzhen
    [6, 6, 3, 7, 7, 7, 7, 6, 6, 6, 6, 7, 6],   # Qingdao
    [7, 4, 4, 8, 7, 8, 6, 8, 7, 7, 7, 7, 7]    # Taipei (Taiwan)
])


destinations = [
    "Beijing", "Guangzhou", "Dalian", "Hangzhou", "Hong Kong", 
    "Seoul", "Shanghai", "Shenzhen", "Qingdao", "Taipei (Taiwan)"
]

def load_preferences():
    with open('app/config/preferences.json', 'r') as file:
        preferences = json.load(file)
    return preferences


# Function to generate the prompt content for each recommended destination
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


# Function to invoke an LLM using LangChain
def invoke_llm(prompt_text):
    llm = ChatOpenAI(model='gpt-4o', temperature=0.1)
    #prompt = ChatPromptTemplate.from_template(prompt_text)
    #print(prompt)
    response = llm.invoke(prompt_text).content
    return response


def recommend_destinations(selected_preferences, month):
    print(selected_preferences)
    preferences = load_preferences()
    # Calculate max_score based on number of selected preferences
    max_score = len(selected_preferences) * 10
    # Create user preference vector A
    A = np.zeros((len(preferences), 1))
    for preference in selected_preferences:
        A[[p["name"] for p in preferences].index(preference)] = 1
    print(A)

    # Calculate the score for each destination
    scores = np.dot(B, A).flatten()
    print(scores)

    # Get the indices of the top 3 destinations
    top_3_indices = np.argsort(scores)[-3:][::-1]
    print(f"top_3_indices = {top_3_indices}")
    
    # Output the top 3 destinations
    top_3_destinations = []
    for i in top_3_indices:
        destination = destinations[i]
        print(f"Max Score = {max_score}")
        # Create user preference vector A
        A = np.zeros(len(selected_preferences))
        for j, pref in enumerate(selected_preferences):
            if pref in preferences:
                A[j] = scores[preferences.index(pref)]

        # Calculate the total score for the destination
        total_score = scores[i]
        print(f"i = {i}")
        print(f"scores = {scores}")
        print(f"A = {A}")
        print(f"Total score = {total_score}")
        # Calculate percentage match for the destination
        percentage_match = int((total_score / max_score) * 100)

        prompt = generate_prompt(destination, month, selected_preferences)
        summary = invoke_llm(prompt)

        top_3_destinations.append({"destination": destination,
                                    "percentage_match": percentage_match,
                                    "summary": summary})

    return top_3_destinations
