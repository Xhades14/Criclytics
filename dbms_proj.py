import os
import json
import pymysql
from datetime import datetime

# Database connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root@DBMS',
    database='criclytics',
    autocommit=True
)

# Cursor for database operations
cursor = connection.cursor()

# Directory containing JSON files
json_directory = 'C:/Users/Manu/Downloads/t20s_male_json'

def insert_innings_data(json_data, match_id):
    try:
        for inning_number, inning in enumerate(json_data['innings'], start=1):
            team_name = inning['team']
            cursor.execute("SELECT id FROM teams WHERE name = %s", (team_name,))
            team_id = cursor.fetchone()[0]

            # Insert innings record
            cursor.execute(
                "INSERT INTO innings (match_id, team_id, inning_number, innings_type) VALUES (%s, %s, %s, %s)",
                (match_id, team_id, inning_number, 'Batting')
            )
            inning_id = cursor.lastrowid

            # Start of each inning
            total_runs = 0
            total_wickets = 0
            total_overs = 0  # Reset overs for each inning

            for over_data in inning['overs']:
                over_number = over_data['over']
                total_overs += 1

                cursor.execute(
                    "INSERT INTO overs (inning_id, over_number) VALUES (%s, %s)",
                    (inning_id, over_number)
                )
                over_id = cursor.lastrowid

                over_runs = 0
                over_wickets = 0
                over_extras = 0

                for delivery_number, delivery in enumerate(over_data['deliveries'], start=1):
                    batter_name = delivery['batter']
                    bowler_name = delivery['bowler']
                    non_striker_name = delivery['non_striker']
                    runs_batter = delivery['runs']['batter']
                    runs_extras = delivery['runs']['extras']
                    runs_total = delivery['runs']['total']

                    total_runs += runs_total
                    over_runs += runs_total
                    over_extras += runs_extras

                    # Retrieve player IDs for batter and bowler
                    cursor.execute("SELECT id FROM players WHERE name = %s", (batter_name,))
                    batter_result = cursor.fetchone()
                    batter_id = batter_result[0] if batter_result else None

                    cursor.execute("SELECT id FROM players WHERE name = %s", (bowler_name,))
                    bowler_result = cursor.fetchone()
                    bowler_id = bowler_result[0] if bowler_result else None

                    # Determine if it's a boundary and type
                    is_boundary = False
                    boundary_type = None
                    if runs_batter == 4:
                        is_boundary = True
                        boundary_type = 'four'
                    elif runs_batter == 6:
                        is_boundary = True
                        boundary_type = 'six'

                    # Check if there are extras and define extra_type
                    extra_type = None
                    if runs_extras > 0:
                        if 'extras' in delivery:
                            if 'wides' in delivery['extras']:
                                extra_type = 'wide'
                            elif 'noballs' in delivery['extras']:
                                extra_type = 'noball'
                            elif 'byes' in delivery['extras']:
                                extra_type = 'bye'
                            elif 'legbyes' in delivery['extras']:
                                extra_type = 'legbye'
                            elif 'penalty' in delivery['extras']:
                                extra_type = 'penalty'

                    # Check if the delivery resulted in a wicket
                    is_wicket = 0  # Default value if no wicket
                    dismissal_type = None
                    fielder_id = None
                    if 'wickets' in delivery and delivery['wickets']:
                        is_wicket = 1  # Set is_wicket to 1 when there's a dismissal
                        total_wickets += 1
                        over_wickets += 1

                        dismissal_info = delivery['wickets'][0]
                        dismissal_type = dismissal_info.get('kind')

                        if dismissal_type == 'caught':
                            fielder_name = dismissal_info.get('fielders')[0].get('name')
                            cursor.execute("SELECT id FROM players WHERE name = %s", (fielder_name,))
                            fielder = cursor.fetchone()
                            if fielder:
                                fielder_id = fielder[0]

                            cursor.execute(
                                """INSERT INTO player_stats (inning_id, player_id, team_id, catches) 
                                   VALUES (%s, %s, %s, 1) 
                                   ON DUPLICATE KEY UPDATE catches = catches + 1""",
                                (inning_id, fielder_id, team_id)
                            )

                    # Insert delivery data with all relevant fields
                    cursor.execute(
                        """INSERT INTO ball_by_ball 
                           (over_id, ball_number, batsman_id, bowler_id, runs_scored, is_wicket, dismissal_type, 
                            fielder_id, is_boundary, boundary_type, extra_type, extra_runs) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (over_id, delivery_number, batter_id, bowler_id, runs_total, is_wicket, dismissal_type,
                         fielder_id, is_boundary, boundary_type, extra_type, runs_extras)
                    )

                    # Update bowler stats
                    cursor.execute(
                        """INSERT INTO player_stats (inning_id, player_id, team_id, wickets_taken, runs_conceded) 
                           VALUES (%s, %s, %s, %s, %s) 
                           ON DUPLICATE KEY UPDATE wickets_taken = wickets_taken + %s, runs_conceded = runs_conceded + %s""",
                        (inning_id, bowler_id, team_id, int(is_wicket), runs_total, int(is_wicket), runs_total)
                    )

                cursor.execute(
                    """UPDATE overs SET runs_scored = %s, wickets_taken = %s, extras = %s 
                       WHERE id = %s""",
                    (over_runs, over_wickets, over_extras, over_id)
                )

            # Update innings table
            cursor.execute(
                """UPDATE innings SET runs_scored = %s, wickets_lost = %s, overs = %s 
                   WHERE id = %s""",
                (total_runs, total_wickets, total_overs, inning_id)
            )

    except pymysql.MySQLError as e:
        print(f"Error inserting innings data: {e}")

def insert_data(json_data):
    try:
        # Insert player and team data
        for team_name, players in json_data['info']['players'].items():
            for player_name in players:
                cursor.execute("SELECT id FROM players WHERE name = %s", (player_name,))
                player = cursor.fetchone()
                if not player:
                    # If the player doesn't exist, insert them into the database
                    try:
                        cursor.execute(
                            "INSERT INTO players (name, nationality) VALUES (%s, %s)", 
                            (player_name, team_name)
                        )
                        player_id = cursor.lastrowid  # Get the player_id of the newly inserted player
                    except pymysql.MySQLError as e:
                        continue  # Skip this player if there's an error
                else:
                    player_id = player[0]

                cursor.execute("SELECT id FROM teams WHERE name = %s", (team_name,))
                team = cursor.fetchone()
                if not team:
                    cursor.execute(
                        "INSERT INTO teams (name, nation) VALUES (%s, %s)",
                        (team_name, team_name[:3])
                    )
                    team_id = cursor.lastrowid
                else:
                    team_id = team[0]

                cursor.execute("SELECT * FROM player_teams WHERE player_id = %s AND team_id = %s", (player_id, team_id))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO player_teams (player_id, team_id, from_date) VALUES (%s, %s, %s)",
                        (player_id, team_id, datetime.now().date())
                    )

        # Insert venue data
        match_info = json_data['info']
        venue_name = match_info['venue']
        cursor.execute("SELECT id FROM venues WHERE name = %s", (venue_name,))
        venue = cursor.fetchone()
        if not venue:
            cursor.execute(
                "INSERT INTO venues (name, city) VALUES (%s, %s)",
                (venue_name, match_info.get('city', 'Unknown'))
            )
            venue_id = cursor.lastrowid
        else:
            venue_id = venue[0]

        # Insert match record with additional details
        match_date = datetime.strptime(match_info['dates'][0], '%Y-%m-%d').date()
        cursor.execute("SELECT id FROM teams WHERE name = %s", (match_info['toss']['winner'],))
        toss_winner_id = cursor.fetchone()[0]
        toss_decision = match_info['toss']['decision']

        team1_name = match_info['teams'][0]
        team2_name = match_info['teams'][1]

        # Query the database for team IDs
        cursor.execute("SELECT id FROM teams WHERE name = %s", (team1_name,))
        team_id1 = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM teams WHERE name = %s", (team2_name,))
        team_id2 = cursor.fetchone()[0]

        # Extract winner and victory margin if available
        outcome = match_info.get('outcome', {})
        winner_name = outcome.get('winner')
        winner_id = None
        result = None

        if winner_name:
            cursor.execute("SELECT id FROM teams WHERE name = %s", (winner_name,))
            winner_result = cursor.fetchone()
            winner_id = winner_result[0] if winner_result else None

        if 'by' in outcome:
            if 'runs' in outcome['by']:
                runs = outcome['by']['runs']
                result = f"Won by {runs} runs"
            elif 'wickets' in outcome['by']:
                wickets = outcome['by']['wickets']
                result = f"Won by {wickets} wickets"

        # Extract Player of the Match if available
        player_of_match_list = match_info.get('player_of_match', [])
        player_of_match = player_of_match_list[0] if player_of_match_list else None

        if player_of_match:
            cursor.execute("SELECT id FROM players WHERE name = %s", (player_of_match,))
            potm_result = cursor.fetchone()
            potm_id = potm_result[0] if potm_result else None
        else:
            potm_id = None

        # Insert data into the matches table
        cursor.execute(
            """INSERT INTO matches (date_of_match, venue_id, toss_winner_id, toss_decision, team1_id, team2_id, winner_id, result, POTM) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (match_date, venue_id, toss_winner_id, toss_decision, team_id1, team_id2, winner_id, result, potm_id)
        )

        match_id = cursor.lastrowid

        # Insert innings data
        insert_innings_data(json_data, match_id)

    except pymysql.MySQLError as e:
        print(f"Error inserting data: {e}")

# Load all JSON files
for file_name in os.listdir(json_directory):
    if file_name.endswith('.json'):
        file_path = os.path.join(json_directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            insert_data(json_data)

# Close connection
cursor.close()
connection.close()
