import os
import pandas as pd
import re
import glob
import argparse
import logging

# Set up logging to only output error messages with detailed information.
logging.basicConfig(
    level=logging.ERROR,
    format="[%(asctime)s] %(levelname)s - %(message)s",
)

# Example name mapping: Map bracket names to the names as found in the team-stats files.
# Adjust these keys and values to suit your data.
name_map = {
    # A
    "AR-Pine Bluff": "Arkansas Pine Bluff",  # KenPom: "Arkansas Pine Bluff"
    "Abilene Christian": "Abilene Christian",
    "Akron": "Akron",
    "Alabama": "Alabama",
    "American": "American",
    "Arizona": "Arizona",
    "Arizona St.": "Arizona St.",
    "Arkansas": "Arkansas",
    "Auburn": "Auburn",
    "Austin Peay": "Austin Peay",
    
    # B
    "Bakersfield": "Cal St. Bakersfield",
    "Baylor": "Baylor",
    "Belmont": "Belmont",
    "Boise St.": "Boise St.",
    "Boston U": "Boston University",
    "Bradley": "Bradley",
    "Bucknell": "Bucknell",
    "Buffalo": "Buffalo",
    "Butler": "Butler",
    
    # C
    "Cal Poly": "Cal Poly",
    "California": "California",
    "Charleston": "Charleston Southern",  # or "College of Charleston" (KenPom has both "Charleston" and "College of Charleston" depending on year)
    "Chattanooga": "Chattanooga",
    "Cincinatti": "Cincinnati",  # Spelling difference
    "Clemson": "Clemson",
    "Cleveland St.": "Cleveland St.",
    "Colgate": "Colgate",
    "Coloado St.": "Colorado St.",  # Spelling fix
    "Colorado": "Colorado",
    "Colorado St.": "Colorado St.",
    "Cornell": "Cornell",
    "Costal Carolina": "Coastal Carolina",  # Spelling fix
    "Creighton": "Creighton",
    
    # D
    "Davidson": "Davidson",
    "Dayton": "Dayton",
    "Delaware": "Delaware",
    "Detroit Mercy": "Detroit",
    "Drake": "Drake",
    "Drexel": "Drexel",
    "Duke": "Duke",
    "Duquesne": "Duquesne",
    
    # E
    "E Washington": "Eastern Washington",
    "East Washington": "Eastern Washington",
    "ETSU": "East Tennessee St.",
    
    # F
    "Fair Dickinson": "Fairleigh Dickinson",
    "FAU": "Florida Atlantic",
    "FGCU": "Florida Gulf Coast",
    "Florida": "Florida",
    "Florida St.": "Florida St.",
    "Fresno St.": "Fresno St.",
    "Fullerton": "Cal St. Fullerton",
    "Furman": "Furman",
    
    # G
    "G Washington": "George Washington",
    "Gardner-Webb": "Gardner Webb",
    "George Mason": "George Mason",
    "Georgetown": "Georgetown",
    "Georgia": "Georgia",
    "Georgia St.": "Georgia St.",
    "Georgia Tech": "Georgia Tech",
    "Gonzaga": "Gonzaga",
    "Grambling St.": "Grambling St.",
    "Grand Canyon": "Grand Canyon",
    "Green Bay": "Green Bay",
    
    # H
    "Hampton": "Hampton",
    "Hartford": "Hartford",
    "Harvard": "Harvard",
    "Hawai'i": "Hawaii",
    "Holy Cross": "Holy Cross",
    "Houston": "Houston",
    "Howard": "Howard",
    
    # I
    "Illinois": "Illinois",
    "Indiana": "Indiana",
    "Indiana St.": "Indiana St.",
    "Iona": "Iona",
    "Iowa": "Iowa",
    "Iowa St.": "Iowa St.",
    
    # J
    # "Jackson St." is different from "Jacksonville St."
    # If "Jax St." was meant to be "Jacksonville St.," do this:
    "Jax St.": "Jacksonville St.",
    
    # K
    "Kansas": "Kansas",
    "Kansas St.": "Kansas St.",
    "Kennesaw St.": "Kennesaw St.",
    "Kent State": "Kent St.",
    "Kentucky": "Kentucky",
    
    # L
    "LSU": "LSU",
    "La Salle": "La Salle",
    "Lafayette": "Lafayette",
    "Lehigh": "Lehigh",
    "Liberty": "Liberty",
    "Lipscomb": "Lipscomb",
    "Little Rock": "Arkansas Little Rock",  # KenPom also calls it "Arkansas Little Rock"; "Little Rock" is fine
    "Long Beach St.": "Long Beach St.",
    "Long Island": "LIU",  # or "LIU Brooklyn" – ambiguous
    "Long Island": "LIU Brooklyn",
    "Longwood": "Longwood",
    "Louisiana": "Louisiana",
    "Louisiana Lafayette": "Louisiana Lafayette",  # Some years might appear as "Louisiana Lafayette"
    "Louisville": "Louisville",
    "Loyola Chicago": "Loyola Chicago",
    "Loyola MD": "Loyola MD",
    
    # M
    "MTSU": "Middle Tennessee",
    "Manhattan": "Manhattan",
    "Marquette": "Marquette",
    "Marshall": "Marshall",
    "Maryland": "Maryland",
    "McNeese": "McNeese St.",
    "Memphis": "Memphis",
    "Mercer": "Mercer",
    "Miami OH": "Miami OH",
    "Miami": "Miami FL",  # "Miami (FL)" in KenPom
    "Michigan": "Michigan",
    "Michigan St.": "Michigan St.",
    "Milwaukee": "Milwaukee",
    "Minnesota": "Minnesota",
    "Mississippi St.": "Mississippi St.",  # "Ole Miss" below is "Mississippi"
    "Missouri": "Missouri",
    "Montana": "Montana",
    "Montana St.": "Montana St.",
    "Morehead St.": "Morehead St.",
    "Morgan St.": "Morgan St.",
    "Mount Saint Mary's": "Mount St. Mary's",
    "Murray St": "Murray St.",
    "Murray St.": "Murray St.",
    
    # N
    "NC A&T": "North Carolina A&T",
    "NC Central": "North Carolina Central",
    "NC State": "N.C. State",
    "Nebraska": "Nebraska",
    "Nevada": "Nevada",
    "New Mexico": "New Mexico",
    "New Mexico St.": "New Mexico St.",
    "Norfolk St.": "Norfolk St.",
    "North Carolina": "North Carolina",
    "North Colorado": "Northern Colorado",
    "North Dakota": "North Dakota",
    "North Dakota St.": "North Dakota St.",
    "North Kentucky": "Northern Kentucky",  # sp fix
    "North Texas": "North Texas",
    "Northeastern": "Northeastern",
    "Northern Iowa": "Northern Iowa",
    "Northern Kentucky": "Northern Kentucky",
    "Northwestern": "Northwestern",
    "Northwestern St.": "Northwestern St.",
    "Notre Dame": "Notre Dame",
    
    # O
    "Oakland": "Oakland",
    "Ohio": "Ohio",
    "Ohio St": "Ohio St.",
    "Ohio St.": "Ohio St.",
    "Oklahoma": "Oklahoma",
    "Oklahoma St.": "Oklahoma St.",
    "Old Dominion": "Old Dominion",
    "Ole Miss": "Mississippi",  # KenPom uses "Mississippi" for Ole Miss
    "Oral Roberts": "Oral Roberts",
    "Oregon": "Oregon",
    "Oregon St.": "Oregon St.",
    
    # P
    "Pacific": "Pacific",
    "Penn": "Penn",
    "Penn St.": "Penn St.",
    "Pitt": "Pittsburgh",
    "Princeton": "Princeton",
    "Providence": "Providence",
    "Purdue": "Purdue",
    
    # R
    "Radford": "Radford",
    "Rhode Island": "Rhode Island",
    "Richmond": "Richmond",
    "Richmonnd": "Richmond",  # Typo
    "Robert Morris": "Robert Morris",
    "Rutgers": "Rutgers",
    
    # S
    "SF Austin": "Stephen F. Austin",
    "SMU": "SMU",
    "Saint Bonaventure": "St. Bonaventure",
    "Saint Joesph's": "Saint Joseph's",  # Typo fix
    "Saint John's": "St. John's",
    "Saint Joseph's": "Saint Joseph's",
    "Saint Louis": "Saint Louis",
    "Saint Mary's": "Saint Mary's",
    "Saint Peter's": "Saint Peter's",
    "Sam Houston": "Sam Houston St.",
    "Samford": "Samford",
    "San Diego St.": "San Diego St.",
    "San Francisco": "San Francisco",
    "Santa Barbara": "UC Santa Barbara",
    "Seton  Hall": "Seton Hall",  # extra space
    "Seton Hall": "Seton Hall",
    "Sienna": "Siena",  # Spelling fix
    "South Carolina": "South Carolina",
    "South Dakota St.": "South Dakota St.",
    "South Florida": "South Florida",
    "Southern": "Southern",
    "Southern Miss": "Southern Miss",
    "St. Bonaventure": "St. Bonaventure",
    "St. Mary's": "Saint Mary's",
    "Stanford": "Stanford",
    "Stetson": "Stetson",
    "Stony Brook": "Stony Brook",
    "Syracuse": "Syracuse",
    
    # T
    "TCU": "TCU",
    "Temple": "Temple",
    "Tennesee": "Tennessee",  # Spelling fix
    "Tennesse": "Tennessee",  # Spelling fix
    "Tennessee": "Tennessee",
    "Texas": "Texas",
    "Texas A&M": "Texas A&M",
    "Texas A&M-CC": "Texas A&M Corpus Chris",
    "Texas Southern": "Texas Southern",
    "Texas Tech": "Texas Tech",
    "Troy": "Troy",
    "Tulsa": "Tulsa",
    
    # U
    "UAB": "UAB",
    "UAlbany": "Albany",  # "UAlbany" is the same as "Albany"
    "UC Davis": "UC Davis",
    "UC Irvine": "UC Irvine",
    "UCF": "UCF",
    "UCLA": "UCLA",
    "UConn": "Connecticut",
    "UMBC": "UMBC",
    "UNC Asheville": "UNC Asheville",
    "UNC Greensboro": "UNC Greensboro",
    "UNC Wilmington": "UNC Wilmington",
    "UNLV": "UNLV",
    "USC": "USC",
    "UTEP": "UTEP",
    "UTSA": "UTSA",
    "Ualbany": "Albany",  # duplicate
    "Uconn": "Connecticut",  # duplicate
    "Umass": "Massachusetts",
    "Utah": "Utah",
    "Utah St.": "Utah St.",
    
    # V
    "VCU": "VCU",
    "Valparaiso": "Valparaiso",
    "Vanderbilt": "Vanderbilt",
    "Vermont": "Vermont",
    "Villanova": "Villanova",
    "Virginia": "Virginia",
    "Virginia Tech": "Virginia Tech",
    
    # W
    "Wagner": "Wagner",
    "Wake Forest": "Wake Forest",
    "Washington": "Washington",
    "Washington St.": "Washington St.",
    "Weber St.": "Weber St.",
    "West Virginia": "West Virginia",
    "Western Kentucky": "Western Kentucky",
    "Western Michigan": "Western Michigan",
    "Wichita St": "Wichita St.",
    "Wichita St.": "Wichita St.",
    "Winthrop": "Winthrop",
    "Wisconsin": "Wisconsin",
    "Wisconson": "Wisconsin",  # Spelling fix
    "Wofford": "Wofford",
    "Wright St.": "Wright St.",
    "Wyoming": "Wyoming",
    
    # X
    "Xavier": "Xavier",
    
    # Y
    "Yale": "Yale"
}

