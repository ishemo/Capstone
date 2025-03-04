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
        template="You are a NCAA basketball analyst and you will make your March Madness bracket as accurate as possible for this year for a school project by predicting each game. Return only the name of the winning team and your score prediction in this format: winning team name, winning team score-losing team score. Do not deviae from that format at all. The two teams playing are {team1} {team2}"
    )
    return prompt_template 