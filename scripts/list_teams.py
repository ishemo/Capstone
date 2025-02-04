import os
import re
import pandas as pd

def strip_seed(team_name: str) -> str:
    """
    Removes trailing seed indicators (like '10', '11*', '(12)', etc.) from the team name.
    Examples of transformations:
      'Iowa 10'       -> 'Iowa'
      'Kansas 1*'     -> 'Kansas'
      'Villanova (4)' -> 'Villanova'
    """
    if not isinstance(team_name, str):
        return team_name  # If it's not a string, just return as-is
    
    # Regex pattern to remove any trailing space/parenthesis/dash + digits + optional asterisks + optional closing parenthesis.
    # Then strip any leftover whitespace.
    cleaned = re.sub(r"[\s(\-]*\d+\**[\)]*$", "", team_name).strip()
    return cleaned

def gather_bracket_teams(bracket_dir, start_year=2010, end_year=2024):
    """
    Reads bracket CSVs in bracket_dir for each year in [start_year, end_year].
    Collects raw team names from 'Team1' and 'Team2'.
    Returns a set of those team names (with seeds stripped).
    """
    bracket_teams = set()

    for year in range(start_year, end_year + 1):
        filename = f"{year}.csv"  # Adjust if your bracket files differ, e.g. f"{year}_bracket.csv"
        path = os.path.join(bracket_dir, filename)

        if not os.path.isfile(path):
            print(f"[WARNING] Missing bracket file for {year} at: {path}. Skipping.")
            continue

        try:
            df = pd.read_csv(path)
            if 'Team1' in df.columns and 'Team2' in df.columns:
                # Gather raw bracket names from Team1 and Team2
                team1_list = df['Team1'].dropna().astype(str).tolist()
                team2_list = df['Team2'].dropna().astype(str).tolist()

                # Strip seeds and add to bracket_teams set
                for name in team1_list:
                    bracket_teams.add(strip_seed(name))
                for name in team2_list:
                    bracket_teams.add(strip_seed(name))

            else:
                print(f"[WARNING] File {filename} does not have Team1/Team2 columns.")

        except Exception as e:
            print(f"[ERROR] Could not read bracket file {filename} for year {year}: {e}")
            continue

    return bracket_teams

def gather_kenpom_teams(kenpom_dir, start_year=2010, end_year=2024):
    """
    Reads KenPom CSVs in kenpom_dir for each year in [start_year, end_year].
    Collects team names from the 'Team' column.
    Returns a set of team names with seeds stripped to match bracket team names.
    """
    kenpom_teams = set()

    for year in range(start_year, end_year + 1):
        filename = f"k{year}.csv"  # Adjust if your KenPom files differ
        path = os.path.join(kenpom_dir, filename)

        if not os.path.isfile(path):
            print(f"[WARNING] Missing KenPom file for {year} at: {path}. Skipping.")
            continue

        try:
            df = pd.read_csv(path)
            if 'Team' in df.columns:
                # Get team names and strip seeds
                team_list = df['Team'].dropna().astype(str).tolist()
                # Add stripped names to set
                for name in team_list:
                    kenpom_teams.add(strip_seed(name))
            else:
                print(f"[WARNING] File {filename} does not have 'Team' column.")

        except Exception as e:
            print(f"[ERROR] Could not read KenPom file {filename} for year {year}: {e}")
            continue

    return kenpom_teams

def main():
    # Adjust these to your local project structure
    bracket_dir = r"C:\Users\shawn\OneDrive\Desktop\Spring 2025\CSE 5914 (AI Capstone)\Capstone\data\bracket_data"
    kenpom_dir  = r"C:\Users\shawn\OneDrive\Desktop\Spring 2025\CSE 5914 (AI Capstone)\Capstone\data\kenpom_data"

    # Gather bracket teams (seed-stripped)
    bracket_teams = gather_bracket_teams(bracket_dir, 2010, 2024)

    # Gather KenPom teams (raw)
    kenpom_teams = gather_kenpom_teams(kenpom_dir, 2010, 2024)

    # Print bracket teams
    print("\n============================")
    print("Bracket Teams (Seed-Stripped)")
    print("============================\n")
    for team in sorted(bracket_teams):
        print(team)

    # Print KenPom teams
    print("\n============================")
    print("KenPom Teams (Raw)")
    print("============================\n")
    for team in sorted(kenpom_teams):
        print(team)

if __name__ == "__main__":
    main()