def strip_seed(team_name: str) -> str:
    """
    Removes trailing seeding (digits) from the team name.
    For instance:
      "Gonzaga 1"    -> "Gonzaga"
      "Virginia 12"  -> "Virginia"
    """
    if not isinstance(team_name, str):
        return team_name  # If it's not a string, just return it unchanged
    
    # This regex looks for zero-or-more spaces followed by one-or-more digits
    # at the very end of the string, and removes them:
    return re.sub(r"\s*\d+\**\s*$", "", team_name).strip()




def map_team_name(team_name):
    """Returns the mapped team name if present; otherwise returns the original."""
    # Remove extra whitespace and any trailing seed number.
    team_name = team_name.strip()
    team_name = strip_seed(team_name)
    return name_map.get(team_name, team_name)

def load_all_bracket_data(bracket_dir, start_year=2010, end_year=2024):
    """
    Loads bracket matchups from CSV files in bracket_dir for each year in [start_year, end_year].
    Returns a single DataFrame with a 'Year' column appended.
    Skips any years for which the file does not exist or cannot be read.
    """
    all_brackets = []
    #print(f"[DEBUG] Loading bracket data from {bracket_dir} for years {start_year} to {end_year}...")

    for year in range(start_year, end_year + 1):
        filename = f"{year}.csv"
        path = os.path.join(bracket_dir, filename)
        #print(f"[DEBUG] Looking for bracket file: {path}")

        if not os.path.isfile(path):
            print(f"  [WARNING] Bracket file for {year} not found at: {path}. Skipping.")
            continue

        try:
            df = pd.read_csv(path)
            df['Year'] = year
            all_brackets.append(df)
            #print(f"  [INFO] Successfully loaded bracket file for {year} with {len(df)} rows.")
        except Exception as e:
            print(f"  [ERROR] Could not read bracket file for {year}: {e}. Skipping.")
            continue

    if not all_brackets:
        print("[WARNING] No bracket files were loaded at all!")
        return pd.DataFrame()

    combined_brackets_df = pd.concat(all_brackets, ignore_index=True)
    #print(f"[INFO] Combined bracket DataFrame shape: {combined_brackets_df.shape}")
    return combined_brackets_df


