# display_bracket.py

def display_bracket():
    # Define the rounds in the proper order
    rounds_order = [
        "First Four",
        "First Round",
        "Second Round",
        "Sweet Sixteen",
        "Elite Eight",
        "Final Four",
        "Championship"
    ]
    
    # Print a header for the final bracket display
    print("=" * 60)
    print("FINAL BRACKET PREDICTIONS".center(60))
    print("=" * 60)
    
    # Iterate through each round and print its results
    for round_name in rounds_order:
        # Convert round name to filename by replacing spaces with underscores
        filename = f"bracket_predictions/{round_name.replace(' ', '_')}.txt"
        try:
            with open(filename, "r") as f:
                games = f.read().splitlines()
        except FileNotFoundError:
            games = []
        
        print("\n" + round_name.upper().center(60))
        print("-" * 60)
        if not games:
            print("No results for this round.".center(60))
        else:
            # Number each game for clarity
            for idx, game in enumerate(games, start=1):
                print(f"Game {idx}: {game}")
        print("-" * 60)
    
    # Display the championship result separately
    championship_file = "bracket_predictions/Championship.txt"
    try:
        with open(championship_file, "r") as f:
            champ_result = f.read().strip()
    except FileNotFoundError:
        champ_result = "No Championship game result found."
    
    print("\n" + "=" * 60)
    print("CHAMPION".center(60))
    print("=" * 60)
    print(champ_result.center(60))
    print("=" * 60)

if __name__ == "__main__":
    display_bracket()