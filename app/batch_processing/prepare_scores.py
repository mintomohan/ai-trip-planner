from dotenv import load_dotenv
load_dotenv()
import re
import csv
import json
import logging
from langchain_anthropic import ChatAnthropic

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

APP_VERSION = 'v2'



def extract_scores_from_llm(destination, month, prompt_text, csv_file, mode='a'):
    llm = ChatAnthropic(model='claude-3-5-sonnet-20240620', temperature=0.1)
    logging.debug(f"Prompt: {prompt_text}")
    response = llm.invoke(prompt_text).content
    logging.debug(f"Response: {response}")
    
    # Use a regular expression to extract the markdown table
    table_pattern = re.compile(r'\| Category\s+\| Score\s+\| Options\s+\|([\s\S]*?)\| Wildlife / Safari\s+\| \d\s+\| [^\|]+\|')
    table_match = table_pattern.search(response)
    
    if table_match:
        table_text = table_match.group(0).strip()
        table_lines = table_text.split('\n')[2:] 

        table_data = []
        for line in table_lines:
            parts = line.split('|')[1:-1]  # Split by '|' and ignore the first and last empty parts
            parts = [part.strip() for part in parts]
            logging.debug({
                "Destination": destination,
                "Month": month,
                "Category": parts[0],
                "Score": parts[1],
                "Options": parts[2]
            })
            table_data.append({
                "Destination": destination,
                "Month": month,
                "Category": parts[0],
                "Score": parts[1],
                "Options": parts[2]
            })

        with open(csv_file, mode=mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Destination", "Month", "Category", "Score", "Options"])
            if mode == 'w':
                writer.writeheader()
            for row in table_data:
                writer.writerow(row)

        logging.info(f"Table data for {destination} in {month} has been written to {csv_file}")
    else:
        logging.warn(f"Table not found in the provided text for {destination} in {month}.")



def main():
    destinations_file_path = f'app/config/{APP_VERSION}/destinations.txt'    
    destinations = []
    with open(destinations_file_path, 'r') as file:
        destinations = [line.strip() for line in file.readlines()]

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    csv_output_file = f"app/config/{APP_VERSION}/destination_rankings.csv"

    with open(f'app/config/{APP_VERSION}/preferences.json', 'r') as f:
        preferences = json.load(f)
    category_names = "\n".join(pref['name'] for pref in preferences)

    # Write the header to the CSV file initially
    with open(csv_output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Destination", "Month", "Category", "Score", "Options"])
        writer.writeheader()

    for destination in destinations:
        for month in months:
            prompt = f"""
            As an expert travel agent, I want to rank the destination "{destination}" in month of {month}, on a scale of 0 to 10 for each of the below parameters:

            {category_names}

            Please summarize the result in a markdown table in below format:
            Category, Score, Options
            """
            extract_scores_from_llm(destination, month, prompt, csv_output_file, mode='a')



if __name__ == '__main__':
    main()