def load_team_stats(team_dir, start_year=2010, end_year=2024):
    """
    Loads team stats from CSV files in team_dir for each year in [start_year, end_year].
    Returns a dict {year: DataFrame}.
    Skips any years for which the file does not exist or cannot be read.
    """
    year_to_df = {}
    #print(f"[DEBUG] Loading team stats from {team_dir} for years {start_year} to {end_year}...")

    for year in range(start_year, end_year + 1):
        filename = f"k{year}.csv"
        path = os.path.join(team_dir, filename)
        #print(f"[DEBUG] Looking for team-stats file: {path}")

        if not os.path.isfile(path):
            print(f"  [WARNING] Team-stats file for {year} not found at: {path}. Skipping.")
            continue

        try:
            df = pd.read_csv(path)
            #print(f"  [INFO] Successfully loaded team-stats file for {year} with {len(df)} rows.")

            # Clean or parse W-L into numeric Wins/Losses if it exists
            if 'W-L' in df.columns:
                try:
                    df[['Wins', 'Losses']] = df['W-L'].str.split('-', expand=True).astype(int)
                    df['WinPct'] = df['Wins'] / (df['Wins'] + df['Losses'])
                    #print("  [DEBUG] Parsed W-L column into Wins, Losses, and WinPct.")
                except Exception as parse_err:
                    print(f"  [WARNING] Could not parse W-L for {year}: {parse_err}")

            # Make sure there's a 'Year' column
            df['Year'] = year

            # Standardize the 'Team' column by stripping whitespace and removing trailing seed digits.
            df['Team'] = df['Team'].str.strip().apply(strip_seed)

            year_to_df[year] = df

        except Exception as e:
            print(f"  [ERROR] Could not read team-stats file for {year}: {e}. Skipping.")
            continue

    if not year_to_df:
        print("[WARNING] No team-stats files were loaded at all!")

    return year_to_df


