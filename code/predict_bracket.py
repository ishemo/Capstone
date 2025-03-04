# predict_bracket.py

import csv
import display_bracket
from config import initialize_llm, create_prompt_template
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAI


def run_game(team1, seed1, team2, seed2, round_name, llm, context):
    """
    Formats the team names with their seed information,
    creates a prompt using main.py's prompt_template,
    invokes the LLM to predict the winner, and returns a formatted result.
    """
    formatted_team1 = f"{team1} (Seed {seed1})"
    formatted_team2 = f"{team2} (Seed {seed2})"
    
    # Create the prompt with seed info
    prompt = create_prompt_template().format(team1=formatted_team1, team2=formatted_team2, context=context)
    
    # Invoke the model to get the prediction
    response = llm.invoke(prompt).content
    
    # Print the matchup and prediction for visibility
    print(f"[{round_name}] {formatted_team1} vs {formatted_team2} -> {response.strip()}")
    
    # Prepare a result string for later reference
    result_text = f"{formatted_team1} vs {formatted_team2} -> {response.strip()}"
    return response.strip()

def simulate_bracket(file_path, llm):
    """
    Reads the bracket file, processes each game, groups results by round,
    and writes out a separate text file for each round.
    """
    # Create the bracket_predictions directory if it doesn't exist
    os.makedirs("bracket_predictions", exist_ok=True)
    
    # Set up vector db for contect
    file_path_data = "data/final_data/current_team_data.txt"
    loader = TextLoader(file_path_data)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("team_info_db")

    rounds_results = {}
    
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            round_name = row["Round"].strip()
            team1 = row["Team1"].strip()
            seed1 = row["Seed1"].strip()
            team2 = row["Team2"].strip()
            seed2 = row["Seed2"].strip()

            # get context
            team1Context = vector_db.similarity_search(team1, k=1)
            team2Context = vector_db.similarity_search(team2, k=1)
            context = f"Team 1 Info:\n{team1Context}\n\nTeam 2 Info:\n{team2Context}"
            
            # Get the result for the game
            result_text = run_game(team1, seed1, team2, seed2, round_name, llm, context)
            
            # Collect results for the round
            if round_name not in rounds_results:
                rounds_results[round_name] = []
            rounds_results[round_name].append(result_text)
    
    # Write a separate file for each round with its results
    for round_name, results in rounds_results.items():
        # Use a simple naming scheme by replacing spaces with underscores
        file_name = f"bracket_predictions/{round_name.replace(' ', '_')}.txt"
        with open(file_name, "w") as f:
            f.write("\n".join(results))
        print(f"Wrote results for {round_name} to {file_name}")

def predict_bracket():
    llm = initialize_llm()
    simulate_bracket("code/testbracket.txt", llm)
    display_bracket.display_bracket()