from dotenv import load_dotenv
load_dotenv()
import re
import csv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def extract_table_and_save_to_csv(destination, month, prompt_text, csv_file, mode='a'):
    # Initialize the LLM with your OpenAI API key
    llm = ChatOpenAI(model='gpt-4o', temperature=0.1)
    prompt = ChatPromptTemplate.from_template(prompt_text)
    print(prompt)
    response = llm.invoke(prompt_text).content
    print(response)
    
    # Use a regular expression to extract the markdown table
    table_pattern = re.compile(r'\| Category\s+\| Score\s+\| Options\s+\|([\s\S]*?)\| Fitness and Active\s+\| \d\s+\| [^\|]+\|')
    table_match = table_pattern.search(response)
    
    if table_match:
        table_text = table_match.group(0).strip()
        
        # Extract the table lines
        table_lines = table_text.split('\n')[2:]  # Skip the header and separator lines

        # Parse the table into a list of dictionaries
        table_data = []
        for line in table_lines:
            parts = line.split('|')[1:-1]  # Split by '|' and ignore the first and last empty parts
            parts = [part.strip() for part in parts]
            print({
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

        # Write the table data to a CSV file
        with open(csv_file, mode=mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Destination", "Month", "Category", "Score", "Options"])
            if mode == 'w':
                writer.writeheader()
            for row in table_data:
                writer.writerow(row)

        print(f"Table data for {destination} in {month} has been written to {csv_file}")
    else:
        print(f"Table not found in the provided text for {destination} in {month}.")




def main():
    destinations = [
        "Beijing", "Guangzhou", "Dalian", "Hangzhou", "Hong Kong", 
        "Seoul", "Shanghai", "Shenzhen", "Qingdao", "Taipei (Taiwan)"
    ]
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    csv_file = "app/config/destination_rankings.csv"

    # Write the header to the CSV file initially
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Destination", "Month", "Category", "Score", "Options"])
        writer.writeheader()

    for destination in destinations:
        for month in months:
            prompt = f"""
            As an expert travel agent, I want to rank the destination "{destination}" in month of {month}, on a scale of 0 to 10 for each of the below parameters:

            Adventure
            Cruise
            Winter Sports
            Gastronomic
            Wellness and Spa
            Festival and Events
            Ecotourism
            Historical and Heritage
            Art and Design
            Photography
            Family Fun
            Romantic Getaways
            Fitness and Active

            Please summarize the result in a markdown table in below format:
            Category, Score, Options
            """
            extract_table_and_save_to_csv(destination, month, prompt, csv_file, mode='a')


if __name__ == '__main__':
    main()