def create_merged_dataset(bracket_df, teamstats_by_year):
    """
    Merges bracket data with each team's stats for the same year.
    Applies team name mapping before merging.
    Produces a single DataFrame that can be saved and used in LangChain.
    """
    #print("[DEBUG] Beginning merge of bracket and team-stats data...")
    merged_rows = []

    if bracket_df.empty:
        print("[WARNING] Bracket DataFrame is empty, nothing to merge.")
        return pd.DataFrame()

    for idx, row in bracket_df.iterrows():
        year = row.get('Year')
        # Get original team names from the bracket file.
        orig_team1 = row.get('Team1')
        orig_team2 = row.get('Team2')
        # Apply name mapping.
        team1 = map_team_name(orig_team1)
        team2 = map_team_name(orig_team2)
        winner = row.get('Winner')
        game_round = row.get('Round', None)
        score = row.get('Score', None)
        region = row.get('Region', None)
        seed1 = row.get('Seed1', None)
        seed2 = row.get('Seed2', None)

        # Check if team stats exists for the given year.
        if year in teamstats_by_year:
            year_stats = teamstats_by_year[year]
            t1_match = year_stats[year_stats["Team"] == team1]
            if not t1_match.empty:
                x = 1
                #print(f"[DEBUG] KenPom team for mapped team '{team1}' is '{t1_match.iloc[0]['Team']}'.")
            else:
                print(f"[DEBUG] No KenPom team found for mapped team '{team1}'.")
        else:
            print(f"  [WARNING] No team-stats DataFrame for year {year} available. Unable to merge teams: "
                  f"Team1='{team1}' (originally '{orig_team1}') and Team2='{team2}' (originally '{orig_team2}'). Skipping this row.")
            continue

        # Attempt to locate the stats for the mapped names.
        t1_stats = year_stats[year_stats['Team'] == team1]
        t2_stats = year_stats[year_stats['Team'] == team2]

        if t1_stats.empty:
            print(f"  [WARNING] Team '{team1}' (originally '{orig_team1}') was not merged because no matching stats "
                  f"were found in the team stats for year {year}. Skipping row.")
            continue
        if t2_stats.empty:
            print(f"  [WARNING] Team '{team2}' (originally '{orig_team2}') was not merged because no matching stats "
                  f"were found in the team stats for year {year}. Skipping row.")
            continue

        t1_row = t1_stats.iloc[0].to_dict()
        t2_row = t2_stats.iloc[0].to_dict()

        row_out = {
            'Year': year,
            'Round': game_round,
            'Region': region,
            'Team1': team1,
            'Seed1': seed1,
            'Team2': team2,
            'Seed2': seed2,
            'Score': score,
            'Winner': winner,

            'Team1_Conf': t1_row.get('Conf', None),
            'Team1_Wins': t1_row.get('Wins', None),
            'Team1_Losses': t1_row.get('Losses', None),
            'Team1_WinPct': t1_row.get('WinPct', None),
            'Team1_NetRtg': t1_row.get('NetRtg', None),
            'Team1_ORtg': t1_row.get('ORtg', None),
            'Team1_DRtg': t1_row.get('DRtg', None),

            'Team2_Conf': t2_row.get('Conf', None),
            'Team2_Wins': t2_row.get('Wins', None),
            'Team2_Losses': t2_row.get('Losses', None),
            'Team2_WinPct': t2_row.get('WinPct', None),
            'Team2_NetRtg': t2_row.get('NetRtg', None),
            'Team2_ORtg': t2_row.get('ORtg', None),
            'Team2_DRtg': t2_row.get('DRtg', None),
        }

        merged_rows.append(row_out)
        #print(f"  [INFO] Successfully merged stats for Team1='{team1}' and Team2='{team2}' (Year={year}).")

    merged_df = pd.DataFrame(merged_rows)
    #print(f"[INFO] Finished merging. Final merged DataFrame shape: {merged_df.shape}")
    return merged_df


