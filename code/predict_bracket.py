# predict_bracket.py

import csv
import main 
import os  # Add this import at the top

def run_game(team1, seed1, team2, seed2, round_name):
    """
    Formats the team names with their seed information,
    creates a prompt using main.py's prompt_template,
    invokes the LLM to predict the winner, and returns a formatted result.
    """
    formatted_team1 = f"{team1} (Seed {seed1})"
    formatted_team2 = f"{team2} (Seed {seed2})"
    
    # Create the prompt with seed info
    #prompt = main.prompt_template.format(team1=formatted_team1, team2=formatted_team2)
    
    # Invoke the model to get the prediction
    #response = main.llm.invoke(prompt)
    response = formatted_team1
    
    # Print the matchup and prediction for visibility
    print(f"[{round_name}] {formatted_team1} vs {formatted_team2} -> {response.strip()}")
    
    # Prepare a result string for later reference
    result_text = f"{formatted_team1} vs {formatted_team2} -> {response.strip()}"
    return result_text

def simulate_bracket(file_path):
    """
    Reads the bracket file, processes each game, groups results by round,
    and writes out a separate text file for each round.
    """
    # Create the bracket_predictions directory if it doesn't exist
    os.makedirs("bracket_predictions", exist_ok=True)
    
    rounds_results = {}
    
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            round_name = row["Round"].strip()
            team1 = row["Team1"].strip()
            seed1 = row["Seed1"].strip()
            team2 = row["Team2"].strip()
            seed2 = row["Seed2"].strip()
            
            # Get the result for the game
            result_text = run_game(team1, seed1, team2, seed2, round_name)
            
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

if __name__ == "__main__":
    simulate_bracket("code/bracket.txt")