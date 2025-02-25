from dotenv import load_dotenv
import os
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate

def initialize_llm():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Initialize the OpenAI model
    llm = OpenAI(temperature=0.7, api_key=OPENAI_API_KEY)
    return llm

def create_prompt_template():
    # Create a prompt template
    prompt_template = PromptTemplate(
        input_variables=["team1", "team2"],
        template="You are a sports analyst and making a prediction for the 2025 March Madness mens basketball tournament. If {team1} and {team2} were to play eachother in the tournament who would win? Only respond with the name of the team who would win and your score prediction."
    )
    return prompt_template 