def load_bracket_data():
    # Hard-coded path to bracket data.
    bracket_dir = r"C:\Users\shawn\OneDrive\Desktop\Spring 2025\CSE 5914 (AI Capstone)\Capstone\data\bracket_data"
    
    data = {}
    excluded_files = []
    try:
        for file in os.listdir(bracket_dir):
            file_path = os.path.join(bracket_dir, file)
            try:
                with open(file_path, "r") as f:
                    data[file] = f.read()
            except Exception as e:
                logging.exception(f"Error reading bracket data file '{file_path}'")
                excluded_files.append(file)
    except Exception as e:
        logging.exception(f"Error listing bracket data directory '{bracket_dir}'")
    
    if excluded_files:
        logging.error(f"Excluded bracket data files due to errors: {', '.join(excluded_files)}")
    return data

def load_team_data():
    # Hard-coded path to team data (Kenpom data).
    team_data_dir = r"C:\Users\shawn\OneDrive\Desktop\Spring 2025\CSE 5914 (AI Capstone)\Capstone\data\kenpom_data"
    
    data = {}
    excluded_files = []
    try:
        for file in os.listdir(team_data_dir):
            file_path = os.path.join(team_data_dir, file)
            try:
                with open(file_path, "r") as f:
                    data[file] = f.read()
            except Exception as e:
                logging.exception(f"Error reading team data file '{file_path}'")
                excluded_files.append(file)
    except Exception as e:
        logging.exception(f"Error listing team data directory '{team_data_dir}'")
    
    if excluded_files:
        logging.error(f"Excluded team data files due to errors: {', '.join(excluded_files)}")
    return data

def main():
    # Define the directories and year range for loading the data.
    bracket_dir = r"C:\Users\shawn\OneDrive\Desktop\Spring 2025\CSE 5914 (AI Capstone)\Capstone\data\bracket_data"
    team_data_dir = r"C:\Users\shawn\OneDrive\Desktop\Spring 2025\CSE 5914 (AI Capstone)\Capstone\data\kenpom_data"
    start_year = 2010
    end_year = 2024
    
    # Load all bracket data from CSV files.
    #print("[INFO] Loading all bracket data...")
    bracket_df = load_all_bracket_data(bracket_dir, start_year, end_year)
    
    # Load team stats from CSV files.
    #print("[INFO] Loading all team stats data...")
    teamstats_by_year = load_team_stats(team_data_dir, start_year, end_year)
    
    # Merge the bracket data with the team-stats data.
    #print("[INFO] Merging bracket and team stats datasets...")
    merged_df = create_merged_dataset(bracket_df, teamstats_by_year)
    
    # Save the merged dataset to a CSV file.
    output_path = os.path.join(os.path.dirname(bracket_dir), "merged_dataset.csv")
    try:
        merged_df.to_csv(output_path, index=False)
        print(f"[INFO] Merged dataset saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save merged dataset: {e}")

if __name__ == "__main__":
    main()
