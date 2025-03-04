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
        input_variables=["team1", "team2", "context"],
        template="""You are an expert NCAA basketball analyst creating precise bracket predictions for March Madness.

Task: Predict the winner of a game between {team1} and {team2} based on the stats provided.

Important stats for both teams:
{context}

Instructions:
1. Always evaluate based on the provided stats, even if they seem limited
2. Consider team records, ratings, and matchup dynamics
3. NEVER refuse to make a prediction or apologize for lack of information
4. NEVER explain your reasoning or include any text beyond the required format

REQUIRED OUTPUT FORMAT: 
[Winning Team Name], [Winning Team Score]-[Losing Team Score]

Example good response: Duke, 78-72
Example bad response: I predict Duke will win with a score of 78-72 over UNC

YOUR PREDICTION:"""
    )
    return prompt_template 