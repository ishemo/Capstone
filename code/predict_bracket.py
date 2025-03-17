# predict_bracket.py

import csv
import display_bracket
from config import initialize_llm, create_prompt_template
import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAI


def run_game(team1, seed1, team2, seed2, round_name, llm, vector_db):
    """
    Formats the team names with their seed information,
    creates a prompt using main.py's prompt_template,
    invokes the LLM to predict the winner, and returns the winning team and seed.
    """
    formatted_team1 = f"{team1} (Seed {seed1})"
    formatted_team2 = f"{team2} (Seed {seed2})"
    
    # Get context for the teams if they're not placeholder winners
    context = ""
    if not team1.startswith("Winner of"):
        try:
            team1_context = vector_db.similarity_search(team1, k=1)
            context += f"Team 1 Info:\n{team1_context[0].page_content}\n\n"
        except:
            print(f"Couldn't find context for {team1}")
    if not team2.startswith("Winner of"):
        try:
            team2_context = vector_db.similarity_search(team2, k=1)
            context += f"Team 2 Info:\n{team2_context[0].page_content}"
        except:
            print(f"Couldn't find context for {team2}")

    # Create the prompt with seed info
    prompt = create_prompt_template().format(team1=formatted_team1, team2=formatted_team2, context=context)
    
    # Invoke the model to get the prediction
    response = llm.invoke(prompt)
    
    # Handle different response types - some LLMs return strings, others return objects with content
    if hasattr(response, 'content'):
        response_text = response.content.strip()
    else:
        response_text = str(response).strip()
    
    # Print the matchup and prediction for visibility
    print(f"[{round_name}] {formatted_team1} vs {formatted_team2} -> {response_text}")
    
    # Determine the winner based on the response
    if team1.lower() in response_text.lower():
        winner, winner_seed = team1, seed1
    elif team2.lower() in response_text.lower():
        winner, winner_seed = team2, seed2
    else:
        # If the model doesn't clearly indicate a winner, default to the higher seed (lower number)
        print(f"Warning: Couldn't determine winner from response. Defaulting to higher seed.")
        if int(seed1) < int(seed2):
            winner, winner_seed = team1, seed1
        else:
            winner, winner_seed = team2, seed2
    
    # Prepare a result string for later reference
    result_text = f"{formatted_team1} vs {formatted_team2} -> {winner} (Seed {winner_seed})"
    return result_text, winner, winner_seed

def simulate_bracket(file_path, llm):
    """
    Reads the bracket file, processes each game in order of rounds,
    tracks winners, and writes out results.
    """
    # Create the bracket_predictions directory if it doesn't exist
    os.makedirs("bracket_predictions", exist_ok=True)
    
    # Set up vector db for context
    try:
        file_path_data = "data/final_data/data.txt"
        loader = TextLoader(file_path_data)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
        chunks = text_splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings()
        vector_db = FAISS.from_documents(chunks, embeddings)
    except Exception as e:
        print(f"Error loading team data: {e}. Will continue without team context.")
        # Create a dummy vector DB that returns empty results
        class DummyVectorDB:
            def similarity_search(self, query, k=1):
                return [type('obj', (object,), {'page_content': f"No data available for {query}"})]
        vector_db = DummyVectorDB()

    # Define the round order to ensure we process in sequence
    round_order = ["First Four", "First Round", "Second Round", "Sweet Sixteen", "Elite Eight", "Final Four", "Championship"]
    
    # Read all games into memory and organize by round
    games_by_round = {round_name: [] for round_name in round_order}
    
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            round_name = row["Round"].strip()
            if round_name in games_by_round:
                games_by_round[round_name].append(row)
    
    # Dictionary to store results in a format that exactly matches the input file references
    winner_lookup = {}
    rounds_results = {round_name: [] for round_name in round_order}
    
    # Process each round in order
    for round_name in round_order:
        print(f"\nProcessing {round_name} games...")
        round_games = games_by_round[round_name]
        
        for game_idx, game in enumerate(round_games, 1):
            team1 = game["Team1"].strip()
            seed1 = game["Seed1"].strip()
            team2 = game["Team2"].strip()
            seed2 = game["Seed2"].strip()
            
            # Create a unique game key in the exact format referenced in the CSV
            game_key = f"{round_name} Game {game_idx}"
            
            # Resolve any "Winner of" placeholder for team1
            if "Winner of" in team1:
                prev_game_key = team1
                if prev_game_key in winner_lookup:
                    team1, seed1 = winner_lookup[prev_game_key]
                else:
                    print(f"Warning: {team1} not found in winner_lookup")
                    continue  # Skip this game
            
            # Resolve any "Winner of" placeholder for team2
            if "Winner of" in team2:
                prev_game_key = team2
                if prev_game_key in winner_lookup:
                    team2, seed2 = winner_lookup[prev_game_key]
                else:
                    print(f"Warning: {team2} not found in winner_lookup")
                    continue  # Skip this game
            
            # Run the game
            result_text, winner, winner_seed = run_game(team1, seed1, team2, seed2, round_name, llm, vector_db)
            
            # Store the result
            winner_lookup[f"Winner of {game_key}"] = (winner, winner_seed)
            rounds_results[round_name].append((game_idx, result_text))
    
    # Write a separate file for each round with its results
    for round_name, results in rounds_results.items():
        if results:  # Only write if there are results
            sorted_results = sorted(results, key=lambda x: x[0])
            results_text = [result for _, result in sorted_results]
            
            file_name = f"bracket_predictions/{round_name.replace(' ', '_')}.txt"
            with open(file_name, "w") as f:
                f.write("\n".join(results_text))
            print(f"Wrote results for {round_name} to {file_name}")
    
    # Create a final bracket result file
    with open("bracket_predictions/final_bracket.txt", "w") as f:
        f.write("============================================================\n")
        f.write("                 FINAL BRACKET PREDICTIONS                  \n")
        f.write("============================================================\n\n")
        
        for round_name in round_order:
            if rounds_results[round_name]:
                f.write(f"{round_name.center(60)}\n")
                f.write("-" * 60 + "\n")
                
                sorted_results = sorted(rounds_results[round_name], key=lambda x: x[0])
                for game_idx, result in sorted_results:
                    f.write(f"Game {game_idx}: {result}\n")
                
                f.write("-" * 60 + "\n\n")
        
        # Write the overall champion
        if "Championship" in rounds_results and rounds_results["Championship"]:
            f.write("============================================================\n")
            f.write("                          CHAMPION                          \n")
            f.write("============================================================\n")
            championship_result = rounds_results["Championship"][0][1]
            champion = championship_result.split("->")[1].strip()
            f.write(f"                        {champion}                         \n")
            f.write("============================================================\n")

def predict_bracket():
    llm = initialize_llm()
    simulate_bracket("code/testbracket.txt", llm)
    display_bracket.display_bracket()