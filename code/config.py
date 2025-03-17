from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

def initialize_llm():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Initialize the OpenAI model
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    return llm

def create_prompt_template():
    """
    Creates a prompt template for team matchup predictions.
    """
    
    template = """You are a college basketball expert analyzing March Madness matchups.

    Below are details for two teams in an upcoming game:

    Team 1: {team1}
    Team 2: {team2}

    Additional Context for the two teams playing:
    {context}

    Based on the information provided, predict which team will win this matchup.

    IMPORTANT: 
    1. Respond ONLY with the EXACT name of the winning team as provided above (either "{team1}" or "{team2}").
    2. Do not include scores, explanations, or variations of the team name.
    3. Simply output only the winning team's name exactly as shown above.

    Your prediction:"""

    return template 