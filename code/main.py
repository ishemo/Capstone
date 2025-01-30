from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI model
llm = OpenAI(temperature=0.7, api_key=OPENAI_API_KEY)

# Create a prompt template
prompt_template = PromptTemplate(
    input_variables=["team1", "team2"],
    template="You are a sports analyst and making a prediction for the 2025 March Madness mens basketball tournament. If {team1} and {team2} were to play eachother in the tournament who would win? Only respond with the name of the team who would win and your score prediction."
)

# Generate the prompt
team1 = input("Enter the first team: ")
team2 = input("Enter the second team: ")
prompt = prompt_template.format(team1=team1, team2=team2)

# Get response from the model
response = llm.invoke(prompt)
print(response)
